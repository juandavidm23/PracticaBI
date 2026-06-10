from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base de datos
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "crm_bi"
    postgres_user: str = "admin"
    postgres_password: str = "admin123"

    # CRM
    crm_base_url: str = "https://jsonplaceholder.typicode.com"
    crm_api_key: str = ""

    # ETL
    sync_interval_minutes: int = 15

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
