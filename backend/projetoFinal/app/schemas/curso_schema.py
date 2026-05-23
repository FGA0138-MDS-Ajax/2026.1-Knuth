from sqlmodel import SQLModel, Field

from app.schemas.aluno_schema import AlunoCreate

class CursoCreate(SQLModel):
    nome: str = Field( min_length=5, max_length=50)

class CursoRead(SQLModel):
    id: int
    nome: str
    alunos: list[AlunoCreate] = []

class CursoUpdate(SQLModel):
    nome: str = Field( min_length=5, max_length=50)        