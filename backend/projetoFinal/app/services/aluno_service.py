from app.crud.aluno_crud import AlunoCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.turma_model import Turma

class AlunoService:
    
    @staticmethod
    def create(session, aluno_create):
        try:
            return AlunoCRUD.create(session, aluno_create)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Aluno com esse email ou matrícula já existe")
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Curso associado não encontrado")
            raise
    
    @staticmethod
    def update(session, aluno_id, aluno_update):
        try:
            aluno = AlunoCRUD.update(session, aluno_id, aluno_update)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Aluno com esse email ou matrícula já existe")
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Curso associado não encontrado")
            raise
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno
    
    @staticmethod
    def delete(session, aluno_id):
        if not AlunoCRUD.get_by_id(session, aluno_id):
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        try:
            AlunoCRUD.delete(session, aluno_id)
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409, detail="Aluno está matriculado em uma ou mais turmas" )
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
    
    @staticmethod
    def inclui_aluno_na_turma(session, aluno_id, turma_id):
        aluno = AlunoCRUD.get_by_id(session, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        turma = session.get(Turma, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        if turma in aluno.turmasMatriculadas:
            raise HTTPException(status_code=400, detail="Aluno já matriculado nessa turma")
        return AlunoCRUD.inclui_turma(session, aluno, turma)
    
    @staticmethod
    def remove_aluno_da_turma(session, aluno_id, turma_id):
        aluno = AlunoCRUD.get_by_id(session, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        turma = session.get(Turma, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        if turma not in aluno.turmasMatriculadas:
            raise HTTPException(status_code=400, detail="Aluno não matriculado nessa turma")
        return AlunoCRUD.remove_turma(session, aluno, turma)