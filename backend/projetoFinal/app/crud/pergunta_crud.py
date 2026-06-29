from sqlmodel import Session, select
from app.models.aluno_model import Aluno
from app.models.turma_model import Turma
from app.schemas.pergunta_schema import PerguntaCreate, PerguntaRead, PerguntaUpdate
from app.models.pergunta_model import Pergunta
from app.models.disciplina_model import Disciplina
from app.crud.aluno_crud import AlunoCRUD
from typing import Optional

class PerguntaCRUD:
    
    @staticmethod
    def create(session: Session, pergunta_create: PerguntaCreate, aluno_id: int) -> Pergunta:
        PerguntaCreate.model_validate(pergunta_create)
        pergunta = Pergunta(
            texto=pergunta_create.texto,
            turma_id=pergunta_create.turma_id,
            aluno_id=aluno_id,
            is_restrita_professor=pergunta_create.is_restrita_professor,
            is_restrita_monitor=pergunta_create.is_restrita_monitor,
            prioridade=pergunta_create.prioridade,
            status="aberta",
        )
        session.add(pergunta)
        session.commit()
        session.refresh(pergunta)
        return pergunta

    @staticmethod
    def update(session: Session, pergunta_id: int, pergunta_update: PerguntaUpdate) -> Optional[Pergunta]:
        PerguntaUpdate.model_validate(pergunta_update)
        pergunta = session.get(Pergunta, pergunta_id)
        if not pergunta:
            return None
        
        if pergunta_update.texto is not None:
            pergunta.texto = pergunta_update.texto
        if pergunta_update.is_restrita_professor is not None:
            pergunta.is_restrita_professor = pergunta_update.is_restrita_professor
        if pergunta_update.is_restrita_monitor is not None:
            pergunta.is_restrita_monitor = pergunta_update.is_restrita_monitor
        if pergunta_update.status is not None:
            pergunta.status = pergunta_update.status
        if pergunta_update.prioridade is not None:
            pergunta.prioridade = pergunta_update.prioridade

        session.add(pergunta)
        session.commit()
        session.refresh(pergunta)
        return pergunta

    @staticmethod
    def delete(session: Session, pergunta_id: int) -> bool:
        pergunta = session.get(Pergunta, pergunta_id)
        if not pergunta:
            return False
        session.delete(pergunta)
        session.commit()
        return True

    @staticmethod
    def get_by_id(session: Session, pergunta_id: int) -> Optional[Pergunta]:
        return session.get(Pergunta, pergunta_id)

    @staticmethod
    def get_by_turma(session: Session, turma_id: int) -> list[Pergunta]:
        statement = select(Pergunta).where(Pergunta.turma_id == turma_id)
        return list(session.exec(statement).all())

    @staticmethod
    def get_all(session: Session) -> list[Pergunta]:
        statement = select(Pergunta)
        return list(session.exec(statement).all())
