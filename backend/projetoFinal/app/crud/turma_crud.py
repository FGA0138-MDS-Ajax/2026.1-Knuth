from certifi import where
from sqlmodel import Session, select
from app.models.aluno_model import Aluno
from app.models.alunoTurmaMatriculado_model import AlunoTurmaMatriculado
from app.models.alunoTurmaMonitor_model import AlunoTurmaMonitor
from app.models.turma_model import Turma
from app.schemas.turma_schema import TurmaCreate, TurmaRead, TurmaUpdate
from app.models.professor_model import Professor
from app.models.disciplina_model import Disciplina
from app.crud.usuario_crud import UsuarioCRUD
from app.models.usuario_model import Usuario
from typing import Optional


class TurmaCRUD:
    
    @staticmethod
    def create(session: Session, turma_create: TurmaCreate):
        turma = Turma.model_validate(turma_create)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def update(session: Session, turma_id: int, turma_update: TurmaUpdate):
        TurmaUpdate.model_validate(turma_update)
        turma = session.get(Turma, turma_id)
        if not turma:
            return None
        turma.descricao = turma_update.descricao
        turma.horario = turma_update.horario
        turma.periodo = turma_update.periodo
        turma.disciplina_id = turma_update.disciplina_id
        turma.professor_id = turma_update.professor_id
        turma.codigo_acesso = turma_update.codigo_acesso
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def delete(session: Session, turma_id: int):
        turma = session.get(Turma, turma_id)
        if not turma:
            return None
        session.delete(turma)
        session.commit()

    @staticmethod
    def get_by_id(session: Session, turma_id: int):
        return session.get(Turma, turma_id)
    
    @staticmethod
    def get_all(session: Session):
        statement = select(Turma)
        return session.exec(statement).all()
    
    @staticmethod
    def get_by_parametros(
        session: Session,
        descricao: Optional[str] = None,
        periodo: Optional[str] = None,
        nome_professor: Optional[str] = None,
        nome_disciplina: Optional[str] = None,
    ):
        statement = select(Turma)
        if descricao:
            statement = statement.where(Turma.descricao.ilike(f"%{descricao}%"))  # pyright: ignore[reportAttributeAccessIssue]
        if periodo:
            statement = statement.where(Turma.periodo.ilike(f"%{periodo}%"))  # pyright: ignore[reportAttributeAccessIssue]
        if nome_professor:
            statement = statement.join(Professor)
            statement = statement.where(Professor.nome.ilike(f"%{nome_professor}%"))  # pyright: ignore[reportAttributeAccessIssue]
        if nome_disciplina:
            statement = statement.join(Disciplina)
            statement = statement.where(Disciplina.nome.ilike(f"%{nome_disciplina}%"))  # pyright: ignore[reportAttributeAccessIssue]
        return session.exec(statement).all()
    
    @staticmethod
    def inclui_aluno(session: Session, aluno: Aluno, turma: Turma):
        turma.alunosMatriculados.append(aluno)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def remove_aluno(session: Session, aluno: Aluno, turma: Turma):
        turma.alunosMatriculados.remove(aluno)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def inclui_monitor(session: Session, aluno: Aluno, turma: Turma):
        turma.alunosMonitores.append(aluno)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def remove_monitor(session: Session, aluno: Aluno, turma: Turma):
        turma.alunosMonitores.remove(aluno)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma
    
    @staticmethod
    def get_by_codigo_acesso(session: Session, codigo_acesso: str):
        return session.exec(select(Turma).where(Turma.codigo_acesso == codigo_acesso)).first()
    
    @staticmethod
    def get_turmas_usuario(session: Session, username: str):
        usuario = UsuarioCRUD.get_by_username(session, username)
        if usuario is None:
            raise ValueError("Usuário não encontrado")
        if not usuario.is_aluno and not usuario.is_professor:
            raise ValueError("Usuário deve ser aluno ou professor")
        if usuario.is_professor:
            statement = (
                select(Turma)
                .join(Professor)
                .where(Professor.email == usuario.username)
            )
            return session.exec(statement).all()
        if usuario.is_aluno:
            statement_matriculado = (
                select(Turma)
                .join(AlunoTurmaMatriculado)
                .join(Aluno)
                .where(Aluno.email == usuario.username)
            )
            statement_monitor = (
                select(Turma)
                .join(AlunoTurmaMonitor)
                .join(Aluno)
                .where(Aluno.email == usuario.username)
            )
            turmas_matriculadas = session.exec(statement_matriculado).all()
            turmas_monitoradas = session.exec(statement_monitor).all()
            
            seen = set()
            result = []
            for t in [*turmas_matriculadas, *turmas_monitoradas]:
                if t.id not in seen:
                    seen.add(t.id)
                    result.append(t)
            return result
        
    @staticmethod
    def is_usuario_monitor(session: Session, username: str, turma_id: int):
        usuario = UsuarioCRUD.get_by_username(session, username)
        if usuario is None:
            raise ValueError("Usuário não encontrado")
        if not usuario.is_aluno:
            raise ValueError("Usuário deve ser aluno para ser monitor")
        statement = (
            select(Turma)
            .join(AlunoTurmaMonitor)
            .join(Aluno)
            .where(Aluno.email == usuario.username, Turma.id == turma_id)
        )
        if session.exec(statement).first() is not None:
            return True
        return False
    
    @staticmethod
    def is_usuario_matriculado(session: Session, username: str, turma_id: int):
        usuario = UsuarioCRUD.get_by_username(session, username)
        if usuario is None:
            raise ValueError("Usuário não encontrado")
        if not usuario.is_aluno:
            raise ValueError("Usuário deve ser aluno para ser matriculado")
        statement = (
            select(Turma)
            .join(AlunoTurmaMatriculado)
            .join(Aluno)
            .where(Aluno.email == usuario.username, Turma.id == turma_id)
        )
        if session.exec(statement).first() is not None:
            return True
        return False
    
    