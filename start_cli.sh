#!/bin/bash
# Arquivo: start_cli.sh

docker-compose -p gestao-tarefas ps | grep -q "gestao-tarefas_db_1.*Up"
db_status=$?
docker-compose -p gestao-tarefas ps | grep -q "gestao-tarefas_web_1.*Up"
web_status=$?

if [ $db_status -ne 0 ] || [ $web_status -ne 0 ]; then
  echo "Iniciando os serviços principais db e web"
  docker-compose -p gestao-tarefas up -d
else
  echo "Serviços principais já estão em execução."
fi

echo "Efetivando mudanças de banco de dados com 'flask db upgrade'"
docker-compose exec web sh -c "cd api && flask db upgrade"
docker-compose -p gestao-tarefas run --entrypoint "" cli bash