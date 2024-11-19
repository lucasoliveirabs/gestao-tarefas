from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restx import Api
from api.db import postgres_db
from api.routes.routes import api as tarefas_namespace
import os

API_KEY = os.getenv("API_KEY", "my-secret-api-key")
migrate = Migrate()

def create_app():
    """Criação e configuração do Flask app."""
    app = Flask(__name__)
    configurar_app(app)
    inicializar_extensoes(app)
    configurar_swagger(app)
    registrar_namespaces(app)

    @app.before_request
    def validar_api_key():
        """Middleware para validar a API Key antes de processar requisições."""
        if request.path not in ["/swagger.json", "/swagger/"]:
            api_key = request.headers.get("X-API-KEY")
            if api_key != API_KEY:
                return jsonify({"message": "API Key inválida ou ausente"}), 401

    with app.app_context():
        postgres_db.create_all()

    return app


def configurar_app(_app):
    """Configuração básica do app."""
    _app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def inicializar_extensoes(_app):
    """Inicializa as extensões do Flask."""
    postgres_db.init_app(_app)
    migrate.init_app(_app, postgres_db)


def configurar_swagger(_app):
    """Configuração da documentação Swagger."""
    api = Api(
        _app,
        version='1.0',
        title='API Gestão de Tarefas',
        description='API para criar, listar, atualizar e excluir tarefas. Interação de usuário via CLI.',
        doc="/swagger/"
    )
    _app.api = api


def registrar_namespaces(_app):
    """Registro dos namespaces no app."""
    _app.api.add_namespace(tarefas_namespace, path='/tarefas')


if __name__ == '__main__':
    app = create_app()

    ssl_cert = os.getenv('SSL_CERT_PATH')
    ssl_key = os.getenv('SSL_KEY_PATH')
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))

    app.run(ssl_context=(ssl_cert, ssl_key), host=host, port=port)
