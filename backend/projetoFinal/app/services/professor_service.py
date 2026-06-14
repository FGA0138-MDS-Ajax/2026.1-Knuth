from fastapi import HTTPException
from app.crud.professor_crud import ProfessorCRUD
from app.schemas.professor_schema import ProfessorCreate, ProfessorUpdate
from sqlmodel import Session

class ProfessorService:
    @staticmethod
    def create(session: Session, professor_create: ProfessorCreate):
        if ProfessorCRUD.get_by_email(session, professor_create.email):
            raise HTTPException(status_code=409, detail="Professor com este e-mail já cadastrado")
        return ProfessorCRUD.create(session, professor_create)

    @staticmethod
    def update(session: Session, professor_id: int, professor_update: ProfessorUpdate):
        professor = ProfessorCRUD.update(session, professor_id, professor_update)
        if not professor:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return professor

    @staticmethod
    def delete(session: Session, professor_id: int):
        if not ProfessorCRUD.delete(session, professor_id):
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return {"detail": "Professor deletado com sucesso"}

    @staticmethod
    def get_by_id(session: Session, professor_id: int):
        professor = ProfessorCRUD.get_by_id(session, professor_id)
        if not professor:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return professor

    @staticmethod
    def get_all(session: Session):
        return ProfessorCRUD.get_all(session)
    
    @staticmethod
    def get_by_email(session: Session, email: str):
        professor = ProfessorCRUD.get_by_email(session, email)
        if not professor:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return professor
