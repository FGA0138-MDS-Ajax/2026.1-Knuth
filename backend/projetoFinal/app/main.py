from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.v1.routes.curso_route import router as curso_router
from app.api.v1.routes.aluno_route import router as aluno_router
from app.api.v1.routes.usuario_route import router as usuario_router
from app.api.v1.routes.auth_route import router as auth_router
from app.api.v1.routes.turma_route import router as turma_router
from app.api.v1.routes.disciplina_route import router as disciplina_router

from app.core.database import create_db_and_tables
from contextlib import asynccontextmanager
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das Rotas
app.include_router(curso_router)
app.include_router(aluno_router)
app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(turma_router)
app.include_router(disciplina_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.SERVER_PORT, reload=True)