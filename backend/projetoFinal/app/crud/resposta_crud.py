from sqlalchemy import text
from sqlmodel import Session, select
from starlette.exceptions import HTTPException
from app.schemas.resposta_schema import RespostaCreate, RespostaUpdate
from app.models.resposta_model import Resposta
from app.crud.usuario_crud import UsuarioCRUD
from app.crud.pergunta_crud import PerguntaCRUD
from app.crud.aluno_crud import AlunoCRUD


class RespostaCRUD:

    @staticmethod
    def create(session: Session, resposta_create: RespostaCreate, username: str):
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario:
            raise HTTPException(status_code=409, detail="Usuário associado não encontrado")

        usuario_id = usuario.id
        if usuario_id is None:
            raise HTTPException(status_code=409, detail="Usuário sem identificador válido")
        pergunta = PerguntaCRUD.get_by_id(session, resposta_create.pergunta_id)
        if not pergunta:
            raise HTTPException(status_code=409, detail="Pergunta associada não encontrada")
        if pergunta.is_restrita_professor and not usuario.is_professor:
            raise HTTPException(status_code=403, detail="Permissão negada para responder a esta pergunta")
        turma = pergunta.turma
        aluno = AlunoCRUD.get_by_email(session, username)
        if pergunta.is_restrita_monitor and aluno not in turma.alunosMonitores:
            raise HTTPException(status_code=403, detail="Permissão negada para responder a esta pergunta")

        RespostaCreate.model_validate(resposta_create)

        resposta = Resposta(
            texto=resposta_create.texto,
            pergunta_id=resposta_create.pergunta_id,
            usuario_id=usuario_id
        )

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
        statement = select(Resposta).order_by(text("data_criacao DESC"))
        return session.exec(statement).all()
