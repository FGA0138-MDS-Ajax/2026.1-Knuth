from typing import Annotated
from fastapi import HTTPException, APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from app.core.security import create_access_token, decode_access_token, get_current_username, possui_permissao, verify_password

from app.services.professor_service import ProfessorService
from app.services.usuario_service import UsuarioService
from app.services.aluno_service import AlunoService
from app.api.dep import SessionDependency


router = APIRouter()


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDependency,
):
    usuario = UsuarioService.get_by_username(session, form_data.username)
    if not usuario or not verify_password(form_data.password, usuario.hashed_password) or usuario.is_active == False:
        raise HTTPException(status_code=400, detail="E-mail ou senha inválidos")

    data = {
        "sub": usuario.username,
        "id": usuario.id,
        "is_aluno": usuario.is_aluno,
        "is_professor": usuario.is_professor,   
        "is_active": usuario.is_active,
        "is_admin": usuario.is_admin
    }
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", dependencies=[Depends(possui_permissao(["QUALQUER"]))])
def get_me(
    authorization: Annotated[str, Header(...)],
    session: SessionDependency,
):
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
        is_professor = payload.get("is_professor")  
        if email is not None and is_professor:
            professor =  ProfessorService.get_by_email(session, email)
            payload["professor_id"] = professor.id
            payload["professor_nome"] = professor.nome
            payload["professor_email"] = professor.email
    return payload
