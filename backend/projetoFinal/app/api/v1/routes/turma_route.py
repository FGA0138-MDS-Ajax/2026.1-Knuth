from typing import Optional
from fastapi import APIRouter
from app.schemas.turma_schema import (
    TurmaCreate,
    TurmaRead,
    TurmaUpdate,
    TurmaCompleta
)
from app.services.turma_service import TurmaService
from app.api.dep import SessionDependency

router = APIRouter(
    prefix="/turmas",
    tags=["Turmas"]
)

@router.post("/", response_model=TurmaRead, summary="Criar uma nova turma")
def create_turma(turma_create: TurmaCreate, session: SessionDependency):
    return TurmaService.create(session, turma_create)


@router.put("/{turma_id}", response_model=TurmaRead, summary="Atualizar uma turma existente")
def update_turma(turma_id: int, turma_update: TurmaUpdate, session: SessionDependency):
    return TurmaService.update(session, turma_id, turma_update)


@router.delete("/{turma_id}", summary="Deletar uma turma")
def delete_turma(turma_id: int, session: SessionDependency):
    return TurmaService.delete(session, turma_id)


@router.get("/busca", response_model=list[TurmaRead], summary="Obter turmas por parâmetros de busca")
def get_turmas_by_parametros(
    session: SessionDependency,
    descricao: Optional[str] = None,
    periodo: Optional[str] = None,
    nome_professor: Optional[str] = None,
    nome_disciplina: Optional[str] = None
):
    return TurmaService.get_by_parametros(
        session,
        descricao,
        periodo,
        nome_professor,
        nome_disciplina
    )


@router.get("/", response_model=list[TurmaRead], summary="Obter todas as turmas")
def get_all_turmas(session: SessionDependency):
    return TurmaService.get_all(session)


@router.get("/{turma_id}", response_model=TurmaRead, summary="Obter uma turma por ID")
def get_turma_by_id(turma_id: int, session: SessionDependency):
    return TurmaService.get_by_id(session, turma_id)


@router.post(
    "/{aluno_id}/matricular/{turma_id}",
    response_model=TurmaCompleta,
    summary="Matricular um aluno em uma turma"
)
def matricular_aluno_turma(
    aluno_id: int,
    turma_id: int,
    session: SessionDependency
):
    return TurmaService.inclui_turma_no_aluno(
        session,
        aluno_id,
        turma_id
    )


@router.delete(
    "/{aluno_id}/desmatricular/{turma_id}",
    response_model=TurmaCompleta,
    summary="Desmatricular um aluno de uma turma"
)
def desmatricular_aluno_turma(
    aluno_id: int,
    turma_id: int,
    session: SessionDependency
):
    return TurmaService.remove_turma_do_aluno(
        session,
        aluno_id,
        turma_id
    )


@router.post(
    "/{aluno_id}/monitorar/{turma_id}",
    response_model=TurmaCompleta,
    summary="Tornar um aluno monitor de uma turma"
)
def monitorar_aluno_turma(
    aluno_id: int,
    turma_id: int,
    session: SessionDependency
):
    return TurmaService.inclui_monitor_no_aluno(
        session,
        aluno_id,
        turma_id
    )


@router.delete(
    "/{aluno_id}/desmonitorar/{turma_id}",
    response_model=TurmaCompleta,
    summary="Remover um aluno do monitoramento de uma turma"
)
def desmonitorar_aluno_turma(
    aluno_id: int,
    turma_id: int,
    session: SessionDependency
):
    return TurmaService.remove_monitor_do_aluno(
        session,
        aluno_id,
        turma_id
    )