from typing import Optional
from fastapi import APIRouter, Depends
from app.schemas.professor_schema import ProfessorCreate, ProfessorRead, ProfessorUpdate
from app.services.professor_service import ProfessorService
from app.api.dep import SessionDependency
from app.core.security import get_current_username, get_current_staff

router = APIRouter(
    prefix="/professores",
    tags=["Professores"],
    dependencies=[Depends(get_current_username)],
)


@router.post(
    "/",
    response_model=ProfessorRead,
    summary="Criar um novo professor",
    dependencies=[Depends(get_current_staff)],
)
def create_professor(professor_create: ProfessorCreate, session: SessionDependency):
    return ProfessorService.create(session, professor_create)


@router.put(
    "/{professor_id}",
    response_model=ProfessorRead,
    summary="Atualizar um professor existente",
    dependencies=[Depends(get_current_staff)],
)
def update_professor(
    professor_id: int, professor_update: ProfessorUpdate, session: SessionDependency
):
    return ProfessorService.update(session, professor_id, professor_update)


@router.delete(
    "/{professor_id}",
    summary="Deletar um professor",
    dependencies=[Depends(get_current_staff)],
)
def delete_professor(professor_id: int, session: SessionDependency):
    return ProfessorService.delete(session, professor_id)


@router.get(
    "/busca",
    response_model=list[ProfessorRead],
    summary="Obter professores por parâmetros de busca",
)
def get_professores_by_parametros(
    session: SessionDependency, nome: Optional[str] = None, email: Optional[str] = None
):
    return ProfessorService.get_by_parametros(session, nome, email)


@router.get(
    "/", response_model=list[ProfessorRead], summary="Obter todos os professores"
)
def get_all_professores(session: SessionDependency):
    return ProfessorService.get_all(session)


@router.get(
    "/{professor_id}", response_model=ProfessorRead, summary="Obter um professor por ID"
)
def get_professor_by_id(professor_id: int, session: SessionDependency):
    return ProfessorService.get_by_id(session, professor_id)
