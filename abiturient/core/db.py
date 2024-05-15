import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from abiturient.core.settings import settings_instance
from abiturient.infra.db.models.base import Base

SQLALCHEMY_DATABASE_URL = settings_instance.db_url.unicode_string()
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)
async_session = async_sessionmaker(engine=engine, expire_on_commit=False)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def run():
    asyncio.run(get_db())
