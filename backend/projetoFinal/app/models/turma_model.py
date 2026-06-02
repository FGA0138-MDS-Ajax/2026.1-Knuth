from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

from app.models.alunoTurmaMatriculado_model import AlunoTurmaMatriculado
from app.models.alunoTurmaMonitor_model import AlunoTurmaMonitor


if TYPE_CHECKING:
    from app.models.disciplina_model import Disciplina
    from app.models.professor_model import Professor
    from app.models.aluno_model import Aluno


class Turma(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descricao: str = Field(index=True, min_length=1, max_length=50)
    horario: str = Field(min_length=3, max_length=20)
    periodo: str = Field(index=True, min_length=6, max_length=7)
    disciplina_id: int = Field(foreign_key="disciplina.id", nullable=False)
    disciplina: "Disciplina" = Relationship(back_populates="turmas", passive_deletes=True)
    professor_id: int = Field(foreign_key="professor.id", nullable=False)
    professor: "Professor" = Relationship(back_populates="turmas", passive_deletes=True)
    alunosMatriculados: list["Aluno"] = Relationship(back_populates="turmasMatriculadas", link_model=AlunoTurmaMatriculado)
    alunosMonitores: list["Aluno"] = Relationship(back_populates="turmasMonitoradas", link_model=AlunoTurmaMonitor)