from app.crud.resposta_crud import RespostaCRUD
from app.crud.usuario_crud import UsuarioCRUD
from app.crud.pergunta_crud import PerguntaCRUD
from app.crud.aluno_crud import AlunoCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class RespostaService:
    
    @staticmethod
    def create(session, resposta_create,username):
        try:
            return RespostaCRUD.create(session, resposta_create, username)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Pergunta ou usuário associado não encontrado")
            raise 
    
    @staticmethod
    def update(session, resposta_id, resposta_update):
        try:
            resposta = RespostaCRUD.update(session, resposta_id, resposta_update)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Pergunta ou usuário associado não encontrado")
            raise
        if not resposta:
            raise HTTPException(status_code=404, detail="Resposta não encontrada")
        return resposta
    
    @staticmethod
    def delete(session, resposta_id):
        if not RespostaCRUD.get_by_id(session, resposta_id):
            raise HTTPException(status_code=404, detail="Resposta não encontrada")
        RespostaCRUD.delete(session, resposta_id)
        return {"detail": "Resposta deletada com sucesso"}
    
    @staticmethod
    def get_by_id(session, resposta_id):
        resposta = RespostaCRUD.get_by_id(session, resposta_id)
        if not resposta:
            raise HTTPException(status_code=404, detail="Resposta não encontrada")
        return resposta
    
    @staticmethod
    def get_all(session):
        return RespostaCRUD.get_all(session)