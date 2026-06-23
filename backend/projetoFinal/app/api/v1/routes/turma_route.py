from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path
from app.schemas.turma_schema import TurmaCreate, TurmaRead, TurmaUpdate, TurmaCompleta
from app.services.turma_service import TurmaService
from app.api.dep import SessionDependency
from app.core.security import get_current_username, possui_permissao

router = APIRouter(prefix="/turmas", tags=["Turmas"], dependencies=[Depends(possui_permissao(["QUALQUER"]))])

@router.post("/", response_model=TurmaRead, summary="Criar uma nova turma", dependencies=[Depends(possui_permissao(["ADMIN", "PROFESSOR"]))])
def create_turma(turma_create: TurmaCreate, session: SessionDependency):
    return TurmaService.create(session, turma_create)

@router.put("/{turma_id}", response_model=TurmaRead, summary="Atualizar uma turma existente", dependencies=[Depends(possui_permissao(["ADMIN", "PROFESSOR"]))])
def update_turma(turma_id: int, turma_update: TurmaUpdate, session: SessionDependency):
    return TurmaService.update(session, turma_id, turma_update)

@router.delete("/{turma_id}", summary="Deletar uma turma", dependencies=[Depends(possui_permissao(["ADMIN", "PROFESSOR"]))])
def delete_turma(turma_id: int, session: SessionDependency):
    return TurmaService.delete(session, turma_id)   

@router.get("/minhas_turmas", response_model=list[TurmaRead], summary="Obter turmas do usuário logado")
def get_turmas_usuario(session: SessionDependency, username: str = Depends(get_current_username)):
    return TurmaService.get_turmas_usuario(session, username)

@router.get("/busca", response_model=list[TurmaRead], summary="Obter turmas por parâmetros de busca")
def get_turmas_by_parametros(session: SessionDependency, descricao: Optional[str] = None, periodo: Optional[str] = None, nome_professor: Optional[str] = None, nome_disciplina: Optional[str] = None):
    return TurmaService.get_by_parametros(session, descricao, periodo, nome_professor, nome_disciplina)

@router.get("/", response_model=list[TurmaRead], summary="Obter todas as turmas")
def get_all_turmas(session: SessionDependency):
    return TurmaService.get_all(session)

@router.get("/{turma_id}", response_model=TurmaRead, summary="Obter uma turma por ID")
def get_turma_by_id(turma_id: int, session: SessionDependency):
    return TurmaService.get_by_id(session, turma_id)

@router.post("/{aluno_id}/matricular/{turma_id}", response_model=TurmaCompleta, summary="Matricular um aluno em uma turma")
def matricular_aluno_turma(aluno_id: int, turma_id: int, session: SessionDependency):
    return TurmaService.inclui_turma_no_aluno(session, aluno_id, turma_id)

@router.delete("/{aluno_id}/desmatricular/{turma_id}", response_model=TurmaCompleta, summary="Desmatricular um aluno de uma turma")
def desmatricular_aluno_turma(aluno_id: int, turma_id: int, session: SessionDependency):
    return TurmaService.remove_turma_do_aluno(session, aluno_id, turma_id)

@router.post("/{aluno_id}/monitorar/{turma_id}", response_model=TurmaCompleta, summary="Tornar um aluno monitor de uma turma")
def monitorar_aluno_turma(aluno_id: int, turma_id: int, session: SessionDependency):
    return TurmaService.inclui_monitor_no_aluno(session, aluno_id, turma_id)

@router.delete("/{aluno_id}/desmonitorar/{turma_id}", response_model=TurmaCompleta, summary="Remover um aluno do monitoramento de uma turma")
def desmonitorar_aluno_turma(aluno_id: int, turma_id: int, session: SessionDependency):
    return TurmaService.remove_monitor_do_aluno(session, aluno_id, turma_id)

@router.post("/codigo_acesso_old", response_model=TurmaCompleta, 
             summary="Incluir aluno na turma usando código de acesso",
             dependencies=[Depends(possui_permissao(["ALUNO"]))])
def incluir_aluno_turma_codigo_acesso_old(codigo_acesso: str, aluno_id: int, session: SessionDependency):
    return TurmaService.inclui_aluno_codigo_acesso_old(session, codigo_acesso, aluno_id)

@router.post("/codigo_acesso", response_model=TurmaCompleta, 
             summary="Incluir aluno na turma usando código de acesso",
             dependencies=[Depends(possui_permissao(["ALUNO"]))])
def incluir_aluno_turma_codigo_acesso(codigo_acesso: str, session: SessionDependency, username: str = Depends(get_current_username)):
    return TurmaService.inclui_aluno_codigo_acesso(session, codigo_acesso, username)


@router.get("/is_monitor/{turma_id}", response_model=bool, summary="Verificar se um aluno é monitor de uma turma")
def is_usuario_monitor(session: SessionDependency, username: str = Depends(get_current_username), turma_id: int = Path(...)):
    return TurmaService.is_usuario_monitor(session, username, turma_id)

@router.get("/is_matriculado/{turma_id}", response_model=bool, summary="Verificar se um aluno está matriculado em uma turma")
def is_usuario_matriculado(session: SessionDependency, username: str = Depends(get_current_username), turma_id: int = Path(...)):
    return TurmaService.is_usuario_matriculado(session, username, turma_id)