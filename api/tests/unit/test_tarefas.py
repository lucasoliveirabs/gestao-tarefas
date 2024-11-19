import pytest, os
from flask import Flask
from flask_migrate import Migrate
from api.models.models import postgres_db
from api.routes.routes import api as tarefas_namespace
from flask_restx import Api
from uuid import uuid4


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    postgres_db.init_app(app)
    Migrate(app, postgres_db)

    api = Api(app)
    api.add_namespace(tarefas_namespace, path="/tarefas")

    with app.app_context():
        postgres_db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        postgres_db.drop_all()


def test_criar_tarefa(client):
    response = client.post('/tarefas', json={"titulo": "Teste 1", "descricao": "Descrição Teste 1"})
    assert response.status_code == 201
    assert response.json["titulo"] == "Teste 1"
    assert response.json["descricao"] == "Descrição Teste 1"

def test_listar_tarefas(client):
    client.post('/tarefas', json={"titulo": "Teste 1", "descricao": "Descrição Teste 1"})
    response = client.get('/tarefas')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    for tarefa in response.json:
        assert "titulo" in tarefa
        assert "descricao" in tarefa


def test_listar_tarefas_incompletas(client):
    client.post('/tarefas', json={"titulo": "Tarefa 1", "descricao": "Descrição 1"})
    client.post('/tarefas', json={"titulo": "Tarefa 2", "descricao": "Descrição 2"})
    response = client.get('/tarefas?status=incompletas')
    assert response.status_code == 200
    assert len(response.json) == 2  


def test_alterar_tarefa(client):
    response = client.post('/tarefas', json={"titulo": "Teste Alteração", "descricao": "Descrição Alteração"})
    tarefa_uuid = response.json["uuid"]

    response = client.patch(f'/tarefas/{tarefa_uuid}', json={"titulo": "Título Alterado", "concluida": True})
    assert response.status_code == 200
    assert response.json["titulo"] == "Título Alterado"
    assert response.json["concluida"] is True
    assert response.json["momento_conclusao"] is not None


def test_alterar_tarefa_sem_concluir(client):
    response = client.post('/tarefas', json={"titulo": "Teste Alteração", "descricao": "Descrição Alteração"})
    tarefa_uuid = response.json["uuid"]

    response = client.patch(f'/tarefas/{tarefa_uuid}', json={"titulo": "Título Alterado"})
    assert response.status_code == 200
    assert response.json["titulo"] == "Título Alterado"
    assert response.json["concluida"] is False
    assert response.json["momento_conclusao"] is None


def test_excluir_tarefa(client):
    response = client.post('/tarefas', json={"titulo": "Tarefa Excluir", "descricao": "Descrição Excluir"})
    tarefa_uuid = response.json["uuid"]

    response = client.delete(f'/tarefas/{tarefa_uuid}')
    assert response.status_code == 204

    response = client.get('/tarefas')
    assert not any(tarefa["uuid"] == tarefa_uuid for tarefa in response.json)

def test_reabrir_tarefa(client):
    response = client.post('/tarefas', json={"titulo": "Teste Reabrir", "descricao": "Descrição Reabrir"})
    tarefa_uuid = response.json["uuid"]

    response = client.patch(f'/tarefas/{tarefa_uuid}', json={"concluida": True})
    assert response.status_code == 200
    assert response.json["concluida"] is True

    response = client.patch(f'/tarefas/{tarefa_uuid}', json={"concluida": False})
    assert response.status_code == 200
    assert response.json["concluida"] is False


def test_listar_tarefas_banco_vazio(client):
    response = client.get('/tarefas')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 0