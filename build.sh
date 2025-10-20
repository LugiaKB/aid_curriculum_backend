#!/bin/bash

# exit on error
set -o errexit

# Instala as dependências do Pipfile diretamente no ambiente do sistema
pip install pipenv
pipenv install --system --deploy