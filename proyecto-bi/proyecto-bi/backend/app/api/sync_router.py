from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.services.etl_sync import ETLSyncService

router = APIRouter(prefix="/sync", tags=["Sincronización"])


@router.post("/run", summary="Ejecutar sincronización completa")
async def run_sync(db: Session = Depends(get_db)):
    """
    Dispara manualmente el ETL completo:
      CRM → RAW (clientes, negocios, actividades)
    """
    try:
        service = ETLSyncService(db)
        result = await service.run_full_sync()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs", summary="Historial de sincronizaciones")
def get_sync_logs(limit: int = 50, db: Session = Depends(get_db)):
    """Retorna los últimos registros del sync_log."""
    rows = db.execute(
        text("""
            SELECT batch_id, entity, status, records_fetched,
                   error_message, started_at, finished_at
            FROM raw.sync_log
            ORDER BY started_at DESC
            LIMIT :limit
        """),
        {"limit": limit},
    ).mappings().all()

    return [dict(r) for r in rows]


@router.get("/stats", summary="Totales en schema RAW")
def get_raw_stats(db: Session = Depends(get_db)):
    """Cuántos registros hay en cada tabla RAW."""
    result = db.execute(
        text("""
            SELECT
                (SELECT COUNT(*) FROM raw.clientes)    AS clientes,
                (SELECT COUNT(*) FROM raw.negocios)    AS negocios,
                (SELECT COUNT(*) FROM raw.actividades) AS actividades,
                (SELECT COUNT(*) FROM raw.sync_log)    AS sync_logs
        """)
    ).mappings().one()

    return dict(result)
