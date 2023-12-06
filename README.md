# ao-conventional-pre-commit

A [`pre-commit`](https://pre-commit.com) hook to check commit messages for
[Conventional Commits](https://conventionalcommits.org) formatting, customized for Anderson Optimization format to include JIRA ticket numbers.

[See the GitBook for more details](https://app.gitbook.com/o/-MPk29w3J35c1gpH27R3/s/-MTfg11Sa9v8-geD90cu/process/overview-2#4.-commit-messages).

Forked from [compilerla/conventional-pre-commit](https://github.com/compilerla/conventional-pre-commit)

Works with Python >= 3.8.

## Usage

Make sure `pre-commit` is [installed](https://pre-commit.com#install).

Create a blank configuration file at the root of your repo, if needed:

```console
touch .pre-commit-config.yaml
```

Add a new repo entry to your configuration file:

```yaml
repos:
    # - repo: ...

    - repo: https://github.com/anderson-optimization/ao-conventional-pre-commit
      rev: <git sha or tag>
      hooks:
          - id: ao-conventional-pre-commit
            stages: [commit-msg]
            args: []
```

Install the `pre-commit` script:

```console
pre-commit install --hook-type commit-msg
```

Make a (normal) commit :x::

```console
$ git commit -m "add a new feature"

[INFO] Initializing environment for ....
AO Conventional Commit......................................................Failed
- hook id: ao-conventional-pre-commit
- duration: 0.07s
- exit code: 1

[Bad Commit message] >> add a new feature

Your commit message does not follow Conventional Commits formatting
https://www.conventionalcommits.org/

AO Conventional Commits start with one of the below types, followed by a colon,
followed by a ticket number and colon, followed by the commit message:

    build chore ci docs feat fix perf refactor revert style test

Example commit message adding a feature:

    feat: SVCOR-12: implement new API

Example commit message fixing an issue:

    fix: DTCT-99: remove infinite loop

Example commit with scope in parentheses after the type for more context:

    fix(account): PROSP-55: remove infinite loop

Example commit with a body:

    fix: DATLA-42: remove infinite loop

    Additional information on the issue caused by the infinite loop
```

Make a (conventional) commit :heavy_check_mark::

```console
$ git commit -m "feat: DTCT-33 add a new feature"

[INFO] Initializing environment for ....
AO Conventional Commit......................................................Passed
- hook id: ao-conventional-pre-commit
- duration: 0.05s
```

## Install with pip

`ao-conventional-pre-commit` can also be installed and used from the command line:

```shell
pip install ao-conventional-pre-commit
```

Then run the command line script:

```shell
ao-conventional-pre-commit [types] input
```

-   `[types]` is an optional list of Conventional Commit types to allow (e.g. `feat fix chore`)

-   `input` is a file containing the commit message to check:

```shell
ao-conventional-pre-commit feat fix chore ci test .git/COMMIT_MSG
```

Or from a Python program:

```python
from ao_conventional_pre_commit.format import is_conventional

# prints True
print(is_conventional("feat: DTCT-99: this is a conventional commit"))

# prints False
print(is_conventional("nope: DTCT-99: this is not a conventional commit"))

# prints True
print(is_conventional("custom: DTCT-99: this is a conventional commit", types=["custom"]))

# prints True
print(is_conventional("feat: this is a conventional commit", optional_ticket=True))

# prints False
print(is_conventional("feat: DTCT-99 this is not a conventional commit", optional_colon_after_ticket=False))
```

## Passing `args`

`ao-conventional-pre-commit` supports a number of arguments to configure behavior:

```shell
$ ao-conventional-pre-commit -h
usage: ao-conventional-pre-commit [-h] [--force-scope] [--strict] [types ...] input

Check a git commit message for Conventional Commits formatting.

positional arguments:
  types          Optional list of types to support
  input          A file containing a git commit message

options:
  -h, --help     show this help message and exit
  --force-scope  Force commit to have scope defined.
  --strict       Force commit to strictly follow Conventional Commits formatting. Disallows fixup! style commits.
  --optional-ticket     Allow for optional ticket number. This enables default conventional commit style.
  --force-colon-after-ticket
                        Force commit to contain a colon after ticket number.
```

Supply arguments on the command-line, or via the pre-commit `hooks.args` property:

```yaml
repos:
    - repo: https://github.com/anderson-optimization/ao-conventional-pre-commit
      rev: <git sha or tag>
      hooks:
          - id: ao-conventional-pre-commit
            stages: [commit-msg]
            args: [--strict, --force-scope, feat, fix, chore, test, custom]
```

**NOTE:** when using as a pre-commit hook, `input` is supplied automatically (with the current commit's message).

## Development

`ao-conventional-pre-commit` comes with a [VS Code devcontainer](https://code.visualstudio.com/learn/develop-cloud/containers)
configuration to provide a consistent development environment.

With the `Remote - Containers` extension enabled, open the folder containing this repository inside Visual Studio Code.

You should receive a prompt in the Visual Studio Code window; click `Reopen in Container` to run the development environment
inside the devcontainer.

If you do not receive a prompt, or when you feel like starting from a fresh environment:

1. `Ctrl/Cmd+Shift+P` to bring up the command palette in Visual Studio Code
1. Type `Remote-Containers` to filter the commands
1. Select `Rebuild and Reopen in Container` to completely rebuild the devcontainer
1. Select `Reopen in Container` to reopen the most recent devcontainer build

## Versioning

Versioning generally follows [Semantic Versioning](https://semver.org/).

## Making a release

Releases to PyPI and GitHub are triggered by pushing a tag.

1. Ensure all changes for the release are present in the `main` branch
1. Tag with the new version: `git tag vX.Y.Z` for regular release, `git tag vX.Y.Z-preN` for pre-release
1. Push the new version tag: `git push origin vX.Y.Z`

## License

[Apache 2.0](LICENSE)

Inspired by matthorgan's [`pre-commit-conventional-commits`](https://github.com/matthorgan/pre-commit-conventional-commits).
