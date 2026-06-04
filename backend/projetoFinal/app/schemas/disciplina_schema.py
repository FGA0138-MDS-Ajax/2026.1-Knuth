from sqlmodel import SQLModel, Field
from app.models.turma_model import Turma

class DisciplinaCreate(SQLModel):
    nome: str = Field( min_length=5, max_length=50)
    codigo: str = Field( min_length=5, max_length=10)

class DisciplinaRead(SQLModel):
    id: int
    nome: str
    codigo: str
    turmas: list["Turma"] = Field(default=None)

class DisciplinaUpdate(SQLModel):
    nome: str = Field( min_length=5, max_length=50)
    codigo: str = Field( min_length=5, max_length=10)