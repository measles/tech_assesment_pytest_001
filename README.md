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
