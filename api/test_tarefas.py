import pytest, os
from flask import Flask
from flask_migrate import Migrate
from .routes import tarefas as tarefas_blueprint
from .models import postgres_db

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(tarefas_blueprint)  
        
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URI')
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
    response = client.get('/tarefas')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    for tarefa in response.json:
        assert 'titulo' in tarefa
        assert 'descricao' in tarefa

def test_alterar_tarefa(client):
    nova_tarefa = {
        "titulo": "Titulo teste 0",
        "descricao": "Descrição teste 0"
    }
    response = client.post('/tarefas', json=nova_tarefa)
    assert response.status_code == 201
    tarefa_id = response.json['id']  
    
    dados_atualizados = {
        "id": tarefa_id,
        "titulo": "Titulo teste 1",
        "descricao": "Descrição teste 1"
    }
    response = client.patch('/tarefas', json=dados_atualizados)
    assert response.status_code == 200
    assert response.json['titulo'] == "Titulo teste 1"
    assert response.json['descricao'] == "Descrição teste 1"
    
    import pytest

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
