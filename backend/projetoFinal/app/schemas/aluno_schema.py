from sqlmodel import SQLModel, Field
from app.models.curso_model import Curso
from app.models.turma_model import Turma

class AlunoCreate(SQLModel):
    nome: str = Field(index=True, min_length=2, max_length=100)
    email: str = Field(index=True, min_length=5, max_length=100)
    matricula: str = Field(index=True, min_length=8, max_length=10)
    curso_id: int

class AlunoRead(SQLModel):
    id: int
    nome: str
    email: str
    matricula: str
    curso: Curso

class AlunoUpdate(SQLModel):
    nome: str = Field(index=True, min_length=2, max_length=100)
    email: str = Field(index=True, min_length=5, max_length=100)
    matricula: str = Field(index=True, min_length=8, max_length=10)
    curso_id: int

class AlunoCompleto(SQLModel):
    id: int
    nome: str
    email: str
    matricula: str
    curso: Curso
    turmasMatriculadas: list["Turma"] = []
    turmasMonitoradas: list["Turma"] = []