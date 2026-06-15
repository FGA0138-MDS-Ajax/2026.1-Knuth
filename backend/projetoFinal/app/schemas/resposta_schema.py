from sqlmodel import SQLModel, Field
from app.models.resposta_model import Resposta
from app.models.usuario_model import Usuario
from app.models.pergunta_model import Pergunta
from datetime import datetime

class RespostaCreate(SQLModel):
    texto: str = Field(min_length=5, max_length=500)
    pergunta_id: int = Field(foreign_key="pergunta.id", nullable=False,index=True,ondelete="RESTRICT")

class RespostaRead(SQLModel):
    id: int
    texto: str
    data_criacao: datetime
    pergunta: Pergunta
    usuario: Usuario

class RespostaUpdate(SQLModel):
    texto: str = Field(min_length=5, max_length=500)
