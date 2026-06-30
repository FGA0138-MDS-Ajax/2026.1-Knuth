from fastapi import APIRouter, Depends
from app.schemas.pergunta_schema import PerguntaCreate, PerguntaRead, PerguntaUpdate
from app.services.pergunta_service import PerguntaService
from app.api.dep import SessionDependency
from app.core.security import get_current_username, possui_permissao

router = APIRouter(prefix="/perguntas", tags=["Perguntas"], dependencies=[Depends(possui_permissao(["QUALQUER"]))])

@router.post("/", response_model=PerguntaRead, summary="Criar uma nova pergunta")
def create_pergunta(pergunta_create: PerguntaCreate, session: SessionDependency, username: str = Depends(get_current_username)):
    return PerguntaService.create(session, pergunta_create, username)

@router.get("/turma/{turma_id}", response_model=list[PerguntaRead], summary="Obter perguntas de uma turma")
def get_perguntas_by_turma(turma_id: int, session: SessionDependency, username: str = Depends(get_current_username)):
    return PerguntaService.get_by_turma(session, turma_id, username)

@router.get("/{pergunta_id}", response_model=PerguntaRead, summary="Obter uma pergunta por ID")
def get_pergunta_by_id(pergunta_id: int, session: SessionDependency, username: str = Depends(get_current_username)):
    return PerguntaService.get_by_id(session, pergunta_id, username)

@router.put("/{pergunta_id}", response_model=PerguntaRead, summary="Atualizar uma pergunta existente")
def update_pergunta(pergunta_id: int, pergunta_update: PerguntaUpdate, session: SessionDependency, username: str = Depends(get_current_username)):
    return PerguntaService.update(session, pergunta_id, pergunta_update, username)

@router.delete("/{pergunta_id}", summary="Deletar uma pergunta")
def delete_pergunta(pergunta_id: int, session: SessionDependency, username: str = Depends(get_current_username)):
    return PerguntaService.delete(session, pergunta_id, username)
