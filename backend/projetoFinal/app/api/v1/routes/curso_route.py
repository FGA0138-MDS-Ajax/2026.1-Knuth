from typing import Optional
from fastapi import APIRouter, Depends
from app.schemas.curso_schema import CursoCreate, CursoRead, CursoSummary, CursoUpdate
from app.services.curso_service import CursoService
from app.api.dep import SessionDependency
from app.core.security import get_current_username, get_current_professor

router = APIRouter(prefix="/cursos", tags=["Cursos"])

<<<<<<< HEAD
_auth = [Depends(get_current_username)]

@router.post("/", response_model=CursoRead, summary="Criar um novo curso", dependencies=_auth)
def create_curso(curso_create: CursoCreate, session: SessionDependency):
    return CursoService.create(session, curso_create)

@router.put("/{curso_id}", response_model=CursoRead, summary="Atualizar um curso existente", dependencies=_auth)
def update_curso(curso_id: int, curso_update: CursoUpdate, session: SessionDependency):
    return CursoService.update(session, curso_id, curso_update)

@router.delete("/{curso_id}", summary="Deletar um curso", dependencies=_auth)
=======
@router.post("/", response_model=CursoRead,summary="Criar um novo curso", dependencies=[Depends(get_current_professor)])
def create_curso(curso_create: CursoCreate, session: SessionDependency):
    return CursoService.create(session, curso_create)

@router.put("/{curso_id}", response_model=CursoRead,summary="Atualizar um curso existente", dependencies=[Depends(get_current_professor)])
def update_curso(curso_id: int, curso_update: CursoUpdate, session: SessionDependency):
    return CursoService.update(session, curso_id, curso_update)

@router.delete("/{curso_id}", summary="Deletar um curso", dependencies=[Depends(get_current_professor)])
>>>>>>> 3f1e9b9dc904f8c994db02a0be7e3179a7b2d237
def delete_curso(curso_id: int, session: SessionDependency):
    return CursoService.delete(session, curso_id)

@router.get("/busca", response_model=list[CursoRead], summary="Obter cursos por parâmetros de busca", dependencies=_auth)
def get_cursos_by_parametros(session: SessionDependency, nome: Optional[str] = None):
    return CursoService.get_by_parametros(session, nome)

@router.get("/", response_model=list[CursoSummary], summary="Listar cursos (público — usado no cadastro)")
def get_all_cursos(session: SessionDependency):
    return CursoService.get_all(session)

@router.get("/{curso_id}", response_model=CursoRead, summary="Obter um curso por ID", dependencies=_auth)
def get_curso_by_id(curso_id: int, session: SessionDependency):
    return CursoService.get_by_id(session, curso_id)