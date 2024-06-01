from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from abiturient.infra.repositories.postgresql.common import CommonRepo
from abiturient.infra.db.models.pdf import University, Specialization, YearStatistics, UniversitySpecialization, \
    ConcursEnum


class UniversityWriter(CommonRepo):
    async def delete_university(self, id: UUID, soft: bool = True):
        return await self.delete(entity=University, where=(University.id == id), soft=soft)

    async def update_university(self, id, **kwargs):
        return await self.update(entity=University, where=(University.id == id), **kwargs)

    async def create_university(self, instance: University):
        await self.insert(instance=instance)

    async def bulk_create_or_update_university(
            self,
            entity: University,
            data: list[dict],
            d_key: str,
            upd_values: list,
            e_where,
            pop_data: list = (),
            extension_data: dict = None,
    ):
        await super().bulk_create_or_update(entity, data, d_key, upd_values, e_where, pop_data, extension_data)


class SpecializationReader(CommonRepo):
    async def get_specialization_by_title_or_create(self, specialization_title):
        query = (
            select(Specialization)
            .select_from(Specialization)
            .distinct(Specialization.id)
            .where(Specialization.title == specialization_title)
        )
        result = await self.session.execute(query)
        specialization = result.scalars().one_or_none()

        if specialization is None:
            specialization = Specialization(title=specialization_title)
            self.session.add(specialization)
            await self.session.commit()

        return specialization


class SpecializationWriter(CommonRepo):
    async def delete_specialization(self, id: UUID, soft: bool = True):
        return await self.delete(entity=Specialization, where=(Specialization.id == id), soft=soft)

    async def update_specialization(self, id, **kwargs):
        return await self.update(entity=Specialization, where=(Specialization.id == id), **kwargs)

    async def create_specialization(self, instance: Specialization):
        await self.insert(instance=instance)

    async def bulk_create_or_update_specialization(
            self,
            entity: Specialization,
            data: list[dict],
            d_key: str,
            upd_values: list,
            e_where,
            pop_data: list = (),
            extension_data: dict = None,
    ):
        await super().bulk_create_or_update(entity, data, d_key, upd_values, e_where, pop_data, extension_data)


class YearStatisticsWriter(CommonRepo):
    async def delete_statistics(self, id: UUID, soft: bool = True):
        return await self.delete(entity=YearStatistics, where=(YearStatistics.id == id), soft=soft)

    async def update_statistics(self, id, **kwargs):
        return await self.update(entity=YearStatistics, where=(YearStatistics.id == id), **kwargs)

    async def create_statistics(self, instance: YearStatistics):
        await self.insert(instance=instance)

    async def create_or_update(self, university_specialization, specialization_type, year,
                               students_amount, min_grade, max_grade, average):

        year_stat = await self.session.execute(
            select(YearStatistics).where(
                YearStatistics.university_specialization_id == university_specialization.id,
                YearStatistics.year == year,
                YearStatistics.concurs_type == getattr(ConcursEnum, specialization_type.upper())
            )
        )
        year_stat = year_stat.scalars().first()

        if year_stat:
            year_stat.students_amount = students_amount
            year_stat.min_pass_score = min_grade
            year_stat.max_pass_score = max_grade
            year_stat.average_pass_score = average
        else:
            year_stat = YearStatistics(
                university_specialization_id=university_specialization.id,
                concurs_type=getattr(ConcursEnum, specialization_type.upper()),
                year=year,
                students_amount=students_amount,
                min_pass_score=min_grade,
                max_pass_score=max_grade,
                average_pass_score=average
            )
            self.session.add(year_stat)
        await self.session.commit()


class UniversityReader(CommonRepo):

    async def get_universities(
            self,
            limit: int = None,
            offset: int = None
    ):
        query = (
            select(University)
            .group_by(University)
            .order_by(self.latest_date(entity=University).desc())
            .limit(limit)
            .offset(offset)
        )
        total_qty = await self.session.execute(
            select(func.count())
        )
        result = await self.session.execute(query)
        return result.scalars().all(), total_qty.scalar_one()

    async def get_university(self, university_id: UUID) -> University | None:
        query = (
            select(University)
            .select_from(University)
            .distinct(University.id)
            .where(University.id == university_id)
        )
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def get_university_by_code_or_create(self, university_code: str) -> University | None:
        query = (
            select(University)
            .select_from(University)
            .distinct(University.id)
            .where(University.code == university_code)
        )
        result = await self.session.execute(query)

        university = result.scalars().one_or_none()

        if university is None:
            university = University(code=university_code)
            self.session.add(university)
            await self.session.commit()

        return university


class UniversitySpecializationRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_university_specialization_or_create(self, university, specialization):
        university_specialization = await self.session.execute(
            select(UniversitySpecialization).where(
                UniversitySpecialization.university_id == university.id,
                UniversitySpecialization.specialization_id == specialization.id
            )
        )
        university_specialization = university_specialization.scalars().first()

        if university_specialization is None:
            university_specialization = UniversitySpecialization(
                university_id=university.id,
                specialization_id=specialization.id
            )
            self.session.add(university_specialization)
            await self.session.commit()

        return university_specialization
