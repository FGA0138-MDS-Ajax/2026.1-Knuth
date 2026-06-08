from fastapi import HTTPException, APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from app.core.security import (
    create_access_token, decode_access_token,
    get_current_username, verify_password, get_password_hash,
)
from app.crud.usuario_crud import UsuarioCRUD
from app.crud.aluno_crud import AlunoCRUD
from app.models.usuario_model import Usuario
from app.models.aluno_model import Aluno
from app.api.dep import SessionDependency

router = APIRouter()


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: SessionDependency = None):
    # UsuarioCRUD retorna None se não encontrado; UsuarioService lançaria 404
    usuario = UsuarioCRUD.get_by_username(session, form_data.username)
    if not usuario or not verify_password(form_data.password, usuario.hashed_password) or not usuario.is_active:
        raise HTTPException(status_code=400, detail="E-mail ou senha inválidos")

    data = {
    data = {
        "sub": usuario.username,
        "id": usuario.id,
        "is_aluno": usuario.is_aluno,
        "is_monitor": usuario.is_monitor,
        "is_professor": usuario.is_professor,
        "is_active": usuario.is_active,
        "is_professor": usuario.is_professor,
        "is_active": usuario.is_active,
    }
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", dependencies=[Depends(get_current_username)])
def get_me(authorization: str = Header(...), session: SessionDependency = None):
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    email = payload.get("sub")
    is_aluno = payload.get("is_aluno")
    if email and is_aluno:
        # AlunoCRUD retorna None em vez de lançar 404
        aluno = AlunoCRUD.get_by_email(session, email)
        if aluno:
            payload["aluno_id"] = aluno.id
            payload["aluno_nome"] = aluno.nome
            payload["aluno_email"] = aluno.email
            payload["aluno_matricula"] = aluno.matricula
            payload["aluno_curso"] = aluno.curso.nome if aluno.curso else None

    return payload


class RegistroCreate(BaseModel):
    nome: str
    email: str
    matricula: str
    senha: str
    curso_id: int


@router.post("/registro")
async def registro(dados: RegistroCreate, session: SessionDependency = None):
    if UsuarioCRUD.get_by_username(session, dados.email):
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")

    try:
        usuario = Usuario(
            username=dados.email,
            hashed_password=get_password_hash(dados.senha),
        )
        session.add(usuario)
        session.flush()

        aluno = Aluno(
            nome=dados.nome,
            email=dados.email,
            matricula=dados.matricula,
            curso_id=dados.curso_id,
        )
        session.add(aluno)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="E-mail ou matrícula já cadastrados")

    return {"detail": "Cadastro realizado com sucesso"}
