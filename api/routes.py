from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from .models import postgres_db, Tarefa

tarefas = Blueprint('tarefas', __name__)

@tarefas.route('/tarefas', methods=['POST'])
def criar_tarefa():
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    if not titulo or not descricao:
        return jsonify({"error": "Título e descrição são obrigatórios"}), 400

    nova_tarefa = Tarefa(titulo=titulo, descricao=descricao)
    postgres_db.session.add(nova_tarefa)
    postgres_db.session.commit()
    return jsonify(nova_tarefa.to_dict()), 201

@tarefas.route('/tarefas', methods=['GET'])
def listar_tarefas():
    data = postgres_db.session.query(Tarefa).all()
    return jsonify([tarefa.to_dict() for tarefa in data]), 200
    
@tarefas.route('/tarefas', methods=['PATCH'])
def alterar_tarefa():
    data = request.get_json()
    tarefa_id = data.get('id')
    tarefa = postgres_db.session.get(Tarefa, tarefa_id)  

    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404 
    
    if 'titulo' in data and data['titulo']:
        tarefa.titulo = data['titulo']
    if 'descricao' in data and data['descricao']:
        tarefa.descricao = data['descricao']
        
    postgres_db.session.commit()
    return jsonify(tarefa.to_dict()), 200