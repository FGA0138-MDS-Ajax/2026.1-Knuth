from sqlmodel import Session, select
from app.models.professor_model import Professor
from app.schemas.professor_schema import ProfessorCreate, ProfessorRead, ProfessorUpdate
from typing import Optional

class ProfessorCRUD:
    
    @staticmethod
    def create(session: Session, professor_create: ProfessorCreate):
        professor = Professor.model_validate(professor_create)
        session.add(professor)
        session.commit()
        session.refresh(professor)
        return professor
    
    @staticmethod
    def update(session: Session, professor_id: int, professor_update: ProfessorUpdate):
        ProfessorUpdate.model_validate(professor_update)
        professor = session.get(Professor, professor_id)
        if not professor:
            return None
        professor.nome = professor_update.nome
        professor.email = professor_update.email
        session.add(professor)
        session.commit()
        session.refresh(professor)
        return professor
    
    @staticmethod
    def delete(session: Session, professor_id: int):
        professor = session.get(Professor, professor_id)
        if not professor:
            return None
        session.delete(professor)
        session.commit()

    @staticmethod
    def get_by_id(session: Session, professor_id: int):
        return session.get(Professor, professor_id)
    
    @staticmethod
    def get_all(session: Session):
        statement = select(Professor)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_parametros(session: Session, nome: Optional[str] = None):
        statement = select(Professor)
        if nome:
            statement = statement.where(Professor.nome.ilike(f"%{nome}%"))  
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_email(session: Session, email: str):
        statement = select(Professor).where(Professor.email == email)
        return session.exec(statement).first()