from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from app.models.resposta_model import Resposta


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, min_length=5, max_length=100,unique=True) #utilizar o email do aluno ou professor como username
    hashed_password: str
    is_active: bool = Field(default=True)
    is_aluno: bool = Field(default=True)
    is_professor: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    respostas: list["Resposta"] = Relationship(back_populates="usuario")