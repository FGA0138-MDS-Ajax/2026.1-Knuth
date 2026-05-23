from app.crud.curso_crud import CursoCRUD
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class CursoService:
    
    @staticmethod
    def create(session, curso_create):
        try:
            return CursoCRUD.create(session, curso_create)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Curso com esse nome já existe")
            raise
    
    @staticmethod
    def update(session, curso_id, curso_update):
        try:
            curso = CursoCRUD.update(session, curso_id, curso_update)
        except IntegrityError as exc:
            session.rollback()
            if "unique" in str(exc).lower():
                raise HTTPException(status_code=409, detail="Curso com esse nome já existe")
            raise
        if not curso:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        return curso
    
    @staticmethod
    def delete(session, curso_id):
        if not CursoCRUD.get_by_id(session, curso_id):
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        try:
            CursoCRUD.delete(session, curso_id)
        except IntegrityError as exc:
            session.rollback()
            if "foreign key constraint" in str(exc).lower():
                raise HTTPException(status_code=400, detail="Não é possível deletar o curso porque existem alunos matriculados nele")
            raise
        return {"detail": "Curso deletado com sucesso"}

    @staticmethod
    def get_by_id(session, curso_id):
        curso = CursoCRUD.get_by_id(session, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        return curso
    
    @staticmethod
    def get_all(session):
        return CursoCRUD.get_all(session)
    
    @staticmethod
    def get_by_parametros(session, nome=None):
        return CursoCRUD.get_by_parametros(session, nome)