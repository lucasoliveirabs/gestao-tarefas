from flask import Blueprint

tarefas = Blueprint('tarefas', __name__)

@tarefas.route('/')
def home():
    return 'Hello, Flask!'