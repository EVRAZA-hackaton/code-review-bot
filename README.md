# Code Review TG Bot

## Dev environment

### Before the very first use

* If you have cloned the existing repo (not generated the repo yourself):
    ```
    pip install pipenv
    export PIPENV_VENV_IN_PROJECT=1 && pipenv install --dev --python 3.11 && pipenv shell
    pre-commit install
    ```
* In IDE, do not forget to select the environment from `.venv`

### Running linters

`flake8`
