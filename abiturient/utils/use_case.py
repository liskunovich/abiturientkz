from sqlalchemy.ext.asyncio import AsyncSession


class BaseUseCaseWithSession:
    def __init__(self, session: AsyncSession):
        self.session = session
