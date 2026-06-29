from datetime import datetime
from typing import Literal
from sqlmodel import SQLModel, Field


class PerguntaCreate(SQLModel):
    texto: str = Field(min_length=5, max_length=500)
    turma_id: int
    is_restrita_professor: bool = False
    is_restrita_monitor: bool = False
    prioridade: Literal["baixa", "media", "alta"] = "media"


class PerguntaRead(SQLModel):
    id: int
    texto: str
    data_criacao: datetime
    turma_id: int
    aluno_id: int
    is_restrita_professor: bool
    is_restrita_monitor: bool
    status: Literal["aberta", "em andamento", "resolvida"]
    prioridade: Literal["baixa", "media", "alta"]


class PerguntaUpdate(SQLModel):
    texto: str | None = None
    is_restrita_professor: bool | None = None
    is_restrita_monitor: bool | None = None
    status: Literal["aberta", "em andamento", "resolvida"] | None = None
    prioridade: Literal["baixa", "media", "alta"] | None = None
