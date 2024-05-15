from os import environ

from pydantic_settings import BaseSettings
from pydantic import (
    PostgresDsn,
)


class Settings(BaseSettings):
    DEBUG: bool = environ.get("DEBUG", default=True)

    PG_USER: str = environ.get("POSTGRES_USER", default='')
    PG_PASSWORD: str = environ.get("POSTGRES_PASSWORD", default='')
    PG_DB: str = environ.get("POSTGRES_DB", default='')
    PG_HOST: str = environ.get("POSTGRES_HOST", default='')
    PG_PORT: str = environ.get("POSTGRES_PORT", default='')

    SECRET_KEY: str = environ.get("SECRET_KEY", default='')
    ALGORITHM: str = environ.get("ALGORITHM", default='HS256')

    POSTGRES_POOL_SIZE: int = environ.get('POSTGRES_POOL_SIZE', default=15)

    def build_psql_url(
            self,
            pg_user,
            pg_password,
            pg_host,
            pg_port,
            pg_db
    ):
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=pg_user,
            password=pg_password,
            host=pg_host,
            port=int(pg_port),
            path='{0}'.format(pg_db),
        )

    def build_sync_psql_url(self):
        return PostgresDsn.build(
            scheme='postgresql',
            user=self.PG_USER,
            password=self.PG_PASSWORD,
            host=self.PG_HOST,
            port=self.PG_PORT,
            path='{0}'.format(self.PG_DB),
        )

    @property
    def db_url(self):
        return self.build_psql_url(
            pg_user=self.PG_USER,
            pg_password=self.PG_PASSWORD,
            pg_host=self.PG_HOST,
            pg_port=self.PG_PORT,
            pg_db=self.PG_DB,
        )


settings_instance = Settings()
