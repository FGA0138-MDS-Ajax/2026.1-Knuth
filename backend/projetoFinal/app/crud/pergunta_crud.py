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
    def create(session: Session, pergunta_create: PerguntaCreate, username: str):
        aluno = AlunoCRUD.get_by_email(session, username)
        if not aluno:
            raise ValueError("Aluno associado não encontrado")
        
        pergunta_create.model_validate(pergunta_create)    
        
        objPergunta = Pergunta(
            texto=pergunta_create.texto,
            turma_id=pergunta_create.turma_id,
            aluno_id=aluno.id,
            is_restrita_professor=pergunta_create.is_restrita_professor,
            is_restrita_monitor=pergunta_create.is_restrita_monitor,
        )
        session.add(objPergunta)
        session.commit()
        session.refresh(objPergunta)
        return objPergunta
    
    @staticmethod
    def update(session: Session, pergunta_id: int, pergunta_update: PerguntaUpdate):
        PerguntaUpdate.model_validate(pergunta_update)
        pergunta = session.get(Pergunta, pergunta_id)
        if not pergunta:
            return None
        pergunta.texto = pergunta_update.texto
        pergunta.is_restrita_professor = pergunta_update.is_restrita_professor
        pergunta.is_restrita_monitor = pergunta_update.is_restrita_monitor
        session.add(pergunta)
        session.commit()
        session.refresh(pergunta)
        return pergunta
    
    @staticmethod
    def delete(session: Session, pergunta_id: int):
        pergunta = session.get(Pergunta, pergunta_id)
        if not pergunta:
            return None
        session.delete(pergunta)
        session.commit()

    @staticmethod
    def get_by_id(session: Session, pergunta_id: int):
        return session.get(Pergunta, pergunta_id)
    
    @staticmethod
    def get_all(session: Session):
        statement = select(Pergunta)
        return session.exec(statement).all()