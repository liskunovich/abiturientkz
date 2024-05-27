from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from abiturient.infra.db.models import (
    Profile
)
from abiturient.infra.repositories.postgresql.common import CommonRepo


class ProfileWriter(CommonRepo):

    async def delete_profile(self, id: UUID, soft: bool = True):
        return await self.delete(entity=Profile, where=(Profile.id == id), soft=soft)

    async def update_profile(self, id, **kwargs):
        return await self.update(entity=Profile, where=(Profile.id == id), **kwargs)

    async def create_profile(self, instance: Profile):
        await self.insert(instance=instance)


class ProfileReader(CommonRepo):

    async def get_profiles(
            self,
            limit: int = None,
            offset: int = None
    ):
        query = (
            select(Profile)
            .group_by(Profile)
            .order_by(self.latest_date(entity=Profile).desc())
            .limit(limit)
            .offset(offset)
        )
        total_qty = await self.session.execute(
            select(func.count())
        )
        result = await self.session.execute(query)
        return result.scalars().all(), total_qty.scalar_one()

    async def get_profile(self, profile_id: UUID) -> Profile | None:
        query = (
            select(Profile)
            .select_from(Profile)
            .distinct(Profile.id)
            .where(Profile.id == profile_id)
        )
        result = await self.session.execute(query)

        return result.scalars().one_or_none()
