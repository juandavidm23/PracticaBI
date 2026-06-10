import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.models.raw_models import RawCliente, RawNegocio, RawActividad, SyncLog


class RawRepository:

    def __init__(self, db: Session):
        self.db = db

    # ─── Clientes ────────────────────────────────────────────────
    def insert_clientes(
        self, records: list[dict[str, Any]], batch_id: uuid.UUID
    ) -> int:
        rows = [
            RawCliente(
                crm_id=record["id"],       # ID que viene del CRM
                payload=record,            # JSON completo, sin tocar
                sync_batch_id=batch_id,
            )
            for record in records
        ]
        self.db.bulk_save_objects(rows)
        self.db.commit()
        return len(rows)

    # ─── Negocios ────────────────────────────────────────────────
    def insert_negocios(
        self, records: list[dict[str, Any]], batch_id: uuid.UUID
    ) -> int:
        rows = [
            RawNegocio(
                crm_id=record["id"],
                payload=record,
                sync_batch_id=batch_id,
            )
            for record in records
        ]
        self.db.bulk_save_objects(rows)
        self.db.commit()
        return len(rows)

    # ─── Actividades ─────────────────────────────────────────────
    def insert_actividades(
        self, records: list[dict[str, Any]], batch_id: uuid.UUID
    ) -> int:
        rows = [
            RawActividad(
                crm_id=record["id"],
                payload=record,
                sync_batch_id=batch_id,
            )
            for record in records
        ]
        self.db.bulk_save_objects(rows)
        self.db.commit()
        return len(rows)

    # ─── Sync Log ────────────────────────────────────────────────
    def log_sync(
        self,
        batch_id: uuid.UUID,
        entity: str,
        status: str,
        records_fetched: int = 0,
        error_message: str | None = None,
    ) -> None:
        """Registra el resultado de una sincronización."""
        log = SyncLog(
            batch_id=batch_id,
            entity=entity,
            status=status,
            records_fetched=records_fetched,
            error_message=error_message,
            finished_at=datetime.now(timezone.utc),
        )
        self.db.add(log)
        self.db.commit()
