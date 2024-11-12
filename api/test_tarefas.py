import pytest, os
from flask import Flask
from flask_migrate import Migrate
from .routes import tarefas as tarefas_blueprint
from .models import postgres_db, Tarefa

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
        postgres_db.create_all()  # Cria as tabelas no banco de dados

    # Criando o cliente de teste
    with app.test_client() as client:
        yield client  # O cliente é fornecido para os testes

    # Limpeza do banco após os testes
    with app.app_context():
        postgres_db.drop_all()  # Remove as tabelas do banco de dados
            
        
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