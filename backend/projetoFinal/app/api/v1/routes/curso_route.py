from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from app.schemas.curso_schema import CursoCreate, CursoRead, CursoUpdate
from app.services.curso_service import CursoService
from app.api.dep import SessionDependency
from app.core.security import get_current_username

router = APIRouter(prefix="/cursos", tags=["Cursos"], dependencies=[Depends(get_current_username)])

@router.post("/", response_model=CursoRead,summary="Criar um novo curso")
def create_curso(curso_create: CursoCreate, session: SessionDependency):
    return CursoService.create(session, curso_create)

@router.put("/{curso_id}", response_model=CursoRead,summary="Atualizar um curso existente")
def update_curso(curso_id: int, curso_update: CursoUpdate, session: SessionDependency):
    return CursoService.update(session, curso_id, curso_update)

@router.delete("/{curso_id}", summary="Deletar um curso")
def delete_curso(curso_id: int, session: SessionDependency):
    return CursoService.delete(session, curso_id)   

@router.get("/busca", response_model=list[CursoRead],summary="Obter cursos por parâmetros de busca")
def get_cursos_by_parametros(session: SessionDependency, nome: Optional[str] = None):
    return CursoService.get_by_parametros(session, nome)

@router.get("/", response_model=list[CursoRead],summary="Obter todos os cursos")
def get_all_cursos(session: SessionDependency):
    return CursoService.get_all(session)

@router.get("/{curso_id}", response_model=CursoRead,summary="Obter um curso por ID")
def get_curso_by_id(curso_id: int, session: SessionDependency):
    return CursoService.get_by_id(session, curso_id)