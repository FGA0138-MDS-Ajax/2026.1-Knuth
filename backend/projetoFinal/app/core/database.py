from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from app.core.config import settings


engine = create_engine(settings.get_database_url(), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE pergunta ADD COLUMN IF NOT EXISTS prioridade VARCHAR NOT NULL DEFAULT 'media'"))
        conn.commit()