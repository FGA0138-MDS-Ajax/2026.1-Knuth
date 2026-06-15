from app.crud.professor_crud import ProfessorCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class ProfessorService:
    
    @staticmethod
    def create(session, professor_create):
        try:
            return ProfessorCRUD.create(session, professor_create)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Professor com esse email já existe")
            raise
    
    @staticmethod
    def update(session, professor_id, professor_update):
        try:
            professor = ProfessorCRUD.update(session, professor_id, professor_update)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Professor com esse email já existe")
            raise
        if not professor:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return professor
    
    @staticmethod
    def delete(session, professor_id):
        if not ProfessorCRUD.get_by_id(session, professor_id):
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        try:
            ProfessorCRUD.delete(session, professor_id)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=400, detail="Não é possível deletar o professor porque existem turmas associadas a ele")
            raise
        return {"detail": "Professor deletado com sucesso"}
    
    @staticmethod
    def get_by_id(session, professor_id):
        professor = ProfessorCRUD.get_by_id(session, professor_id)
        if not professor:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return professor
    
    @staticmethod
    def get_all(session):
        return ProfessorCRUD.get_all(session)
    
    @staticmethod
    def get_by_parametros(session, nome=None):
        return ProfessorCRUD.get_by_parametros(session, nome)
    
    @staticmethod
    def get_by_email(session, email):
        professor = ProfessorCRUD.get_by_email(session, email)
        if not professor:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return professor
    
