from app.crud.aluno_crud import AlunoCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class AlunoService:
    
    @staticmethod
    def create(session, aluno_create):
        try:
            return AlunoCRUD.create(session, aluno_create)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Aluno com esse email ou matrícula já existe")
            raise
    
    @staticmethod
    def update(session, aluno_id, aluno_update):
        try:
            aluno = AlunoCRUD.update(session, aluno_id, aluno_update)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Aluno com esse email ou matrícula já existe")
            raise
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno
    
    @staticmethod
    def delete(session, aluno_id):
        if not AlunoCRUD.get_by_id(session, aluno_id):
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        AlunoCRUD.delete(session, aluno_id)
        return {"detail": "Aluno deletado com sucesso"}

    @staticmethod
    def get_by_id(session, aluno_id):
        aluno = AlunoCRUD.get_by_id(session, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno
    
    @staticmethod
    def get_all(session):
        return AlunoCRUD.get_all(session)
    
    @staticmethod
    def get_by_parametros(session, nome=None, email=None, matricula=None):
        return AlunoCRUD.get_by_parametros(session, nome, email, matricula)
    
    @staticmethod   
    def get_by_email(session, email):
        aluno = AlunoCRUD.get_by_email(session, email)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno