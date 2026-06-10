from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# ─── Motor de conexión ────────────────────────────────────────
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,   # verifica conexión antes de usarla
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# ─── Dependency para FastAPI ──────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection() -> bool:
    """Verifica que la BD esté disponible."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
