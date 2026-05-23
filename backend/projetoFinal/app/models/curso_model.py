from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
if TYPE_CHECKING:
    from app.models.aluno_model import Aluno

class Curso(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True, min_length=5, max_length=50, unique=True)
    alunos: list["Aluno"] = Relationship(back_populates="curso", passive_deletes=True)