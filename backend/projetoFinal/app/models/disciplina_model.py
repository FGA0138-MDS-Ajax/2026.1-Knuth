from sqlmodel import Relationship, SQLModel, Field
from app.models.turma_model import Turma

class Disciplina(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True, min_length=5, max_length=50, unique=True)
    codigo: str = Field(index=True, min_length=5, max_length=10, unique=True)
    turmas: list["Turma"] = Relationship(back_populates="disciplina", passive_deletes=True)