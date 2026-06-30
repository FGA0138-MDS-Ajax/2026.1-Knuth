from datetime import datetime
from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.turma_model import Turma
    from app.models.aluno_model import Aluno
    from app.models.resposta_model import Resposta

class Pergunta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    texto: str = Field(min_length=5, max_length=500)
    data_criacao: datetime = Field(default_factory=datetime.now)
    turma_id: int = Field(foreign_key="turma.id", nullable=False,index=True,ondelete="RESTRICT")
    turma: "Turma" = Relationship(back_populates="perguntas")
    aluno_id: int = Field(foreign_key="aluno.id", nullable=False,index=True,ondelete="RESTRICT")
    aluno: "Aluno" = Relationship(back_populates="perguntas")
    respostas: list["Resposta"] = Relationship(back_populates="pergunta")
    is_restrita_professor: bool = Field(default=False)
    is_restrita_monitor: bool = Field(default=False)
    status: str = Field(default="aberta")
    prioridade: str = Field(default="media")


    