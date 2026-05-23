from sqlmodel import Session, select
from app.models.aluno_model import Aluno
from app.schemas.aluno_schema import AlunoCreate, AlunoRead, AlunoUpdate
from typing import Optional

class AlunoCRUD:
    
    @staticmethod
    def create(session: Session, aluno_create: AlunoCreate):
        aluno = Aluno.model_validate(aluno_create)
        session.add(aluno)
        session.commit()
        session.refresh(aluno)
        return aluno
    
    @staticmethod
    def update(session: Session, aluno_id: int, aluno_update: AlunoUpdate):
        AlunoUpdate.model_validate(aluno_update)
        aluno = session.get(Aluno, aluno_id)
        if not aluno:
            return None
        aluno.nome = aluno_update.nome
        aluno.email = aluno_update.email
        aluno.matricula = aluno_update.matricula
        session.add(aluno)
        session.commit()
        session.refresh(aluno)
        return aluno
    
    @staticmethod
    def delete(session: Session, aluno_id: int):
        aluno = session.get(Aluno, aluno_id)
        if not aluno:
            return None
        session.delete(aluno)
        session.commit()

    @staticmethod
    def get_by_id(session: Session, aluno_id: int):
        return session.get(Aluno, aluno_id)
    
    @staticmethod
    def get_all(session: Session):
        statement = select(Aluno)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_email(session: Session, email: str):
        statement = select(Aluno).where(Aluno.email == email)
        result = session.exec(statement).first()
        return result
    
    @staticmethod
    def get_by_parametros(session: Session, nome: Optional[str] = None, email: Optional[str] = None, matricula: Optional[str] = None):
        statement = select(Aluno)
        if nome:
            statement = statement.where(Aluno.nome.ilike(f"%{nome}%"))  
        if email:
            statement = statement.where(Aluno.email.ilike(f"%{email}%"))
        if matricula:
            statement = statement.where(Aluno.matricula.ilike(f"%{matricula}%"))
        return session.exec(statement).all()