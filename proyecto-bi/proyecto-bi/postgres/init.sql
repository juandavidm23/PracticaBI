-- =============================================================
-- Inicialización de la base de datos CRM → BI
-- =============================================================

-- ─── Schemas ─────────────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;

-- =============================================================
-- SCHEMA RAW
-- Copia exacta de lo que llega del CRM. Nunca se modifica.
-- =============================================================

CREATE TABLE IF NOT EXISTS raw.clientes (
    id              SERIAL PRIMARY KEY,
    crm_id          INTEGER NOT NULL,           -- ID original del CRM
    payload         JSONB   NOT NULL,           -- JSON completo sin tocar
    source          TEXT    NOT NULL DEFAULT 'jsonplaceholder',
    ingested_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sync_batch_id   UUID                        -- agrupa registros de una misma ejecución
);

CREATE TABLE IF NOT EXISTS raw.negocios (
    id              SERIAL PRIMARY KEY,
    crm_id          INTEGER NOT NULL,
    payload         JSONB   NOT NULL,
    source          TEXT    NOT NULL DEFAULT 'jsonplaceholder',
    ingested_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sync_batch_id   UUID
);

CREATE TABLE IF NOT EXISTS raw.actividades (
    id              SERIAL PRIMARY KEY,
    crm_id          INTEGER NOT NULL,
    payload         JSONB   NOT NULL,
    source          TEXT    NOT NULL DEFAULT 'jsonplaceholder',
    ingested_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sync_batch_id   UUID
);

-- ─── Tabla de control de sincronizaciones ────────────────────
CREATE TABLE IF NOT EXISTS raw.sync_log (
    id              SERIAL PRIMARY KEY,
    batch_id        UUID        NOT NULL,
    entity          TEXT        NOT NULL,   -- 'clientes', 'negocios', etc.
    status          TEXT        NOT NULL,   -- 'success', 'error'
    records_fetched INTEGER     DEFAULT 0,
    error_message   TEXT,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at     TIMESTAMPTZ
);

-- ─── Índices ─────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_raw_clientes_crm_id    ON raw.clientes(crm_id);
CREATE INDEX IF NOT EXISTS idx_raw_clientes_ingested  ON raw.clientes(ingested_at);
CREATE INDEX IF NOT EXISTS idx_raw_negocios_crm_id    ON raw.negocios(crm_id);
CREATE INDEX IF NOT EXISTS idx_raw_actividades_crm_id ON raw.actividades(crm_id);
