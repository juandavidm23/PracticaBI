import logging
from typing import Any

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class CRMClient:
    """Cliente HTTP para consumir el CRM."""

    def __init__(self):
        self.base_url = settings.crm_base_url.rstrip("/")
        self.headers = {
            "Content-Type": "application/json",
            # Para CRMs reales: "Authorization": f"Bearer {settings.crm_api_key}"
        }

    # ─── Método genérico ─────────────────────────────────────────
    async def _get(self, endpoint: str, params: dict | None = None) -> list[dict]:
        """Realiza un GET al CRM y retorna la lista de registros."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"[CRM] GET {url} params={params}")

        async with httpx.AsyncClient(timeout=30) as client:
            response = client.get(url, headers=self.headers, params=params or {})
            # httpx síncrono dentro de async: usamos await directamente
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=self.headers, params=params or {})

        response.raise_for_status()
        data = response.json()

        # JSONPlaceholder devuelve lista o dict; normalizamos a lista
        return data if isinstance(data, list) else [data]

    # ─── Entidades del CRM ───────────────────────────────────────
    async def fetch_clientes(self) -> list[dict[str, Any]]:
        """
        Obtiene clientes del CRM.
        JSONPlaceholder: /users (10 registros)
        """
        return await self._get("/users")

    async def fetch_negocios(self) -> list[dict[str, Any]]:
        """
        Obtiene negocios / oportunidades del CRM.
        JSONPlaceholder: /posts (100 registros)
        """
        return await self._get("/posts")

    async def fetch_actividades(self) -> list[dict[str, Any]]:
        """
        Obtiene actividades / tareas del CRM.
        JSONPlaceholder: /todos (200 registros)
        """
        return await self._get("/todos")
