# Contributing to iotrace

Contributions to [iotrace](https://github.com/ktvanzwol/iotrace) are welcome from all!

iotrace is managed via [Git](https://git-scm.com), with the canonical upstream repository hosted on [GitHub](https://github.com/ktvanzwol/iotrace).

iotrace follows a pull request model for development. If you wish to contribute, you will need to create a GitHub account, fork this project, push a branch with your changes to your project, and then submit a pull request.

See [GitHub's official documentation](https://help.github.com/articles/using-pull-requests/) for more details.

## Getting Started

### Prerequisites

- Windows
- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) (recommended package manager)
- [NI IO Trace](https://www.ni.com/docs/en-US/bundle/ni-io-trace/page/overview.html) installed (required for system tests)

### Environment Setup

Clone the repository and install dependencies using [uv](https://docs.astral.sh/uv/):

``` shell
git clone https://github.com/ktvanzwol/iotrace.git
cd iotrace
uv sync
```

This will create a virtual environment and install all development dependencies.

### Code Formatting

iotrace uses [ruff](https://docs.astral.sh/ruff/) for formatting. To format the entire project, run:

``` shell
uv run ruff format
```

### Linting

iotrace uses [ruff](https://docs.astral.sh/ruff/) for linting. To lint the entire project, run:

``` shell
uv run ruff check
```

To automatically fix lint issues where possible:

``` shell
uv run ruff check --fix
```

### Testing

iotrace uses [pytest](https://docs.pytest.org/) to run tests. To run the unit tests:

``` shell
uv run pytest
```

To run tests with coverage:

``` shell
uv run pytest --cov
```

#### System Tests

Some tests require NI IO Trace to be installed on the machine. These are marked with the `system` marker and are skipped by default. To include system tests, pass the `--system` flag:

``` shell
uv run pytest --system
```

### Building

To build the project:

``` shell
uv build
```

If the build succeeds, artifacts will be placed in `dist/`.

### Releasing

Releases are triggered by pushing a version tag such as `v0.1.2`. The tag must
match the version in `pyproject.toml`. The release workflow runs lint and unit
tests on Windows, builds a wheel and source archive, publishes those artifacts
to PyPI, then creates a GitHub release with generated notes and the same files
attached. System tests are not run.

#### One-Time Setup

1. Create a GitHub environment named `pypi` in this repository's settings.
    Optionally require approval before deployments to this environment.
2. Configure a GitHub Trusted Publisher in the PyPI project's publishing settings:
    - Owner: `ktvanzwol`
    - Repository: `iotrace`
    - Workflow filename: `release.yml`
    - Environment: `pypi`

If the project does not yet exist on PyPI, configure a pending publisher for
`iotrace` instead. Trusted Publishing uses GitHub's short-lived identity tokens;
no PyPI API token or repository secret is required.

#### Create a Release

Choose a version that has not already been published to PyPI. For example:

``` shell
uv version 0.1.2
uv lock
git add pyproject.toml uv.lock
git commit -m "Release v0.1.2"
git push origin master
git tag v0.1.2
git push origin v0.1.2
```

Wait for branch CI to pass before pushing the tag. You can also edit the version
in `pyproject.toml` manually and run `uv lock` before committing. Monitor the
Release workflow in GitHub Actions, including any environment approval request.

PyPI versions cannot be overwritten. If publishing succeeds but GitHub release
creation fails, rerun only the failed job from GitHub Actions after resolving
the problem; do not rerun the publishing job or delete and recreate the tag.

## Developer Certificate of Origin (DCO)

   Developer's Certificate of Origin 1.1

   By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.

(taken from [developercertificate.org](https://developercertificate.org/))

See [LICENSE](https://github.com/ktvanzwol/iotrace/blob/main/LICENSE) for details about how iotrace is licensed.
