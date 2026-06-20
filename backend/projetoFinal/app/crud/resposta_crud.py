from sqlmodel import Session, select
from app.schemas.resposta_schema import RespostaCreate, RespostaUpdate
from app.models.resposta_model import Resposta
from app.models.pergunta_model import Pergunta
from app.crud.usuario_crud import UsuarioCRUD


class RespostaCRUD:

    @staticmethod
    def create(session: Session, resposta_create: RespostaCreate, username: str):
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        RespostaCreate.model_validate(resposta_create)

        pergunta = session.get(Pergunta, resposta_create.pergunta_id)
        if not pergunta:
            raise ValueError("Pergunta não encontrada")

        resposta = Resposta(
            texto=resposta_create.texto,
            pergunta_id=resposta_create.pergunta_id,
            usuario_id=usuario.id
        )

        if pergunta.status == "aberta":
            pergunta.status = "em andamento"
            session.add(pergunta)

        session.add(resposta)
        session.commit()
        session.refresh(resposta)
        return resposta

    @staticmethod
    def update(session: Session, resposta_id: int, resposta_update: RespostaUpdate):
        RespostaUpdate.model_validate(resposta_update)

        resposta = session.get(Resposta, resposta_id)
        if not resposta:
            return None

        resposta.texto = resposta_update.texto

        session.add(resposta)
        session.commit()
        session.refresh(resposta)
        return resposta

    @staticmethod
    def delete(session: Session, resposta_id: int):
        resposta = session.get(Resposta, resposta_id)
        if not resposta:
            return None

        session.delete(resposta)
        session.commit()
        return resposta

    @staticmethod
    def get_by_id(session: Session, resposta_id: int):
        return session.get(Resposta, resposta_id)

    @staticmethod
    def get_all(session: Session):
        statement = select(Resposta).order_by(Resposta.data_criacao.desc)
        return session.exec(statement).all()
