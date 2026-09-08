"""Punto de entrada de ms-usuarios.

Microservicio de cuentas de acceso: registro, login y administracion de
usuarios. Es el unico que emite tokens; los demas microservicios los verifican
con el mismo JWT_SECRET, sin llamarlo por HTTP.
"""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import get_db
from app.routers import auth, usuarios

settings = get_settings()

app = FastAPI(
    title="ms-usuarios",
    description=(
        "Microservicio de usuarios del condominio: register, login, alta y baja "
        "de cuentas. Emite los tokens JWT que usan los demas microservicios."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS: sin esto el navegador bloquea el login desde el frontend en Amplify.
# TODO: en produccion reemplazar "*" por el dominio real de Amplify.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)


@app.get("/health", tags=["health"])
def health(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
        base = "ok"
    except Exception:
        base = "error"

    return {
        "status": "ok" if base == "ok" else "degraded",
        "service": settings.app_name,
        "database": base,
    }
