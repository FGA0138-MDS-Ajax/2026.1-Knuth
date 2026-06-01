from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from app.schemas.usuario_schema import UsuarioCreate, UsuarioRead, UsuarioTrocaSenha, UsuarioUpdate
from app.services.usuario_service import UsuarioService
from app.api.dep import SessionDependency
from app.core.security import get_current_username  

#router = APIRouter(prefix="/usuarios", tags=["Usuários"], dependencies=[Depends(get_current_username)])
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioRead, summary="Criar um novo usuário")
def create_usuario(usuario_create: UsuarioCreate, session: SessionDependency):
    return UsuarioService.create(session, usuario_create)

@router.get("/username/{username}", response_model=UsuarioRead, summary="Obter um usuário por username")
def get_usuario_by_username(username: str, session: SessionDependency):
    return UsuarioService.get_by_username(session, username)

@router.get("/{usuario_id}", response_model=UsuarioRead, summary="Obter um usuário por ID")
def get_usuario_by_id(usuario_id: int, session: SessionDependency):
    return UsuarioService.get_by_id(session, usuario_id)

@router.delete("/{usuario_id}", summary="Deletar um usuário")
def delete_usuario(usuario_id: int, session: SessionDependency):
    return UsuarioService.delete(session, usuario_id)

@router.get("/", response_model=list[UsuarioRead], summary="Obter todos os usuários")
def get_all_usuarios(session: SessionDependency):
    return UsuarioService.get_all(session)

@router.put("/senha",response_model=UsuarioRead, summary="Trocar senha do usuário")
def update_password(troca_senha: UsuarioTrocaSenha, session: SessionDependency):
    return UsuarioService.update_password(session, troca_senha)

@router.put("/{usuario_id}", response_model=UsuarioRead, summary="Atualizar informações de um usuário")
def update_usuario(usuario_id: int, usuario_update: UsuarioUpdate, session: SessionDependency):
    return UsuarioService.update_usuario(session, usuario_id, usuario_update)
