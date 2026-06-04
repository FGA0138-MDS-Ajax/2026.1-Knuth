from app.crud.disciplina_crud import DisciplinaCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class DisciplinaService:

    @staticmethod
    def create(session, disciplina_create):
        try:
            return DisciplinaCRUD.create(session, disciplina_create)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Disciplina com esse nome já existe")
            raise
        
    @staticmethod
    def update(session, disciplina_id, disciplina_update):
        try:
            disciplina = DisciplinaCRUD.update(session, disciplina_id, disciplina_update)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Disciplina com esse nome já existe")
            raise
        if not disciplina:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        return disciplina
    
    @staticmethod
    def delete(session, disciplina_id):
        if not DisciplinaCRUD.get_by_id(session, disciplina_id):
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        try:
            DisciplinaCRUD.delete(session, disciplina_id)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=400, detail="Não é possível deletar a disciplina porque existem turmas associadas a ela")
            raise
        return {"detail": "Disciplina deletada com sucesso"}
    
    @staticmethod
    def get_by_id(session, disciplina_id):
        disciplina = DisciplinaCRUD.get_by_id(session, disciplina_id)
        if not disciplina:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        return disciplina
    
    @staticmethod
    def get_all(session):
        return DisciplinaCRUD.get_all(session)
    
    @staticmethod
    def get_by_parametros(session, nome=None, codigo=None):
        return DisciplinaCRUD.get_by_parametros(session, nome, codigo)