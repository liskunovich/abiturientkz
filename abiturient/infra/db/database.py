from typing import (
    AsyncGenerator,
    Callable,
)

from sqlalchemy import (
    orm,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from abiturient.core.settings import Settings


def session_factory(url: str, pool_size: int = 10):  # Default pool size: 10
    engine: AsyncEngine = create_async_engine(
        url,
        pool_pre_ping=True,
        future=True,
        connect_args={
            'timeout': 120
        },
        pool_size=pool_size,
    )
    return orm.sessionmaker(  # noqa
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False,
    )


def async_session(url: str, settings: Settings) -> Callable[..., AsyncGenerator]:
    factory = session_factory(url=url, pool_size=settings.POSTGRES_POOL_SIZE)

    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with factory() as session:
            yield session

    return get_session
