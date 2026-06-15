from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from app.schemas.resposta_schema import RespostaCreate, RespostaRead, RespostaUpdate
from app.services.resposta_service import RespostaService
from app.models.resposta_model import Resposta
from app.api.dep import SessionDependency
from app.core.security import get_current_username, possui_permissao

router = APIRouter(prefix="/respostas", tags=["Respostas"], dependencies=[Depends(possui_permissao(["QUALQUER"]))])

@router.post("/", response_model=RespostaRead, summary="Criar uma nova resposta")
def create_resposta(resposta_create: RespostaCreate, session: SessionDependency,username: str = Depends(get_current_username)):
    return RespostaService.create(session, resposta_create, username)

@router.put("/{resposta_id}", response_model=RespostaRead, summary="Atualizar uma resposta existente")
def update_resposta(resposta_id: int, resposta_update: RespostaUpdate, session: SessionDependency):
    return RespostaService.update(session, resposta_id, resposta_update)

@router.delete("/{resposta_id}", summary="Deletar uma resposta")
def delete_resposta(resposta_id: int, session: SessionDependency):
    return RespostaService.delete(session, resposta_id)

@router.get("/", response_model=list[RespostaRead], summary="Obter todas as respostas")
def get_all_respostas(session: SessionDependency):
    return RespostaService.get_all(session)

@router.get("/{resposta_id}", response_model=RespostaRead, summary="Obter uma resposta por ID")
def get_resposta_by_id(resposta_id: int, session: SessionDependency):
    return RespostaService.get_by_id(session, resposta_id)

