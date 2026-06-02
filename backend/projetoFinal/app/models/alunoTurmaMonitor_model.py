from sqlmodel import SQLModel, Field

class AlunoTurmaMonitor(SQLModel, table=True):
    aluno_id: int = Field(foreign_key="aluno.id", primary_key=True, ondelete="RESTRICT")
    turma_id: int = Field(foreign_key="turma.id", primary_key=True, ondelete="RESTRICT")