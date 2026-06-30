from fastapi import APIRouter, Depends
from app.schemas.resposta_schema import RespostaCreate, RespostaRead, RespostaUpdate
from app.services.resposta_service import RespostaService
from app.api.dep import SessionDependency
from app.core.security import get_current_username, possui_permissao

router = APIRouter(prefix="/respostas", tags=["Respostas"], dependencies=[Depends(possui_permissao(["QUALQUER"]))])


@router.post("/", response_model=RespostaRead, summary="Criar uma nova resposta")
def create_resposta(resposta_create: RespostaCreate, session: SessionDependency, username: str = Depends(get_current_username)):
    return RespostaService.create(session, resposta_create, username)


@router.get("/pergunta/{pergunta_id}", response_model=list[RespostaRead], summary="Obter respostas de uma pergunta")
def get_respostas_by_pergunta(pergunta_id: int, session: SessionDependency):
    return RespostaService.get_by_pergunta(session, pergunta_id)


@router.get("/", response_model=list[RespostaRead], summary="Obter todas as respostas")
def get_all_respostas(session: SessionDependency):
    return RespostaService.get_all(session)


@router.get("/{resposta_id}", response_model=RespostaRead, summary="Obter uma resposta por ID")
def get_resposta_by_id(resposta_id: int, session: SessionDependency):
    return RespostaService.get_by_id(session, resposta_id)


@router.put("/{resposta_id}", response_model=RespostaRead, summary="Atualizar uma resposta existente")
def update_resposta(resposta_id: int, resposta_update: RespostaUpdate, session: SessionDependency, username: str = Depends(get_current_username)):
    return RespostaService.update(session, resposta_id, resposta_update, username)


@router.delete("/{resposta_id}", summary="Deletar uma resposta")
def delete_resposta(resposta_id: int, session: SessionDependency, username: str = Depends(get_current_username)):
    return RespostaService.delete(session, resposta_id, username)
