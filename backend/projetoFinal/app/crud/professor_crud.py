from sqlmodel import Session, select
from app.models.professor_model import Professor
from app.schemas.professor_schema import ProfessorCreate, ProfessorUpdate
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
        professor = session.get(Professor, professor_id)
        if not professor:
            return None
        
        professor_data = professor_update.model_dump(exclude_unset=True)
        for key, value in professor_data.items():
            setattr(professor, key, value)
            
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
        return True

    @staticmethod
    def get_by_id(session: Session, professor_id: int):
        return session.get(Professor, professor_id)
    
    @staticmethod
    def get_all(session: Session):
        statement = select(Professor)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_email(session: Session, email: str):
        statement = select(Professor).where(Professor.email == email)
        result = session.exec(statement).first()
        return result
    
    @staticmethod
    def get_by_nome(session: Session, nome: str):
        statement = select(Professor).where(Professor.nome.ilike(f"%{nome}%"))
        return session.exec(statement).all()
