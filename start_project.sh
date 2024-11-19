#!/bin/bash

export FLASK_ENV=development
export SQLALCHEMY_DATABASE_URI=postgresql://username:password@db/gestao_tarefas
export FLASK_APP=app.py
export HOST=0.0.0.0
export PORT=5000
export SSL_CERT_PATH=/app/api/ssl/server.crt
export SSL_KEY_PATH=/app/api/ssl/server.key

export API_KEY=$(openssl rand -base64 32)
echo "API Key gerada: $API_KEY"

echo "Inicializando o projeto..."
docker-compose build
docker-compose up -d
docker-compose run tests

docker-compose ps
echo "Projeto iniciado! Acesse https://localhost:443/swagger/"