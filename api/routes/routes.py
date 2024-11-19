from flask import request
from datetime import datetime, timezone, timedelta
from api.models.models import postgres_db, Tarefa
from flask_restx import Namespace, Resource, fields
from uuid import UUID

api = Namespace('tarefas', description='Operações para gestão de tarefas')
brt_timezone = timezone(timedelta(hours=-3))

tarefa_model = api.model('Tarefa', {
    'uuid': fields.String(description='UUID da tarefa', readonly=True),
    'titulo': fields.String(required=True, description='Título da tarefa'),
    'descricao': fields.String(required=True, description='Descrição da tarefa'),
    'concluida': fields.Boolean(description='Status da tarefa'),
    'momento_criacao': fields.DateTime(description='Data e hora de criação', readonly=True),
    'momento_conclusao': fields.DateTime(description='Data e hora de conclusão', readonly=True),
})

tarefa_update_model = api.model('AtualizarTarefa', {
    'descricao': fields.String(description='Nova descrição da tarefa'),
    'concluida': fields.Boolean(description='Status de conclusão da tarefa')
})

@api.errorhandler
def handle_restx_validation_error(error):
    """Trata erros de validação gerados pelo Flask-RESTx."""
    if "Input payload validation failed" in str(error):
        return {"message": "Dados inválidos ou incompletos.", "details": error.data.get("errors", {})}, 400

    return {"message": "Erro desconhecido.", "details": str(error)}, 400

@api.route('/', strict_slashes=False)
class Tarefas(Resource):
    @api.doc('criar_tarefa')
    @api.expect(tarefa_model, validate=True)
    @api.marshal_with(tarefa_model, code=201)
    def post(self):
        data = request.get_json()
        
        if not data:
            return {"message": "O corpo da requisição não pode estar vazio."}, 400
        if not data.get("titulo"):
            return {"message": "O campo 'título' é obrigatório."}, 400
        if not data.get("descricao"):
            return {"message": "O campo 'descrição' é obrigatório."}, 400

        nova_tarefa = Tarefa(titulo=data["titulo"], descricao=data["descricao"])
        postgres_db.session.add(nova_tarefa)
        postgres_db.session.commit()

        return nova_tarefa, 201


    @api.doc(
    'listar_tarefas',
    params={
        'status': {
            'description': "Filtrar tarefas por status ('incompletas' para não concluídas).",
            'type': 'string',
            'required': False
            }
        }
    )
    @api.marshal_list_with(tarefa_model)
    def get(self):
        status = request.args.get('status')
        query = postgres_db.session.query(Tarefa)

        if status and status not in ['incompletas']:
            return {"message": f"O valor '{status}' para o parâmetro 'status' não é válido."}, 400

        if status == 'incompletas':
            query = query.filter(Tarefa.concluida == False)

        tarefas = query.all()
        return tarefas, 200


@api.route('/<string:uuid>', strict_slashes=False)
class TarefaDetalhe(Resource):
    @api.expect(tarefa_update_model, validate=True)
    @api.marshal_with(tarefa_model)
    def patch(self, uuid):
        try:
            tarefa_uuid = UUID(uuid)
        except ValueError:
            return {"message": "O UUID fornecido é inválido."}, 400

        tarefa = postgres_db.session.query(Tarefa).filter_by(uuid=tarefa_uuid).first()
        if not tarefa:
            return {"message": "Tarefa não encontrada."}, 404

        data = request.get_json()
        if 'titulo' in data:
            tarefa.titulo = data['titulo']
        if 'descricao' in data:
            tarefa.descricao = data['descricao']
        if 'concluida' in data:
            tarefa.concluida = data['concluida']
            tarefa.momento_conclusao = datetime.now(brt_timezone) if tarefa.concluida else None

        postgres_db.session.commit()
        return tarefa, 200


    
    @api.response(204, 'Tarefa excluída')
    def delete(self, uuid):
        try:
            tarefa_uuid = UUID(uuid, version=4)
        except ValueError:
            return {"message": "O UUID fornecido é inválido."}, 400

        tarefa = postgres_db.session.query(Tarefa).filter_by(uuid=tarefa_uuid).first()
        if not tarefa:
            return {"message": "Tarefa não encontrada."}, 404

        postgres_db.session.delete(tarefa)
        postgres_db.session.commit()
        return '', 204
