from typing import Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    func,
    select,
)

from abiturient.infra.repositories.postgresql.common import CommonRepo
from abiturient.infra.db.models import UniversityReview, EducationalProgramReview


class ReviewWriter(CommonRepo):

    def __init__(self, session: AsyncSession, review_model: Type[UniversityReview | EducationalProgramReview]):
        super().__init__(session=session)
        self.review_model = review_model

    async def delete_review(self, id: UUID, soft: bool = True):
        return await self.delete(entity=self.review_model, where=(self.review_model.id == id), soft=soft)

    async def update_review(self, id: UUID, **kwargs):
        return await self.update(entity=self.review_model, where=(self.review_model.id == id), **kwargs)

    async def create_review(self, instance: Type[UniversityReview | EducationalProgramReview]):
        await self.insert(instance=instance)


class ReviewReader(CommonRepo):
    def __init__(self, session: AsyncSession, review_model: Type[UniversityReview | EducationalProgramReview]):
        super().__init__(session=session)
        self.review_model = review_model

    async def get_reviews(
            self,
            limit: int = None,
            offset: int = None
    ):
        query = (
            select(self.review_model)
            .group_by(self.review_model)
            .order_by(self.latest_date(entity=self.review_model).desc())
            .limit(limit)
            .offset(offset)
        )
        total_qty = await self.session.execute(
            select(func.count())
        )
        result = await self.session.execute(query)
        return result.scalars().all(), total_qty.scalar_one()

    async def get_review(self, review_id: UUID) -> Type[EducationalProgramReview | UniversityReview | None]:
        query = (
            select(self.review_model)
            .select_from(self.review_model)
            .distinct(self.review_model.id)
            .where(self.review_model.id == review_id)
        )
        result = await self.session.execute(query)

        return result.scalars().one_or_none()
