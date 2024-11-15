from flask import Flask
from flask_migrate import Migrate
from .db import postgres_db
from api.routes.routes import tarefas as tarefas_blueprint
from dotenv import load_dotenv
import os 

migrate = Migrate()

def create_app():        
    app = Flask(__name__)
    configure_app(app)
    initialize_postgres(app)    
    
    migrate.init_app(app, postgres_db)
    app.register_blueprint(tarefas_blueprint)
    
    with app.app_context():
        postgres_db.create_all()
    return app

def configure_app(_app):    
    _app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    
def initialize_postgres(_app):
    postgres_db.init_app(_app)

if __name__ == '__main__':
    app = create_app()
    app.run()
    