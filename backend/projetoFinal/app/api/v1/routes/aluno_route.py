from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from app.schemas.aluno_schema import AlunoCreate, AlunoRead, AlunoUpdate
from app.services.aluno_service import AlunoService
from app.api.dep import SessionDependency
from app.core.security import get_current_username

router = APIRouter(prefix="/alunos", tags=["Alunos"], dependencies=[Depends(get_current_username)])

@router.post("/", response_model=AlunoRead,summary="Criar um novo aluno")
def create_aluno(aluno_create: AlunoCreate, session: SessionDependency):
    return AlunoService.create(session, aluno_create)

@router.put("/{aluno_id}", response_model=AlunoRead,summary="Atualizar um aluno existente")
def update_aluno(aluno_id: int, aluno_update: AlunoUpdate, session: SessionDependency):
    return AlunoService.update(session, aluno_id, aluno_update)

@router.delete("/{aluno_id}", summary="Deletar um aluno")
def delete_aluno(aluno_id: int, session: SessionDependency):
    return AlunoService.delete(session, aluno_id)

@router.get("/busca", response_model=list[AlunoRead],summary="Obter alunos por parâmetros de busca")
def get_alunos_by_parametros(session: SessionDependency, nome: Optional[str] = None, email: Optional[str] = None, matricula: Optional[str] = None):
    return AlunoService.get_by_parametros(session, nome, email, matricula)

@router.get("/", response_model=list[AlunoRead],summary="Obter todos os alunos")
def get_all_alunos(session: SessionDependency):
    return AlunoService.get_all(session)

@router.get("/{aluno_id}", response_model=AlunoRead,summary="Obter um aluno por ID")
def get_aluno_by_id(aluno_id: int, session: SessionDependency):
    return AlunoService.get_by_id(session, aluno_id)
