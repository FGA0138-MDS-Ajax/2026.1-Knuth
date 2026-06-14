from app.crud.aluno_crud import AlunoCRUD
from app.crud.turma_crud import TurmaCRUD
from app.crud.usuario_crud import UsuarioCRUD
from app.crud.professor_crud import ProfessorCRUD
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
                raise HTTPException(status_code=409, detail="Turma com essa descrição já existe")
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
                raise HTTPException(status_code=409, detail="Turma com essa descrição já existe")
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
    def get_minhas_turmas(session, email, is_professor, is_aluno):
        if is_professor:
            return TurmaCRUD.get_by_professor_email(session, email)
        if is_aluno:
            return TurmaCRUD.get_by_aluno_email(session, email)
        return []

    @staticmethod
    def inscrever_aluno_por_email(session, email, turma_id):
        aluno = AlunoCRUD.get_by_email(session, email)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return TurmaService.inclui_turma_no_aluno(session, aluno.id, turma_id)

    @staticmethod
    def associar_usuario_por_id(session, usuario_id, turma_id):
        usuario = UsuarioCRUD.get_by_id(session, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        if usuario.is_professor:
            professor = ProfessorCRUD.get_by_email(session, usuario.username)
            if not professor:
                raise HTTPException(status_code=404, detail="Professor não encontrado para este usuário")
            
            turma = session.get(Turma, turma_id)
            if not turma:
                raise HTTPException(status_code=404, detail="Turma não encontrada")
            
            turma.professor_id = professor.id
            session.add(turma)
            session.commit()
            session.refresh(turma)
            return turma

        if usuario.is_aluno:
            aluno = AlunoCRUD.get_by_email(session, usuario.username)
            if not aluno:
                raise HTTPException(status_code=404, detail="Aluno não encontrado para este usuário")
            return TurmaService.inclui_turma_no_aluno(session, aluno.id, turma_id)
        
        raise HTTPException(status_code=400, detail="Usuário não possui cargo associável à turma")

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