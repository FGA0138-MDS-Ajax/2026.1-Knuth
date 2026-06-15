from datetime import datetime
from sqlmodel import SQLModel, Field
from app.models.aluno_model import Aluno
from app.models.pergunta_model import Pergunta
from app.models.disciplina_model import Disciplina
from app.models.resposta_model import Resposta
from app.models.turma_model import Turma

class PerguntaCreate(SQLModel):
    texto: str = Field(min_length=5, max_length=500)
    turma_id: int = Field(foreign_key="turma.id", nullable=False,index=True,ondelete="RESTRICT")
    is_restrita_professor: bool = Field(default=False)
    is_restrita_monitor: bool = Field(default=False)

class PerguntaRead(SQLModel):
    id: int
    texto: str
    data_criacao: datetime
    turma: Turma
    aluno: Aluno
    is_restrita_professor: bool
    is_restrita_monitor: bool

class PerguntaUpdate(SQLModel):
    texto: str = Field(min_length=5, max_length=500)
    is_restrita_professor: bool = Field(default=False)
    is_restrita_monitor: bool = Field(default=False)

class PerguntaCompleta(SQLModel):
    id: int
    texto: str
    data_criacao: datetime
    turma: Turma
    aluno: Aluno
    respostas: list["Resposta"] = []
    is_restrita_professor: bool
    is_restrita_monitor: bool