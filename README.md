# pre-commit hooks for AL

This is a collection of hooks designed for AL development that can be used with the [pre-commit framework](https://github.com/pre-commit/pre-commit).

## Installation

These hooks require the pre-commit framework, which is a python library. Check the [pre-commit site](https://pre-commit.com/#install) for details and a quickstart guide.

## Usage

In your `.pre-commit-config.yaml` configuration, add the following to the `repos` list:

```yml
-   repo: https://github.com/cegekaJG/AL-Pre-Commit-Hooks
    rev: v0.2.0  # Use the ref you want to point at
    hooks:
    -   id: compile-al-app
    #   args: [...]
    # -   id: ...
```

## Hooks available

### `compile-al-app`

Compiles all AL apps in the repository. You can use a glob pattern in the arguments to filter apps.

If run in a GitHub runner, it will download the `alc.exe` compiler from the Visual Studio marketplace.
Otherwise, this hook requires the AL extension for Visual Studio Code.

## ToDo

- [ ] Specify an output directory & a flag to keep the compiled apps
- [ ] Allow custom arguments to be passed to the compiler
- [ ] Read VS Code settings per app directory
- [ ] Automatically pass rulesets & CodeCops from VS Code settings
- [ ] Add tests
- [ ] *New hook*: Rename & reorganize AL object files from [CRS AL language extension](https://github.com/waldo1001/crs-al-language-extension)
- [ ] *New hook*: Code cleanup from [AZ AL Dev Tools](https://github.com/anzwdev/al-code-outline)
- [ ] *New hook*: Per-file linting
