from sqlmodel import Session, select
from app.models.disciplina_model import Disciplina
from app.schemas.disciplina_schema import DisciplinaCreate, DisciplinaRead, DisciplinaUpdate
from typing import Optional

class DisciplinaCRUD:
    
    @staticmethod
    def create(session: Session, disciplina_create: DisciplinaCreate):
        disciplina = Disciplina.model_validate(disciplina_create)
        session.add(disciplina)
        session.commit()
        session.refresh(disciplina)
        return disciplina
    
    @staticmethod
    def update(session: Session, disciplina_id: int, disciplina_update: DisciplinaUpdate):
        DisciplinaUpdate.model_validate(disciplina_update)
        disciplina = session.get(Disciplina, disciplina_id)
        if not disciplina:
            return None
        disciplina.nome = disciplina_update.nome
        session.add(disciplina)
        session.commit()
        session.refresh(disciplina)
        return disciplina
    
    @staticmethod
    def delete(session: Session, disciplina_id: int):
        disciplina = session.get(Disciplina, disciplina_id)
        if not disciplina:
            return None
        session.delete(disciplina)
        session.commit()
    
    @staticmethod
    def get_by_id(session: Session, disciplina_id: int):
        return session.get(Disciplina, disciplina_id)
    
    @staticmethod
    def get_all(session: Session):
        statement = select(Disciplina)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_parametros(session: Session, nome: Optional[str] = None, codigo: Optional[str] = None):
        statement = select(Disciplina)
        if nome:
            statement = statement.where(Disciplina.nome.ilike(f"%{nome}%"))  # pyright: ignore[reportAttributeAccessIssue]
        if codigo:
            statement = statement.where(Disciplina.codigo.ilike(f"%{codigo}%"))  # pyright: ignore[reportAttributeAccessIssue]
        return session.exec(statement).all()