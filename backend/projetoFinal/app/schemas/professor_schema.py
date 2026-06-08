from sqlmodel import SQLModel, Field
from app.models.turma_model import Turma


class ProfessorCreate(SQLModel):
    nome: str = Field(index=True, min_length=2, max_length=50)
    email: str = Field(index=True, min_length=5, max_length=50)


class ProfessorRead(SQLModel):
    id: int
    nome: str
    email: str
    turmas: list["Turma"] = []


class ProfessorUpdate(SQLModel):
    nome: str = Field(index=True, min_length=2, max_length=50)
    email: str = Field(index=True, min_length=5, max_length=50)

