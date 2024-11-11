from flask import Flask
from routes import tarefas as tarefas_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(tarefas_blueprint)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()