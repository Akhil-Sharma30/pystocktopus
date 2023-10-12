# Contributing guide

If you are planning to develop `pystocktopus`, or want to use the latest commit
of `pystocktopus` on your local machine, you might want to install it from the
source. This installation is not recommended for users who want to use the
stable version of `pystocktopus`. The steps below describe the installation
process of `pystocktopus`'s latest commit. It also describes how to test
`pystocktopus`'s codebase and build `pystocktopus`'s documentation.

## Installing

We recommend using a virtual environment to install `pystocktopus`. This would
isolate the library from your global `Python` environment, which would be
beneficial for reproducing bugs, and the overall development of `pystocktopus`.
The first step would be to clone `pystocktopus` -

```bash
git clone https://github.com/Akhil-Sharma30/pystocktopus
```

and then we can change the current working directory and enter `pystocktopus` -

```bash
cd pystocktopus
```

### Creating a virtual environment

A virtual environment can be set up and activated using `venv` in and `Windows`
systems.

**Windows**:

```bash
python -m venv .tester_dev
.env\bin\activate
```

### Installing pystocktopus

`pystocktopus` uses modern `Python` packaging and can be installed using `pip` -

```bash
python -m pip install pystocktopus
```

The developer installation of `pystocktopus` comes with a lot of options -

- `test`: the test dependencies
- `docs`: extra dependencies to build and develop `pystocktopus`'s documentation
- `dev`: installs the `test` and `docs` dependencies

These options can be used with `pip` with the editable (`-e`) mode of
installation in the following ways -

```bash
pip install -e .[dev,test]
```

For example, if you want to install the `docs` dependencies along with the
dependencies included above, use -

```bash
pip install -e .[dev,test,docs]
```

## Activating pre-commit

`pystocktopus` uses a set of `pre-commit` hooks and the `pre-commit` bot to
format, type-check, and prettify the codebase. The hooks can be installed
locally using -

```bash
pre-commit install
```

This would run the checks every time a commit is created locally. The checks
will only run on the files modified by that commit, but the checks can be
triggered for all the files using -

```bash
pre-commit run --all-files
```

If you would like to skip the failing checks and push the code for further
discussion, use the `--no-verify` option with `git commit`.

## Submitting Code

The following is a _short_ list of recommendations. PRs that don't match these
criteria won't be closed but it'll be harder to merge the changes into the code.

- **Do** stick to [PEP8](https://www.python.org/dev/peps/pep-0008/).
- **Do** specify a descriptive title to make searching for your pull request
  easier.
- **Don't** leave your pull request description blank.
- **Do** license your code as GPLv3.

Also, please submit PRs to the `develop` branch.

#### Unit Tests

**Do** add unit tests if you think it fits. We place our unit tests in the same
folder as the code, with the same filename, followed by the \_test suffix. So
for example: `somefile.py` will be tested by `somefile_test.py`.

Please try to read some of the existing unit testing code, so you can see some
examples.

#### Branches Naming Scheme

**Do** name your branches in accordance with GitFlow. The format is
`ISSUE_#/BRANCH_NAME`; For example, `100/fix-for-pattern` or
`232/Documentation/add-new-feature`.

## Testing pystocktopus

`pystocktopus` is tested with `pytest` and `xdoctest`. `pytest` is responsible
for testing the code, whose configuration is available in
[pyproject.toml](https://github.com/Akhil-Sharma30/pystocktopus/blob/main/pyproject.toml),
and on the other hand, `xdoctest` is responsible for testing the examples
available in every docstring, which prevents them from going stale.
Additionally, `pystocktopus` also uses `pytest-cov` to calculate the coverage of
these unit tests.

### Running tests locally

The tests can be executed using the `test` dependencies of `pystocktopus` in the
following way -

```bash
python -m pytest
```

### Running tests with coverage locally

The coverage value can be obtained while running the tests using `pytest-cov` in
the following way -

```bash
python -m pytest --cov=pystocktopus tests/
```

A much more detailed guide on testing with `pytest` is available
[here](https://scikit-hep.org/developer/pytest).

## Documenting pystocktopus

`pystocktopus`'s documentation is mainly written in the form of
[docstrings](https://peps.python.org/pep-0257/) and
[Markdown](https://en.wikipedia.org/wiki/Markdown). The docstrings include the
description, arguments, examples, return values, and attributes of a class or a
function, and the `.md` files enable us to render this documentation on
`pystocktopus`'s documentation website.

`pystocktopus` primarily uses [MkDocs](https://www.mkdocs.org/) and
[mkdocstrings](https://mkdocstrings.github.io/) for rendering documentation on
its website. The configuration file (`mkdocs.yml`) for `MkDocs` can be found
[here](https://github.com/Akhil-Sharma30/pystocktopus/blob/main/mkdocs.yml). The
documentation is deployed on <https://readthedocs.io>
[here](https://pystocktopus.readthedocs.io/en/latest/).

Ideally, with the addition of every new feature to `pystocktopus`, documentation
should be added using comments, docstrings, and `.md` files.

### Building documentation locally

The documentation is located in the `docs` folder of the main repository. This
documentation can be generated using the `docs` dependencies of `pystocktopus`
in the following way -

```bash
mkdocs serve
```

The commands executed above will clean any existing documentation build, create
a new build (in `./site/`), and serve it on your `localhost`. To just build the
documentation, use -

```bash
mkdocs build
```

## Nox

`pystocktopus` supports running various critical commands using
[nox](https://github.com/wntrblm/nox) to make them less intimidating for new
developers. All of these commands (or sessions in the language of `nox`) -
`lint`, `tests`, `docs`, and `build` - are defined in
[noxfile.py](https://github.com/Akhil-Sharma30/pystocktopus/blob/main/noxfile.py).

`nox` can be installed via `pip` using -

```bash
pip install nox
```

The default sessions (`lint`, `tests`) can be executed using -

```bash
nox
```

### Running pre-commit with nox

The `pre-commit` hooks can be run with `nox` in the following way -

```bash
nox -s lint
```

### Running tests with nox

Tests can be run with `nox` in the following way -

```bash
nox -s tests
```

### Building documentation with nox

Docs can be built with `nox` in the following way -

```bash
nox -s docs
```

Use the following command if you want to deploy the docs on `localhost` -

```bash
nox -s docs -- serve
```
