from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioRead, UsuarioTrocaSenha, UsuarioUpdate
from app.core.security import get_password_hash

class UsuarioCRUD:
    @staticmethod
    def create(session: Session, usuario_create: UsuarioCreate):
        usuarioCreate = UsuarioCreate.model_validate(usuario_create)
        usuario = Usuario(username=usuarioCreate.username, hashed_password=usuarioCreate.password)
        usuario.hashed_password = get_password_hash(usuario.hashed_password)   
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

    @staticmethod
    def get_by_id(session: Session, usuario_id: int):
        return session.get(Usuario, usuario_id)

    @staticmethod
    def get_by_username(session: Session, username: str):
        statement = select(Usuario).where(Usuario.username == username)
        result = session.exec(statement).first()
        return result
    
    @staticmethod
    def delete(session: Session, usuario_id: int):
        usuario = session.get(Usuario, usuario_id)
        if usuario:
            session.delete(usuario)
            session.commit()

    @staticmethod
    def get_all(session: Session):
        statement = select(Usuario)
        return session.exec(statement).all()
    
    @staticmethod
    def update_password(session: Session, troca_senha: UsuarioTrocaSenha):
        usuario = session.get(Usuario, troca_senha.id)
        if not usuario:
            return None
        if not verify_password(troca_senha.old_password, usuario.hashed_password):
            return not usuario
        usuario.hashed_password = get_password_hash(troca_senha.new_password)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
    
    @staticmethod
    def update_usuario(session: Session, usuario_id: int, usuario_update: UsuarioUpdate):
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            return None
        usuario.is_active = usuario_update.is_active
        usuario.is_aluno = usuario_update.is_aluno
        usuario.is_monitor = usuario_update.is_monitor
        usuario.is_professor = usuario_update.is_professor
        usuario.is_admin = usuario_update.is_admin
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
