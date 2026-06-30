from app.crud.resposta_crud import RespostaCRUD
from app.crud.usuario_crud import UsuarioCRUD
from app.crud.pergunta_crud import PerguntaCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class RespostaService:

    @staticmethod
    def create(session, resposta_create, username: str):
        try:
            return RespostaCRUD.create(session, resposta_create, username)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Pergunta ou usuário associado não encontrado")
            raise

    @staticmethod
    def update(session, resposta_id: int, resposta_update, username: str):
        resposta = RespostaCRUD.get_by_id(session, resposta_id)
        if not resposta:
            raise HTTPException(status_code=404, detail="Resposta não encontrada")
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario or resposta.usuario_id != usuario.id:
            raise HTTPException(status_code=403, detail="Você não tem permissão para editar esta resposta")
        try:
            return RespostaCRUD.update(session, resposta_id, resposta_update)
        except IntegrityError as exc:
            session.rollback()
            raise HTTPException(status_code=409, detail="Erro ao atualizar resposta")

    @staticmethod
    def delete(session, resposta_id: int, username: str):
        resposta = RespostaCRUD.get_by_id(session, resposta_id)
        if not resposta:
            raise HTTPException(status_code=404, detail="Resposta não encontrada")
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario or resposta.usuario_id != usuario.id:
            raise HTTPException(status_code=403, detail="Você não tem permissão para deletar esta resposta")
        RespostaCRUD.delete(session, resposta_id)
        return {"detail": "Resposta deletada com sucesso"}

    @staticmethod
    def get_by_id(session, resposta_id: int):
        resposta = RespostaCRUD.get_by_id(session, resposta_id)
        if not resposta:
            raise HTTPException(status_code=404, detail="Resposta não encontrada")
        return resposta

    @staticmethod
    def get_by_pergunta(session, pergunta_id: int):
        if not PerguntaCRUD.get_by_id(session, pergunta_id):
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
        return RespostaCRUD.get_by_pergunta(session, pergunta_id)

    @staticmethod
    def get_all(session):
        return RespostaCRUD.get_all(session)
