from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from app.schemas.aluno_schema import AlunoCreate, AlunoRead, AlunoUpdate, AlunoCompleto
from app.services.aluno_service import AlunoService
from app.api.dep import SessionDependency
from app.core.security import possui_permissao

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.post("/", response_model=AlunoRead, summary="Criar um novo aluno")
def create_aluno(aluno_create: AlunoCreate, session: SessionDependency):
    return AlunoService.create(session, aluno_create)

@router.put("/{aluno_id}", response_model=AlunoRead, summary="Atualizar um aluno existente", dependencies=[Depends(possui_permissao(["QUALQUER"]))])
def update_aluno(aluno_id: int, aluno_update: AlunoUpdate, session: SessionDependency):
    return AlunoService.update(session, aluno_id, aluno_update)

@router.delete("/{aluno_id}", summary="Deletar um aluno", dependencies=[Depends(possui_permissao(["ADMIN", "PROFESSOR"]))])
def delete_aluno(aluno_id: int, session: SessionDependency):
    return AlunoService.delete(session, aluno_id)

@router.get("/busca", response_model=list[AlunoCompleto], summary="Obter alunos por parâmetros de busca", dependencies=[Depends(possui_permissao(["QUALQUER"]))])
def get_alunos_by_parametros(session: SessionDependency, nome: Optional[str] = None, email: Optional[str] = None, matricula: Optional[str] = None):
    return AlunoService.get_by_parametros(session, nome, email, matricula)

@router.get("/", response_model=list[AlunoCompleto], summary="Obter todos os alunos", dependencies=[Depends(possui_permissao(["QUALQUER"]))])
def get_all_alunos(session: SessionDependency):
    return AlunoService.get_all(session)

@router.get("/{aluno_id}", response_model=AlunoCompleto, summary="Obter um aluno por ID", dependencies=[Depends(possui_permissao(["QUALQUER"]))])
def get_aluno_by_id(aluno_id: int, session: SessionDependency):
    return AlunoService.get_by_id(session, aluno_id)

@router.post("/{aluno_id}/matricular/{turma_id}", response_model=AlunoCompleto, summary="Matricular um aluno em uma turma", dependencies=[Depends(possui_permissao(["QUALQUER"]))])
def matricular_aluno_turma(aluno_id: int, turma_id: int, session: SessionDependency):
    return AlunoService.inclui_aluno_na_turma(session, aluno_id, turma_id)

@router.delete("/{aluno_id}/desmatricular/{turma_id}", response_model=AlunoCompleto, summary="Desmatricular um aluno de uma turma", dependencies=[Depends(possui_permissao(["QUALQUER"]))])
def desmatricular_aluno_turma(aluno_id: int, turma_id: int, session: SessionDependency):
    return AlunoService.remove_aluno_da_turma(session, aluno_id, turma_id)

