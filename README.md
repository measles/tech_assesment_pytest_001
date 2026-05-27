# Tech Assesment

## Setup
Assesment project is build on [uv package manager](https://docs.astral.sh/uv/getting-started/installation/). Before anything else ensure you have the up to day version installed.

Project utilizes [direnv](https://direnv.net/). To use it install it and activate it in a project root folder:
```bash
direnv allow .
```

This will automatically activate the environment and make a synchronization of a dev-environment packages.

It will be enough to install all developemt requirement.

To do it manually, execute:
```bash
uv sync --dev
source .venv/bin/activate
```

To setup pre-commit actions run:
```bash
pre-commit install 
```

## Execution
The project uses [nox](https://nox.thea.codes/) to automate test execution and linting.

### Running Tests
To run all tests and generate an HTML report, execute:

```bash
uv run nox -s tests
```

This will:
1. Run all tests in `src/tech_assesment_001`.
2. Generate a self-contained HTML report at `report.html`.
3. Display test results in a concise single-row format.

### Linting and Formatting
To run all formatters and linters (`black`, `isort`, `pylint`), execute:

```bash
uv run nox -s lint
```

### Preparing CI of a cloned repo to execution
CI pipeline should run tests in three cases:
1. Pull request to `main` branch
2. Merge to `main` branch
3. Externall call with a proper token

To prepare your clonned repo to execution you should set:
 - **BASE_URL** repo variable
 - **CREDENTIALS** repo secret

## Documentation
You may read [CHECKLIST](./docs/CHECKLIST.md) to have a list of implemented checks.
