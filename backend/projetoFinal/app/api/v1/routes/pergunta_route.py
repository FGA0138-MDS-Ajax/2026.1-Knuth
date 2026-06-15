from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from app.schemas.pergunta_schema import PerguntaCreate, PerguntaRead, PerguntaUpdate, PerguntaCompleta
from app.services.pergunta_service import PerguntaService
from app.models.pergunta_model import Pergunta
from app.api.dep import SessionDependency
from app.core.security import get_current_username, possui_permissao

router = APIRouter(prefix="/perguntas", tags=["Perguntas"], dependencies=[Depends(possui_permissao(["QUALQUER"]))])

@router.post("/", response_model=PerguntaRead, summary="Criar uma nova pergunta", dependencies=[Depends(possui_permissao(["ADMIN", "ALUNO"]))])
def create_pergunta(pergunta_create: PerguntaCreate, session: SessionDependency, username: str = Depends(get_current_username)):
    return PerguntaService.create(session, pergunta_create, username)

@router.put("/{pergunta_id}", response_model=PerguntaCompleta, summary="Atualizar uma pergunta existente", dependencies=[Depends(possui_permissao(["ADMIN", "ALUNO"]))])
def update_pergunta(pergunta_id: int, pergunta_update: PerguntaUpdate, session: SessionDependency):
    return PerguntaService.update(session, pergunta_id, pergunta_update)    

@router.delete("/{pergunta_id}", summary="Deletar uma pergunta", dependencies=[Depends(possui_permissao(["ADMIN", "ALUNO"]))])
def delete_pergunta(pergunta_id: int, session: SessionDependency):
    return PerguntaService.delete(session, pergunta_id) 

@router.get("/", response_model=list[PerguntaCompleta], summary="Obter todas as perguntas")
def get_all_perguntas(session: SessionDependency):
    return PerguntaService.get_all(session)

@router.get("/{pergunta_id}", response_model=PerguntaCompleta, summary="Obter uma pergunta por ID")
def get_pergunta_by_id(pergunta_id: int, session: SessionDependency):
    return PerguntaService.get_by_id(session, pergunta_id)

