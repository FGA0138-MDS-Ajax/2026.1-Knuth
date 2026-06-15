from fastapi import FastAPI
import uvicorn
from app.api.v1.routes.curso_route import router as curso_router
from app.api.v1.routes.aluno_route import router as aluno_router
from app.api.v1.routes.usuario_route import router as usuario_router
from app.api.v1.routes.auth_route import router as auth_router     
from app.api.v1.routes.disciplina_route import router as disciplina_router     
from app.api.v1.routes.professor_route import router as professor_router 
from app.api.v1.routes.turma_route import router as turma_router
from app.api.v1.routes.pergunta_route import router as pergunta_router
from app.api.v1.routes.resposta_route import router as resposta_router
from app.core.database import create_db_and_tables  
from app.startup import seed_initial_data
from contextlib import asynccontextmanager
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    try:
        seed_initial_data()
    except Exception:
        # don't break app startup if seeding fails
        pass
    yield

app = FastAPI(title="API", lifespan=lifespan)
app.include_router(curso_router)
app.include_router(aluno_router)
app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(disciplina_router)
app.include_router(professor_router)
app.include_router(turma_router)
app.include_router(pergunta_router)
app.include_router(resposta_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.SERVER_PORT, reload=True)
