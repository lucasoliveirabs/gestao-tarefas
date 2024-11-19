from datetime import datetime, timezone, timedelta
from api.db import postgres_db
from uuid import uuid4

brt_timezone = timezone(timedelta(hours=-3))

class Tarefa(postgres_db.Model):
    __tablename__ = 'tarefas'
    
    uuid = postgres_db.Column(
        postgres_db.UUID(as_uuid=True), 
        primary_key=True, 
        unique=True, 
        nullable=False, 
        default=uuid4  
    )    
    titulo = postgres_db.Column(postgres_db.String(120), nullable=False)
    descricao = postgres_db.Column(postgres_db.String(255), nullable=False)
    concluida = postgres_db.Column(postgres_db.Boolean, default=False)
    momento_criacao = postgres_db.Column(postgres_db.DateTime, default=datetime.now(brt_timezone))
    momento_conclusao = postgres_db.Column(postgres_db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "uuid": str(self.uuid),
            "titulo": self.titulo,
            "descricao": self.descricao,
            "concluida": self.concluida,
            "momento_criacao": self.momento_criacao,
            "momento_conclusao": self.momento_conclusao
        }