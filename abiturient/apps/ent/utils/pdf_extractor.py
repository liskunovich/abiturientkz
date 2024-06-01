import asyncio
import abc
import datetime
import logging
from collections import deque
import re
import io
import fitz

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s")


class Extractor(abc.ABC):
    _file = None

    def __init__(self, file: str | io.BytesIO) -> None:
        self._file = file

    @staticmethod
    def _color_output(msg):
        return f'\033[1;33m{msg}\033[0m'


class TitleExtractor(Extractor):
    titles_deque: deque = deque()
    async def _extract_titles(self, page):
        # pattern = re.compile(r'(?P<specialization>B\d{3}(?: \([^)]+\))? - .+)|(?P<university>\d{3} - .+)')
        pattern = re.compile(r'(?P<specialization>[A-Z]{1,2}\d{3}(?: \([^)]+\))? - .+)|(?P<university>\d{3} - .+)')
        words = page.get_textpage().extractText()
        matches = pattern.finditer(words)

        current_specialization = None
        for match in matches:
            specialization = match.group('specialization')
            university = match.group('university')

            if specialization:
                current_specialization = specialization.strip()
                self.titles_deque.append({'specialization': current_specialization, 'university': None})
            if university and len(self.titles_deque) > 0:
                self.titles_deque[-1]['university'] = university.split('-')[0].strip()

    async def get_specializations_titles(self) -> deque:

        logging.info(self._color_output('EXTRACTING SPECIALIZATIONS'))

        with fitz.open(stream=self._file, filetype='pdf') as doc:
            for page in doc:
                # if page.number < 856: continue
                # if page.number >= 858: break
                await self._extract_titles(page)
        return self.titles_deque


class TableExtractor(Extractor):
    specializations = {}
    start_page: int
    end_page: int
    year: int

    _specializations_titles: deque
    _last_used_university: str = ''
    _last_used_title: str
    _last_used_type: str

    def __init__(self, file: str | io.BytesIO,
                 start_page: int = 0,
                 end_page: int = 5,
                 year: int = datetime.datetime.now().year) -> None:
        super().__init__(file)
        self.start_page = start_page
        self.end_page = end_page
        self.year = year

    async def __call__(self, *args, **kwargs):
        self._specializations_titles = await TitleExtractor(self._file).get_specializations_titles()
        await self._specializations_init()
        return self

    async def _specializations_init(self) -> None:
        logging.info(self._color_output('[1/2] INITIALIZATION'))
        self._last_used_type = 'common'

        self.specializations.setdefault(self.year, {})

        for title_dict in self._specializations_titles:
            specialization_code, university = title_dict.get('specialization'), title_dict.get('university')
            if not self._last_used_university: self._last_used_university = university
            if specialization_code:
                self.specializations[self.year].setdefault(specialization_code, {
                    'common': {},
                    'rural_quota': {}
                })

    async def _update_or_setdefault_key(self, row) -> None:
        key = self.specializations[self.year][self._last_used_title][self._last_used_type]

        if self._last_used_university:
            key.setdefault(self._last_used_university, [])
            key[self._last_used_university].append(row[-1])
        else:
            key.setdefault(row[-1], [])
            key[row[-1]].append(row[len(row) - 2])

    async def _update_specializations(self, tables) -> None:
        for table in tables:
            for row in table.extract():
                if row[0] == 'ОБЩИЙ КОНКУРС':
                    self._last_used_type = 'common'
                    if self._specializations_titles:
                        title_dict = self._specializations_titles.popleft()
                        title = title_dict.get('specialization').strip()
                        specialization_university = title_dict.get('university')

                        if title:
                            self._last_used_title = title
                        if specialization_university:
                            self._last_used_university = specialization_university
                        else:
                            self._last_used_university = ''

                elif row[0] == 'СЕЛЬСКАЯ КВОТА':
                    self._last_used_type = 'rural_quota'

                if (row[1] is not None and len(row[1]) == 9 and  # row[1], len(row[1]) - ИКТ
                        row[len(row) - 1] is not None):  # row[len(row) - 1] - балл
                    await self._update_or_setdefault_key(row)

    async def extract_table(self) -> None:
        logging.info(self._color_output('[2/2] PARSING STARTED'))
        with fitz.open(stream=self._file, filetype='pdf') as doc:
            for page in doc:
                if page.number < self.start_page: continue
                if page.number >= self.end_page: break
                tables = page.find_tables()
                await self._update_specializations(tables)

    async def get_specializations(self):
        if self.specializations:
            return self.specializations

