from sqlmodel import Session, select
from app.models.aluno_model import Aluno
from app.models.turma_model import Turma
from app.schemas.turma_schema import TurmaCreate, TurmaRead, TurmaUpdate
from app.models.professor_model import Professor
from app.models.disciplina_model import Disciplina
from typing import Optional

class TurmaCRUD:
    
    @staticmethod
    def create(session: Session, turma_create: TurmaCreate):
        turma = Turma.model_validate(turma_create)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def update(session: Session, turma_id: int, turma_update: TurmaUpdate):
        TurmaUpdate.model_validate(turma_update)
        turma = session.get(Turma, turma_id)
        if not turma:
            return None
        turma.descricao = turma_update.descricao
        turma.horario = turma_update.horario
        turma.periodo = turma_update.periodo
        turma.disciplina_id = turma_update.disciplina_id
        turma.professor_id = turma_update.professor_id
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def delete(session: Session, turma_id: int):
        turma = session.get(Turma, turma_id)
        if not turma:
            return None
        session.delete(turma)
        session.commit()

    @staticmethod
    def get_by_id(session: Session, turma_id: int):
        return session.get(Turma, turma_id)
    
    @staticmethod
    def get_all(session: Session):
        statement = select(Turma)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_parametros(session: Session, descricao: Optional[str] = None, periodo: Optional[str] = None,nome_professor: Optional[str] = None, nome_disciplina: Optional[str] = None):
        statement = select(Turma)
        if descricao:
            statement = statement.where(Turma.descricao.ilike(f"%{descricao}%"))  
        if periodo:
            statement = statement.where(Turma.periodo.ilike(f"%{periodo}%"))
        if nome_professor:
            statement = statement.join(Professor).where(Professor.nome.ilike(f"%{nome_professor}%"))
        if nome_disciplina:
            statement = statement.join(Disciplina).where(Disciplina.nome.ilike(f"%{nome_disciplina}%"))
        return session.exec(statement).all()
    
    @staticmethod
    def inclui_aluno(session: Session, aluno: Aluno, turma: Turma):
        turma.alunosMatriculados.append(aluno)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def remove_aluno(session: Session, aluno: Aluno, turma: Turma):
        turma.alunosMatriculados.remove(aluno)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def inclui_monitor(session: Session, aluno: Aluno, turma: Turma):
        turma.alunosMonitores.append(aluno)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def remove_monitor(session: Session, aluno: Aluno, turma: Turma):
        turma.alunosMonitores.remove(aluno)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
        