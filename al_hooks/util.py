import subprocess
from typing import Any

class CalledProcessError(RuntimeError):
    pass

def cmd_output(*cmd: str, retcode: int | None = 0, **kwargs: Any) -> str:
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout

def added_files() -> set[str]:
    return changed_files('--diff-filter=A')

def changed_files(arg: str | None = None) -> set[str]:
    cmd = ('git', 'diff', '--staged', '--name-only')
    if arg is not None:
        cmd += arg
    return set(cmd_output(*cmd).splitlines())

def zsplit(s: str) -> list[str]:
    s = s.strip('\0')
    if s:
        return s.split('\0')
    else:
        return []