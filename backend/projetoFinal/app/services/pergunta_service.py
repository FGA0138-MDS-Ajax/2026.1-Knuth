from app.crud.pergunta_crud import PerguntaCRUD
from app.crud.aluno_crud import AlunoCRUD
from app.crud.turma_crud import TurmaCRUD
from app.crud.usuario_crud import UsuarioCRUD
from app.schemas.pergunta_schema import PerguntaCreate, PerguntaUpdate
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
    def create(session, pergunta_create: PerguntaCreate, username: str):
        aluno = AlunoCRUD.get_by_email(session, username)
        if not aluno:
            raise HTTPException(status_code=403, detail="Apenas alunos podem criar perguntas")

        aluno_id = aluno.id
        if aluno_id is None:
            raise HTTPException(status_code=500, detail="Erro ao identificar o aluno")
        
        # Check if aluno is matriculated in the turma
        is_matriculado = TurmaCRUD.is_usuario_matriculado(session, username, pergunta_create.turma_id)
        if not is_matriculado:
            raise HTTPException(status_code=403, detail="O aluno não está matriculado nesta turma")
        
        try:
            return PerguntaCRUD.create(session, pergunta_create, aluno_id)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Turma ou aluno associado não encontrado")
            raise

    @staticmethod
    def get_by_id(session, pergunta_id: int, username: str):
        pergunta = PerguntaCRUD.get_by_id(session, pergunta_id)
        if not pergunta:
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
        
       
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        
        if usuario.is_professor:
            turma = TurmaCRUD.get_by_id(session, pergunta.turma_id)
            if turma and turma.professor.email == username:
                return pergunta
            raise HTTPException(status_code=403, detail="Você não tem permissão para visualizar esta pergunta")
        
        if usuario.is_aluno:
            aluno = AlunoCRUD.get_by_email(session, username)
            if aluno and pergunta.aluno_id == aluno.id:
                return pergunta
 
            is_monitor = TurmaCRUD.is_usuario_monitor(session, username, pergunta.turma_id)
            if is_monitor:
                if pergunta.is_restrita_professor:
                    raise HTTPException(status_code=403, detail="Esta pergunta é restrita ao professor")
                return pergunta
            
            is_matriculado = TurmaCRUD.is_usuario_matriculado(session, username, pergunta.turma_id)
            if is_matriculado:
                if pergunta.is_restrita_professor or pergunta.is_restrita_monitor:
                    raise HTTPException(status_code=403, detail="Esta pergunta possui restrições de acesso")
                return pergunta
            
        raise HTTPException(status_code=403, detail="Você não tem permissão para visualizar esta pergunta")

    @staticmethod
    def get_by_turma(session, turma_id: int, username: str):
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        is_professor_turma = False
        is_monitor_turma = False
        is_matriculado_turma = False
        
        if usuario.is_professor:
            turma = TurmaCRUD.get_by_id(session, turma_id)
            if turma and turma.professor.email == username:
                is_professor_turma = True
        elif usuario.is_aluno:
            is_monitor_turma = TurmaCRUD.is_usuario_monitor(session, username, turma_id)
            is_matriculado_turma = TurmaCRUD.is_usuario_matriculado(session, username, turma_id)
        
        if not (is_professor_turma or is_monitor_turma or is_matriculado_turma):
            raise HTTPException(status_code=403, detail="Você não tem acesso a esta turma")
        
        perguntas = PerguntaCRUD.get_by_turma(session, turma_id)
        
        filtered = []
        aluno = AlunoCRUD.get_by_email(session, username) if usuario.is_aluno else None
        
        for p in perguntas:
            if aluno and p.aluno_id == aluno.id:
                filtered.append(p)
                continue
            if is_professor_turma:
                filtered.append(p)
                continue
            if is_monitor_turma:
                if not p.is_restrita_professor:
                    filtered.append(p)
                continue
            if is_matriculado_turma:
                if not p.is_restrita_professor and not p.is_restrita_monitor:
                    filtered.append(p)
                    
        return filtered

    @staticmethod
    def update(session, pergunta_id: int, pergunta_update: PerguntaUpdate, username: str):
        pergunta = PerguntaCRUD.get_by_id(session, pergunta_id)
        if not pergunta:
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
        
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        is_creator = False
        if usuario.is_aluno:
            aluno = AlunoCRUD.get_by_email(session, username)
            if aluno and pergunta.aluno_id == aluno.id:
                is_creator = True
                
        is_professor_turma = False
        if usuario.is_professor:
            turma = TurmaCRUD.get_by_id(session, pergunta.turma_id)
            if turma and turma.professor.email == username:
                is_professor_turma = True
                
        is_monitor_turma = False
        if usuario.is_aluno:
            is_monitor_turma = TurmaCRUD.is_usuario_monitor(session, username, pergunta.turma_id)
        
        changing_metadata = (
            pergunta_update.texto is not None or 
            pergunta_update.is_restrita_professor is not None or 
            pergunta_update.is_restrita_monitor is not None
        )
        
        if changing_metadata and not is_creator:
            raise HTTPException(status_code=403, detail="Apenas o autor da pergunta pode alterar seu conteúdo ou restrições")
        
        if pergunta_update.status is not None:
            if not (is_creator or is_monitor_turma or is_professor_turma):
                raise HTTPException(status_code=403, detail="Você não tem permissão para alterar o status desta pergunta")
        
        try:
            updated = PerguntaCRUD.update(session, pergunta_id, pergunta_update)
            if not updated:
                raise HTTPException(status_code=404, detail="Pergunta não encontrada")
            return updated
        except Exception as exc:
            session.rollback()
            raise HTTPException(status_code=409, detail=str(exc))

    @staticmethod
    def delete(session, pergunta_id: int, username: str):
        pergunta = PerguntaCRUD.get_by_id(session, pergunta_id)
        if not pergunta:
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
            
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
        is_creator = False
        if usuario.is_aluno:
            aluno = AlunoCRUD.get_by_email(session, username)
            if aluno and pergunta.aluno_id == aluno.id:
                is_creator = True
                
        is_professor_turma = False
        if usuario.is_professor:
            turma = TurmaCRUD.get_by_id(session, pergunta.turma_id)
            if turma and turma.professor.email == username:
                is_professor_turma = True
                
        if not (is_creator or is_professor_turma):
            raise HTTPException(status_code=403, detail="Você não tem permissão para deletar esta pergunta")
            
        PerguntaCRUD.delete(session, pergunta_id)
        return {"detail": "Pergunta deletada com sucesso"}
