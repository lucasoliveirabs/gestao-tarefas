import pytest, os
from flask import Flask
from flask_migrate import Migrate
from api.routes.routes import tarefas as tarefas_blueprint
from api.models.models import postgres_db
from dotenv import load_dotenv

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(tarefas_blueprint)  
    load_dotenv()
        
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    postgres_db.init_app(app)
    Migrate().init_app(app, postgres_db)

    with app.app_context():
        postgres_db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        postgres_db.drop_all()  
        
def test_criar_tarefa(client):
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste 1", "descricao": "Descricao Teste 1"})
    assert response.status_code == 201
    assert response.json["titulo"] == "Titulo Teste 1"
    assert response.json["descricao"] == "Descricao Teste 1"
    
def test_criar_tarefa_sem_campo_titulo(client):
    response = client.post('/tarefas', json = {"descricao": "Descricao Teste 1"})
    assert response.status_code == 400
    assert response.json == {"error": "Título e descrição são obrigatórios"}
    
def test_criar_tarefa_titulo_vazio(client):
    response = client.post('/tarefas', json = {"titulo": "","descricao": "Descricao Teste 1"})
    assert response.status_code == 400
    assert response.json == {"error": "Título e descrição são obrigatórios"}
    
def test_criar_tarefa_sem_campo_descricao(client):
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste 1"})
    assert response.status_code == 400
    assert response.json == {"error": "Título e descrição são obrigatórios"}
    
def test_criar_tarefa_descricao_vazio(client):
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste 1","descricao": ""})
    assert response.status_code == 400
    assert response.json == {"error": "Título e descrição são obrigatórios"}
    
def test_listar_tarefas(client):
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste lista", "descricao": "Descricao Teste lista"})
    response = client.get('/tarefas')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    for tarefa in response.json:
        assert 'titulo' in tarefa
        assert 'descricao' in tarefa

def test_listar_tarefas_incompletas(client):
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste lista 1", "descricao": "Descricao Teste lista 1"})
    tarefa_id_1 = response.get_json()["id"]
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste lista 2", "descricao": "Descricao Teste lista 2"})
    tarefa_id_2 = response.get_json()["id"]
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste lista 3", "descricao": "Descricao Teste lista 3"})

    client.patch('/tarefas', json = {"id": tarefa_id_1, "concluida": True})
    client.patch('/tarefas', json = {"id": tarefa_id_2, "concluida": True})

    response = client.get('/tarefas?status=incompletas')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    for tarefa in response.json:
        assert 'titulo' in tarefa
        assert 'descricao' in tarefa
        assert tarefa.get('concluida') == False
        
def test_listar_tarefas_banco_vazio(client):
    response = client.get('/tarefas')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.get_json() == []
        
def test_alterar_tarefa(client):
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste 1", "descricao": "Descricao Teste 1"})
    tarefa_id_1 = response.get_json()["id"]
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste 2", "descricao": "Descricao Teste 2"})
    tarefa_id_2 = response.get_json()["id"]
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste 3", "descricao": "Descricao Teste 3"})
    tarefa_id_3 = response.get_json()["id"]

    response = client.patch('/tarefas', json = {"id": tarefa_id_1, "titulo": "Titulo Teste 1 - Atualizado", "concluida": True})
    assert response.status_code == 200
    assert response.get_json()['titulo'] == "Titulo Teste 1 - Atualizado"
    assert response.get_json()['concluida'] == True
    assert response.get_json()["momento_conclusao"] is not None

    response = client.patch('/tarefas', json = {"id": tarefa_id_2, "descricao": "Descricao Teste 2 - Atualizado", "concluida": True})
    assert response.status_code == 200
    assert response.get_json()['descricao'] == "Descricao Teste 2 - Atualizado"
    assert response.get_json()['concluida'] == True
    assert response.get_json()["momento_conclusao"] is not None
    
    response = client.patch('/tarefas', json = {"id": tarefa_id_3})
    assert response.status_code == 200
    assert response.get_json()['concluida'] == False
    assert response.get_json()["momento_conclusao"] is None
    
def test_reabrir_tarefa(client):
    response = client.post('/tarefas', json = {"titulo": "Titulo Teste 1", "descricao": "Descricao Teste 1"})
    tarefa_id_1 = response.get_json()["id"]

    response = client.patch('/tarefas', json={"id": tarefa_id_1, "concluida": True})
    assert response.status_code == 200
    assert response.get_json()["concluida"] is True
    assert response.get_json()["momento_conclusao"] is not None

    response = client.patch('/tarefas', json={"id": tarefa_id_1, "concluida": False})
    assert response.status_code == 200
    assert response.get_json()["concluida"] is False
    assert response.get_json()["momento_conclusao"] is None
    
def test_excluir_tarefa(client):
    nova_tarefa = {
        "titulo": "Tarefa para Deletar",
        "descricao": "Descrição da Tarefa para Deletar"
    }
    response = client.post('/tarefas', json=nova_tarefa)
    assert response.status_code == 201
    tarefa_id = response.json['id']  
    
    response = client.delete('/tarefas', json={"id": tarefa_id})
    assert response.status_code == 200 
    assert response.json['id'] == tarefa_id  

    response = client.get('/tarefas')
    tasks = response.get_json()
    assert not any(task["id"] == tarefa_id for task in tasks)