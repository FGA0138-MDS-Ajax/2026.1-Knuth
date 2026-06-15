from app.crud.pergunta_crud import PerguntaCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class PerguntaService:
    
    @staticmethod
    def create(session, pergunta_create, username):
        try:
            return PerguntaCRUD.create(session, pergunta_create, username)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Aluno ou turma associada não encontrada")
            raise
    
    @staticmethod
    def update(session, pergunta_id, pergunta_update):
        try:
            pergunta = PerguntaCRUD.update(session, pergunta_id, pergunta_update)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Aluno ou turma associada não encontrada")
            raise
        if not pergunta:
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
        return pergunta
    
    @staticmethod
    def delete(session, pergunta_id):
        if not PerguntaCRUD.get_by_id(session, pergunta_id):
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
        PerguntaCRUD.delete(session, pergunta_id)
        return {"detail": "Pergunta deletada com sucesso"}
    
    @staticmethod
    def get_by_id(session, pergunta_id):
        pergunta = PerguntaCRUD.get_by_id(session, pergunta_id)
        if not pergunta:
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
        return pergunta
    
    @staticmethod
    def get_all(session):
        return PerguntaCRUD.get_all(session)