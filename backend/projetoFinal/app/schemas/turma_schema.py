from sqlmodel import SQLModel, Field
from app.models.aluno_model import Aluno
from app.models.professor_model import Professor
from app.models.disciplina_model import Disciplina
from app.models.turma_model import Turma

class TurmaCreate(SQLModel):
    descricao: str = Field(index=True, min_length=1, max_length=50, unique=True)
    horario: str = Field(min_length=3, max_length=20)
    periodo: str = Field(index=True, min_length=6, max_length=7)
    disciplina_id: int = Field(foreign_key="disciplina.id", nullable=False)
    professor_id: int = Field(foreign_key="professor.id", nullable=False)


class TurmaRead(SQLModel):
    id: int
    descricao: str
    horario: str
    periodo: str
    disciplina: Disciplina
    professor: Professor

class TurmaUpdate(SQLModel):
    descricao: str = Field(index=True, min_length=1, max_length=50, unique=True)
    horario: str = Field(min_length=3, max_length=20)
    periodo: str = Field(index=True, min_length=6, max_length=7)
    disciplina_id: int = Field(foreign_key="disciplina.id", nullable=False)
    professor_id: int = Field(foreign_key="professor.id", nullable=False)

class TurmaCompleta(SQLModel):
    id: int
    descricao: str
    horario: str
    periodo: str
    disciplina: Disciplina
    professor: Professor
    alunosMatriculados: list["Aluno"] = []
    alunosMonitores: list["Aluno"] = []