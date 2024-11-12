from datetime import datetime, timezone, timedelta
from .db import postgres_db
import uuid

brt_timezone = timezone(timedelta(hours=-3))

class Tarefa(postgres_db.Model):
    __tablename__ = 'tarefas'
    
    id = postgres_db.Column(postgres_db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = postgres_db.Column(postgres_db.String(120), nullable=False)
    descricao = postgres_db.Column(postgres_db.String(255), nullable=False)
    data_criacao = postgres_db.Column(postgres_db.DateTime, default=datetime.now(brt_timezone))
    data_exclusao = postgres_db.Column(postgres_db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "data_criacao": self.data_criacao,
            "data_exclusao": self.data_exclusao
        }
