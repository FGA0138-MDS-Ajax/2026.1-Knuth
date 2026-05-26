from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:  
    from app.models.curso_model import Curso    


class Aluno(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True, min_length=2, max_length=100)
    email: str = Field(index=True, min_length=5, max_length=100, unique=True)
    matricula: str = Field(index=True, min_length=8, max_length=10, unique=True)
    curso_id: int = Field(foreign_key="curso.id", ondelete="RESTRICT")
    curso: "Curso" = Relationship(back_populates="alunos")