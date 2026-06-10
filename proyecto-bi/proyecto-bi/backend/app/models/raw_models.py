"""
Modelos SQLAlchemy para el schema RAW.

Estas tablas guardan el JSON original del CRM sin ninguna modificación.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database import Base


class RawCliente(Base):
    __tablename__ = "clientes"
    __table_args__ = {"schema": "raw"}

    id            = Column(Integer, primary_key=True, autoincrement=True)
    crm_id        = Column(Integer, nullable=False, index=True)
    payload       = Column(JSONB, nullable=False)          # JSON exacto del CRM
    source        = Column(Text, nullable=False, default="jsonplaceholder")
    ingested_at   = Column(DateTime(timezone=True), server_default=func.now())
    sync_batch_id = Column(UUID(as_uuid=True), nullable=True)


class RawNegocio(Base):
    __tablename__ = "negocios"
    __table_args__ = {"schema": "raw"}

    id            = Column(Integer, primary_key=True, autoincrement=True)
    crm_id        = Column(Integer, nullable=False, index=True)
    payload       = Column(JSONB, nullable=False)
    source        = Column(Text, nullable=False, default="jsonplaceholder")
    ingested_at   = Column(DateTime(timezone=True), server_default=func.now())
    sync_batch_id = Column(UUID(as_uuid=True), nullable=True)


class RawActividad(Base):
    __tablename__ = "actividades"
    __table_args__ = {"schema": "raw"}

    id            = Column(Integer, primary_key=True, autoincrement=True)
    crm_id        = Column(Integer, nullable=False, index=True)
    payload       = Column(JSONB, nullable=False)
    source        = Column(Text, nullable=False, default="jsonplaceholder")
    ingested_at   = Column(DateTime(timezone=True), server_default=func.now())
    sync_batch_id = Column(UUID(as_uuid=True), nullable=True)


class SyncLog(Base):
    __tablename__ = "sync_log"
    __table_args__ = {"schema": "raw"}

    id              = Column(Integer, primary_key=True, autoincrement=True)
    batch_id        = Column(UUID(as_uuid=True), nullable=False)
    entity          = Column(Text, nullable=False)
    status          = Column(Text, nullable=False)          # 'success' | 'error'
    records_fetched = Column(Integer, default=0)
    error_message   = Column(Text, nullable=True)
    started_at      = Column(DateTime(timezone=True), server_default=func.now())
    finished_at     = Column(DateTime(timezone=True), nullable=True)
