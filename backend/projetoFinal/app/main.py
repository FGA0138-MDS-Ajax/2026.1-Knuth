from fastapi import FastAPI
import uvicorn
from app.api.v1.routes.curso_route import router as curso_router
from app.api.v1.routes.aluno_route import router as aluno_router
from app.api.v1.routes.usuario_route import router as usuario_router
from app.api.v1.routes.auth_route import router as auth_router           
from app.core.database import create_db_and_tables  
from contextlib import asynccontextmanager
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="API", lifespan=lifespan)
app.include_router(curso_router)
app.include_router(aluno_router)
app.include_router(usuario_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.SERVER_PORT, reload=True)
