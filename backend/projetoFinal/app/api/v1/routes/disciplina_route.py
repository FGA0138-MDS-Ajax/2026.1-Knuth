from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from app.schemas.disciplina_schema import DisciplinaCreate, DisciplinaRead, DisciplinaUpdate
from app.services.disciplina_service import DisciplinaService
from app.api.dep import SessionDependency
from app.core.security import get_current_username, possui_permissao

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"], dependencies=[Depends(possui_permissao(["QUALQUER"]))])

@router.post("/", response_model=DisciplinaRead,summary="Criar uma nova disciplina", dependencies=[Depends(possui_permissao(["ADMIN"]))])
def create_disciplina(disciplina_create: DisciplinaCreate, session: SessionDependency):
    return DisciplinaService.create(session, disciplina_create)

@router.put("/{disciplina_id}", response_model=DisciplinaRead,summary="Atualizar uma disciplina existente", dependencies=[Depends(possui_permissao(["ADMIN"]))])
def update_disciplina(disciplina_id: int, disciplina_update: DisciplinaUpdate, session: SessionDependency):
    return DisciplinaService.update(session, disciplina_id, disciplina_update)

@router.delete("/{disciplina_id}", summary="Deletar uma disciplina", dependencies=[Depends(possui_permissao(["ADMIN"]))])
def delete_disciplina(disciplina_id: int, session: SessionDependency):
    return DisciplinaService.delete(session, disciplina_id)

@router.get("/busca", response_model=list[DisciplinaRead],summary="Obter disciplinas por parâmetros de busca")
def get_disciplinas_by_parametros(session: SessionDependency, nome: Optional[str] = None):
    return DisciplinaService.get_by_parametros(session, nome)

@router.get("/", response_model=list[DisciplinaRead],summary="Obter todas as disciplinas")
def get_all_disciplinas(session: SessionDependency):
    return DisciplinaService.get_all(session)

@router.get("/{disciplina_id}", response_model=DisciplinaRead,summary="Obter uma disciplina por ID")
def get_disciplina_by_id(disciplina_id: int, session: SessionDependency):
    return DisciplinaService.get_by_id(session, disciplina_id)