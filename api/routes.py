from flask import Blueprint, jsonify, request

tarefas = Blueprint('tarefas', __name__)

mock_tarefas = []

@tarefas.route('/tarefas', methods=['POST'])
def criar_tarefa():
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    if not titulo or not descricao:
        return jsonify({"error": "Título e descrição são obrigatórios"}), 400

    nova_tarefa = {"titulo": titulo, "descricao": descricao}
    mock_tarefas.append(nova_tarefa)
    return jsonify(nova_tarefa), 201