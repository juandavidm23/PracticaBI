import logging
import uuid

from sqlalchemy.orm import Session

from app.services.crm_client import CRMClient
from app.repositories.raw_repository import RawRepository

logger = logging.getLogger(__name__)


class ETLSyncService:

    def __init__(self, db: Session):
        self.db = db
        self.crm = CRMClient()
        self.repo = RawRepository(db)

    async def run_full_sync(self) -> dict:
        """
        Ejecuta una sincronización completa de todas las entidades.
        Retorna un resumen del resultado.
        """
        batch_id = uuid.uuid4()
        logger.info(f"[ETL] Iniciando sync. batch_id={batch_id}")

        results = {}

        results["clientes"]    = await self._sync_entity("clientes",    batch_id)
        results["negocios"]    = await self._sync_entity("negocios",    batch_id)
        results["actividades"] = await self._sync_entity("actividades", batch_id)

        logger.info(f"[ETL] Sync completo. batch_id={batch_id} resultados={results}")
        return {"batch_id": str(batch_id), "entities": results}

    # ─── Sync por entidad ─────────────────────────────────────────
    async def _sync_entity(self, entity: str, batch_id: uuid.UUID) -> dict:
        """
        Sincroniza una entidad específica.

        Flujo:
          fetch del CRM → insertar en RAW → registrar log
        """
        logger.info(f"[ETL] Sincronizando: {entity}")

        try:
            # 1. Obtener datos del CRM
            records = await self._fetch_from_crm(entity)
            logger.info(f"[ETL] {entity}: {len(records)} registros obtenidos del CRM")

            # 2. Guardar en RAW (sin modificar)
            count = self._insert_raw(entity, records, batch_id)

            # 3. Registrar éxito
            self.repo.log_sync(
                batch_id=batch_id,
                entity=entity,
                status="success",
                records_fetched=count,
            )

            return {"status": "success", "records": count}

        except Exception as e:
            logger.error(f"[ETL] Error sincronizando {entity}: {e}")

            self.repo.log_sync(
                batch_id=batch_id,
                entity=entity,
                status="error",
                error_message=str(e),
            )

            return {"status": "error", "error": str(e)}

    # ─── Helpers privados ─────────────────────────────────────────
    async def _fetch_from_crm(self, entity: str) -> list:
        """Despacha al método correcto del CRM según la entidad."""
        dispatch = {
            "clientes":    self.crm.fetch_clientes,
            "negocios":    self.crm.fetch_negocios,
            "actividades": self.crm.fetch_actividades,
        }
        if entity not in dispatch:
            raise ValueError(f"Entidad desconocida: {entity}")
        return await dispatch[entity]()

    def _insert_raw(
        self, entity: str, records: list, batch_id: uuid.UUID
    ) -> int:
        """Despacha al repositorio correcto según la entidad."""
        dispatch = {
            "clientes":    self.repo.insert_clientes,
            "negocios":    self.repo.insert_negocios,
            "actividades": self.repo.insert_actividades,
        }
        return dispatch[entity](records, batch_id)
