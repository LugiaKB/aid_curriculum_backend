#!/usr/bin/env bash

# Aborta imediatamente se algum comando falhar
set -e

echo "--- 1. Instalando Pipenv globalmente ---"
# Instala o Pipenv no ambiente de build
pip install pipenv

echo "--- 2. Instalando dependências do Pipenv ---"
# Instala as dependências usando o Pipfile.lock (modo deploy)
# Garante que as dependências sejam as definidas no lock file
pipenv install --deploy

# Opcional: Limpa o cache do pip para economizar espaço
# pip cache purge

echo "--- Build concluído com sucesso! ---"