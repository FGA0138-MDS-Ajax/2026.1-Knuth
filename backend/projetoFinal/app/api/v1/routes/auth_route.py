from fastapi import HTTPException, APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, decode_access_token, get_current_username, verify_password

from app.services.usuario_service import UsuarioService
from app.services.aluno_service import AlunoService
from app.api.dep import SessionDependency


router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: SessionDependency = None):
    usuario = UsuarioService.get_by_username(session, form_data.username)
    if not usuario or not verify_password(form_data.password, usuario.hashed_password) or usuario.is_active == False:
        raise HTTPException(status_code=400, detail="E-mail ou senha inválidos")

    data={
        "sub": usuario.username,
        "id": usuario.id,
        "is_aluno": usuario.is_aluno,
        "is_monitor": usuario.is_monitor,
        "is_professor": usuario.is_professor,   
        "is_active": usuario.is_active 
    }

    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", dependencies=[Depends(get_current_username)])
def get_me(authorization: str = Header(...), session: SessionDependency = None):
    token = authorization.replace("Bearer ", "")

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )
    else:
        email = payload.get("sub")
        is_aluno = payload.get("is_aluno")  
        if email is not None and is_aluno:
            aluno =  AlunoService.get_by_email(session, email)
            payload["aluno_id"] = aluno.id
            payload["aluno_nome"] = aluno.nome
            payload["aluno_email"] = aluno.email
            payload["aluno_matricula"] = aluno.matricula
            payload["aluno_curso"] = aluno.curso.nome if aluno.curso else None    
        #todo: adicionar informações do professor no payload            
    return payload