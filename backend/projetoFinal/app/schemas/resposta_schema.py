from datetime import datetime
from sqlmodel import SQLModel, Field


class UsuarioPublico(SQLModel):
    id: int
    username: str
    is_aluno: bool
    is_professor: bool
    is_admin: bool


class RespostaCreate(SQLModel):
    texto: str = Field(min_length=5, max_length=500)
    pergunta_id: int


class RespostaRead(SQLModel):
    id: int
    texto: str
    data_criacao: datetime
    pergunta_id: int
    usuario: UsuarioPublico


class RespostaUpdate(SQLModel):
    texto: str = Field(min_length=5, max_length=500)
