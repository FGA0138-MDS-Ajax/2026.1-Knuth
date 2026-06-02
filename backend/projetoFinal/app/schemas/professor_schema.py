from sqlmodel import SQLModel, Field
from app.models.turma_model import Turma

class ProfessorCreate(SQLModel):
    nome: str = Field(index=True, min_length=2, max_length=50, unique=True)
    email: str = Field(index=True, min_length=5, max_length=50, unique=True)

class ProfessorRead(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True, min_length=2, max_length=50, unique=True)
    email: str = Field(index=True, min_length=5, max_length=50, unique=True)
    turmas: list["Turma"] = Field(default=None)

class ProfessorUpdate(SQLModel):
    nome: str = Field(index=True, min_length=2, max_length=50, unique=True)
    email: str = Field(index=True, min_length=5, max_length=50, unique=True)