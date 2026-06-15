from app.core.security import get_current_username
from app.crud.aluno_crud import AlunoCRUD
from app.crud.turma_crud import TurmaCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.turma_model import Turma

class TurmaService:
    
    @staticmethod
    def create(session, turma_create):
        try:
            return TurmaCRUD.create(session, turma_create)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Turma com essa descrição ou código de acesso já existe")
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Professor ou disciplina associada não encontrada")
            raise
    
    @staticmethod
    def update(session, turma_id, turma_update):
        try:
            turma = TurmaCRUD.update(session, turma_id, turma_update)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Turma com essa descrição ou código de acesso já existe")
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Professor ou disciplina associada não encontrada")
            raise
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma
    
    @staticmethod
    def delete(session, turma_id):
        if not TurmaCRUD.get_by_id(session, turma_id):
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        TurmaCRUD.delete(session, turma_id)
        return {"detail": "Turma deletada com sucesso"}
    
    @staticmethod
    def get_by_id(session, turma_id):
        turma = TurmaCRUD.get_by_id(session, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma
    
    @staticmethod
    def get_all(session):
        return TurmaCRUD.get_all(session)
    
    @staticmethod
    def get_by_parametros(session, descricao=None, periodo=None,nome_professor=None, nome_disciplina=None):
        return TurmaCRUD.get_by_parametros(session, descricao, periodo,nome_professor,nome_disciplina)
    
    @staticmethod
    def inclui_turma_no_aluno(session, aluno_id, turma_id):
        aluno = AlunoCRUD.get_by_id(session, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        turma = session.get(Turma, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        if aluno in turma.alunosMatriculados:
            raise HTTPException(status_code=400, detail="Aluno já matriculado nessa turma")
        return TurmaCRUD.inclui_aluno(session, aluno, turma)
    
    @staticmethod
    def remove_turma_do_aluno(session, aluno_id, turma_id):
        aluno = AlunoCRUD.get_by_id(session, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        turma = session.get(Turma, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        if aluno not in turma.alunosMatriculados:
            raise HTTPException(status_code=400, detail="Aluno não matriculado nessa turma")
        return TurmaCRUD.remove_aluno(session, aluno, turma)
    
    @staticmethod
    def inclui_monitor_no_aluno(session, aluno_id, turma_id):
        aluno = AlunoCRUD.get_by_id(session, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        turma = session.get(Turma, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        if aluno in turma.alunosMonitores:
            raise HTTPException(status_code=400, detail="Aluno já monitor dessa turma")
        return TurmaCRUD.inclui_monitor(session, aluno, turma)
    
    @staticmethod
    def remove_monitor_do_aluno(session, aluno_id, turma_id):
        aluno = AlunoCRUD.get_by_id(session, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        turma = session.get(Turma, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        if aluno not in turma.alunosMonitores:
            raise HTTPException(status_code=400, detail="Aluno não monitor dessa turma")
        return TurmaCRUD.remove_monitor(session, aluno, turma)
    
    @staticmethod
    def inclui_aluno_codigo_acesso(session, codigo_acesso, username: str):
        aluno = AlunoCRUD.get_by_email(session, username)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

        turma = TurmaCRUD.get_by_codigo_acesso(session, codigo_acesso)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        if aluno in turma.alunosMatriculados:
            raise HTTPException(status_code=400, detail="Aluno já matriculado nessa turma")
        return TurmaCRUD.inclui_aluno(session, aluno, turma)
    

    @staticmethod
    def inclui_aluno_codigo_acesso_old(session, codigo_acesso, aluno_id):
        aluno = AlunoCRUD.get_by_id(session, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        turma = TurmaCRUD.get_by_codigo_acesso(session, codigo_acesso)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        if aluno in turma.alunosMatriculados:
            raise HTTPException(status_code=400, detail="Aluno já matriculado nessa turma")
        return TurmaCRUD.inclui_aluno(session, aluno, turma)
    
    @staticmethod
    def get_turmas_usuario(session, username):
        try:
            return TurmaCRUD.get_turmas_usuario(session, username)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        
    @staticmethod
    def is_usuario_monitor(session, username, turma_id):
        try:
            return TurmaCRUD.is_usuario_monitor(session, username, turma_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))   
        
    @staticmethod
    def is_usuario_matriculado(session, username, turma_id):
        try:
            return TurmaCRUD.is_usuario_matriculado(session, username, turma_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))