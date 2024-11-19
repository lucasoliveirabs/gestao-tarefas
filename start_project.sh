#!/bin/bash

echo "Inicializando o projeto..."
docker-compose build
docker-compose up -d
docker-compose run tests

docker-compose ps
echo "Projeto iniciado! Acesse https://localhost:443/swagger/"