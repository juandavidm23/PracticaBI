import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import check_connection
from app.jobs.sync_job import start_scheduler, stop_scheduler
from app.api.sync_router import router as sync_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────
    logger.info("Iniciando aplicación...")

    if check_connection():
        logger.info("✅ PostgreSQL conectado")
    else:
        logger.warning("⚠️  No se pudo conectar a PostgreSQL")

    start_scheduler()

    yield  # la app corre aquí

    # ── Shutdown ─────────────────────────────────────────────
    stop_scheduler()
    logger.info("Aplicación detenida.")


app = FastAPI(
    title="CRM → BI Backend",
    description="ETL que extrae datos del CRM y los almacena en PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── Routers ─────────────────────────────────────────────────
app.include_router(sync_router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "CRM BI Backend corriendo"}


@app.get("/health", tags=["Health"])
def health():
    db_ok = check_connection()
    return {
        "api": "ok",
        "database": "ok" if db_ok else "error",
    }
