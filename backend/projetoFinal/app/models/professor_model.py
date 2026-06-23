from sqlmodel import Relationship, SQLModel, Field
from app.models.turma_model import Turma

class Professor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True, min_length=2, max_length=50)
    email: str = Field(index=True, min_length=5, max_length=50, unique=True)
    turmas: list["Turma"] = Relationship(back_populates="professor", passive_deletes=True)