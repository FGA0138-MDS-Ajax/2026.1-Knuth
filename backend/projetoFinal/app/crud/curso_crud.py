from sqlmodel import Session, select
from app.models.curso_model import Curso
from app.schemas.curso_schema import CursoCreate, CursoRead, CursoUpdate

from typing import Optional

class CursoCRUD:
    
    @staticmethod
    def create(session: Session, curso_create: CursoCreate):
        curso = Curso.model_validate(curso_create)
        session.add(curso)
        session.commit()
        session.refresh(curso)
        return curso
    
    @staticmethod
    def update(session: Session, curso_id: int, curso_update: CursoUpdate):
        CursoUpdate.model_validate(curso_update)
        curso = session.get(Curso, curso_id)
        if not curso:
            return None
        curso.nome = curso_update.nome
        session.add(curso)
        session.commit()
        session.refresh(curso)
        return curso
    
    @staticmethod
    def delete(session: Session, curso_id: int):
        curso = session.get(Curso, curso_id)
        if not curso:
            return None
        session.delete(curso)
        session.commit()

    @staticmethod
    def get_by_id(session: Session, curso_id: int):
        return session.get(Curso, curso_id)
    
    @staticmethod
    def get_all(session: Session):
        statement = select(Curso)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_parametros(session: Session, nome: Optional[str] = None):
        statement = select(Curso)
        if nome:
            statement = statement.where(Curso.nome.ilike(f"%{nome}%"))  
        return session.exec(statement).all()