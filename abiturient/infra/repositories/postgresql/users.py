from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from abiturient.infra.db.models import (
    User
)
from abiturient.infra.repositories.postgresql.common import CommonRepo


class UserReader(CommonRepo):

    async def get_users(
            self,
            limit: int = None,
            offset: int = None
    ):
        query = (
            select(User)
            .group_by(User)
            .order_by(self.latest_date(entity=User).desc())
            .limit(limit)
            .offset(offset)
        )
        total_qty = await self.session.execute(
            select(func.count())
        )
        result = await self.session.execute(query)
        return result.scalars().all(), total_qty.scalar_one()

    async def get_user_by_email(self, email: str):
        query = (
            select(User)
            .where(
                User.email == email,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_user(self, user_id: UUID) -> User:
        query = (
            select(User)
            .select_from(User)
            .distinct(User.id)
            .where(User.id == user_id)
        )
        result = await self.session.execute(query)

        return result.scalars().one_or_none()


class UserWriter(CommonRepo):

    async def delete_user(self, id: UUID, soft: bool = True):
        return await self.delete(entity=User, where=(User.id == id), soft=soft)

    async def update_user(self, id, **kwargs):
        return await self.update(entity=User, where=(User.id == id), **kwargs)

    async def create_user(self, instance: User):
        await self.insert(instance=instance)
