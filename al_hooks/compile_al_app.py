import os
import argparse
import sys
import glob
import urllib.request
import subprocess
from typing import Any

args: dict[str, Any] = ()


def main():
    # Get the arguments from the command line using ArgumentParser
    init_args()

    # Determine whether the script is running in a GitHub runner
    if 'GITHUB_ACTIONS' in os.environ:
        compiler_path = download_compiler()
    else:
        compiler_path = get_compiler_path()
        if not compiler_path:
            print(
                'Please make sure you have the AL Language extension for VS Code installed.'
            )
            exit(1)

    # Get a list of valid app directories
    app_paths = get_app_paths()

    if len(app_paths) == 0:
        print('No valid app directory found.')

    failed_apps = []
    for app_path in app_paths:
        package_path = get_package_path(app_path)

        app_name = os.path.split(app_path)[1]
        print(f"Compiling '{app_name}'...")

        if compile_app(compiler_path, app_path, package_path) == 0:
            print(f"Successfully compiled '{app_name}'.")
        else:
            print(f"Failed to compile '{app_name}'.")
            if args['failFast']:
                exit(1)
            failed_apps.append(app_name)

    if len(failed_apps) == 0:
        print('All apps successfully compiled.')
    else:
        print(f"Failed to compile the following apps: {', '.join(failed_apps)}")
        exit(1)


def compile_app(compiler_path, app_path, package_path):
    global args
    verbose = args['verbose']

    # Run alc.exe with the project and package paths as arguments
    command = (
        f'"{compiler_path}" /project:"{app_path}" /packagecachepath:"{package_path}"'
    )
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )

    # Capture & print the output of the subprocess
    output, _ = process.communicate()
    if verbose:
        print(output.decode())

    # Return the exit code of the compiler
    return process.returncode


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'app',
        type=str,
        default='*',
        help='The app within the repository to compile. May be an absolute path or a glob pattern. (default: %(default)s)',
    )
    parser.add_argument(
        '-p',
        '--packages',
        type=str,
        default='.alpackages',
        help='Path to the package cache directory containing the dependencies. (default: %(default)s)',
    )
    parser.add_argument(
        '-V',
        '--version',
        type=str,
        default='11.0.787898',
        help='The version of the AL compiler. Only used when downloading the compiler from the Visual Studio marketplace. (default: %(default)s)',
    )
    parser.add_argument(
        '-U',
        '--compilerUrl',
        type=str,
        help='Alternate URL of the compiler. Only used when downloading the compiler from the Visual Studio marketplace. The default link is rate limited to 10 per day, so specify one if necessary.',
    )
    parser.add_argument(
        '-F',
        '--failFast',
        action='store_true',
        help='Aborts the run as soon as one of the apps fails to compile.',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='Enable verbose output.'
    )

    global args
    args = vars(parser.parse_args())

    if args['verbose']:
        print('Arguments:')
        print(args)


def get_package_path(app_path):
    global args
    packages = args['packages']

    if os.path.isabs(packages):
        package_path = packages
    else:
        package_path = os.path.join(app_path, packages).replace('\\', '/')
    return package_path


def get_app_paths():
    global args
    app = args['app']

    if os.path.isabs(app):
        # If the path is absolute, skip the pattern matching
        matched_paths = [app]
    else:
        # Get a list of all paths that match the glob pattern
        app_glob = os.path.join(os.getcwd(), app).replace('\\', '/')
        matched_paths = glob.glob(app_glob)

    # Remove directories that don't contain an app manifest
    filtered_paths = []
    for matched_path in matched_paths:
        matched_path = matched_path.replace('\\', '/')
        if is_AL_app(matched_path):
            filtered_paths.append(matched_path)
    return filtered_paths


def is_AL_app(app_path):
    return os.path.exists(os.path.join(app_path, 'app.json'))


def get_compiler_path():
    # Get the current user's username
    username = os.getlogin()

    # Set the relative path to alc.exe
    relative_path = '.vscode/extensions/ms-dynamics-smb.al-*/bin/alc.exe'

    # Combine the root directory with the relative path to create an absolute path
    compiler_glob = os.path.join('C:/Users', username, relative_path).replace('\\', '/')
    compiler_paths = glob.glob(compiler_glob)

    compiler_path = ''
    # Check if the file exists
    if len(compiler_paths) > 0:
        compiler_path = compiler_paths[0]
    return compiler_path


def download_compiler() -> str:
    global args
    compilerUrl, version = args['compilerUrl'], args['version']

    compiler_path = os.path.join(os.getcwd(), 'temp/alc.exe').replace('\\', '/')
    if not compilerUrl:
        compilerUrl = f'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-dynamics-smb/vsextensions/al/{version}/vspackage'

    if not os.path.exists(compiler_path):
        urllib.request.urlretrieve(compilerUrl, compiler_path)

    return compiler_path


if __name__ == '__main__':
    sys.exit(main())
