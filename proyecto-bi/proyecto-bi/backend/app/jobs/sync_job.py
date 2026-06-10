"""
Scheduler — dispara el ETL automáticamente cada N minutos.

Usa APScheduler (AsyncIOScheduler) para no bloquear FastAPI.
El intervalo se configura en .env → SYNC_INTERVAL_MINUTES
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import settings
from app.database import SessionLocal
from app.services.etl_sync import ETLSyncService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def _run_sync_job():
    """Función que ejecuta el ETL completo."""
    logger.info("[Scheduler] Disparando sync automático")
    db = SessionLocal()
    try:
        service = ETLSyncService(db)
        result = await service.run_full_sync()
        logger.info(f"[Scheduler] Sync finalizado: {result}")
    except Exception as e:
        logger.error(f"[Scheduler] Error en sync: {e}")
    finally:
        db.close()


def start_scheduler():
    """Registra el job y arranca el scheduler."""
    scheduler.add_job(
        _run_sync_job,
        trigger=IntervalTrigger(minutes=settings.sync_interval_minutes),
        id="etl_sync",
        replace_existing=True,
        max_instances=1,       # evita ejecuciones simultáneas
    )
    scheduler.start()
    logger.info(
        f"[Scheduler] Iniciado. Sync cada {settings.sync_interval_minutes} minutos."
    )


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("[Scheduler] Detenido.")
