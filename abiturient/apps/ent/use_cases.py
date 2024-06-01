import statistics

from abiturient.apps.ent.utils.pdf_extractor import TableExtractor
from abiturient.infra.repositories.postgresql.pdf import (UniversityReader,
                                                          SpecializationReader,
                                                          YearStatisticsWriter,
                                                          UniversitySpecializationRepo)

from abiturient.utils.use_case import BaseUseCaseWithSession


class ExtractPDFUseCase:
    async def __call__(self,
                       file,
                       year: int,
                       *args,
                       **kwargs):
        table = await TableExtractor(file, start_page=0, end_page=1000, year=year)()  # TODO: AutoFill From Query
        await table.extract_table()
        return await table.get_specializations()


class FillStatisticUseCase(BaseUseCaseWithSession):
    async def __call__(self, data, *args, **kwargs):
        for year, specializations in data.items():
            for specialization_name, types in specializations.items():
                for specialization_type, universities in types.items():
                    for university_code, grades in universities.items():
                        if grades:
                            grades_array = [int(x) for x in grades if x is not None] or [0, 0, 0]
                            average = statistics.fmean(grades_array)
                            min_grade = min(grades_array)
                            max_grade = max(grades_array)
                            students_amount = len(grades_array)

                            await self._create_or_update_statistic(
                                year=year,
                                specialization_title=specialization_name,
                                specialization_type=specialization_type,
                                university_code=university_code,
                                students_amount=students_amount,
                                min_grade=min_grade,
                                max_grade=max_grade,
                                average=average
                            )

    async def _create_or_update_statistic(self, year, specialization_title,
                                          specialization_type, university_code, students_amount,
                                          min_grade, max_grade, average):

        university = await UniversityReader(self.session).get_university_by_code_or_create(university_code)

        specialization = await SpecializationReader(self.session).get_specialization_by_title_or_create(
            specialization_title)

        university_specialization = await (UniversitySpecializationRepo(self.session)
                                           .get_university_specialization_or_create(university, specialization))

        year_stat = await YearStatisticsWriter(self.session).create_or_update(
            university_specialization, specialization_type, year,
            students_amount, min_grade, max_grade, average
        )
