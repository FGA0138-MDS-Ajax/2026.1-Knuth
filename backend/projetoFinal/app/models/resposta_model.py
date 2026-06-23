from sqlmodel import Relationship, Relationship, SQLModel, Field
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.pergunta_model import Pergunta
    from app.models.usuario_model import Usuario

class Resposta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    texto: str = Field(min_length=5, max_length=500)
    data_criacao: datetime = Field(default_factory=datetime.now)
    usuario_id: int = Field(foreign_key="usuario.id", nullable=False, index=True, ondelete="RESTRICT")
    usuario: "Usuario" = Relationship()
    pergunta_id: int = Field(foreign_key="pergunta.id", nullable=False, index=True, ondelete="RESTRICT")
    pergunta: "Pergunta" = Relationship(back_populates="respostas")