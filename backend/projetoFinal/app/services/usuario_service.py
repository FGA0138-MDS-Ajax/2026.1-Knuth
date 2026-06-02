from fastapi import HTTPException
from app.crud.usuario_crud import UsuarioCRUD
from app.core.security import verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings

class UsuarioService:
    @staticmethod
    def create(session, usuario_create):
        if UsuarioCRUD.get_by_username(session, usuario_create.username):
            raise HTTPException(status_code=409, detail="Usuário com esse username já existe")
        return UsuarioCRUD.create(session, usuario_create)

    @staticmethod
    def get_by_id(session, usuario_id):
        usuario = UsuarioCRUD.get_by_id(session, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return usuario

    @staticmethod
    def delete(session, usuario_id):
        if not UsuarioCRUD.get_by_id(session, usuario_id):
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        UsuarioCRUD.delete(session, usuario_id)
        return {"detail": "Usuário deletado com sucesso"}
    
    @staticmethod
    def get_by_username(session, username):
        usuario = UsuarioCRUD.get_by_username(session, username)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado com esse username")
        return usuario
    
    @staticmethod
    def get_all(session):
        return UsuarioCRUD.get_all(session)
    
    @staticmethod
    def update_password(session, troca_senha):
        usuario = UsuarioCRUD.update_password(session, troca_senha)
        if not usuario:
            raise HTTPException(status_code=400, detail="Erro ao trocar senha. Verifique as informações fornecidas.")
        return usuario
    
    @staticmethod
    def update_usuario(session, usuario_id, usuario_update):
        usuario = UsuarioCRUD.update_usuario(session, usuario_id, usuario_update)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return usuario
    
    @staticmethod 
    def login(session, usuario_login):
        usuario = UsuarioCRUD.get_by_username(
            session,
            usuario_login.username
        )

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Usuário ou senha inválidos"
            )
        
        senha_correta = verify_password(
            usuario_login.password,
            usuario.hashed_password
        )

        if not senha_correta:
            raise HTTPException(
                status_code=401,
                detail="Usuário ou senha inválidos"
            )
        
        access_token = create_access_token(
            data={"sub": usuario.username}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    