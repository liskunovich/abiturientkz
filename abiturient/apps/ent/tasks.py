from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from abiturient.core.taskiq import broker

from abiturient.infra.db.database import async_session
from abiturient.core.settings import settings_instance
from abiturient.apps.ent.use_cases import ExtractPDFUseCase, FillStatisticUseCase
from abiturient.utils.redis_utils import get_redis_connector
from abiturient.utils.logger import get_logger


@broker.task
async def async_process_pdf(key: str,
                            session: AsyncSession = Depends(
                                async_session(settings_instance.db_url.unicode_string(),
                                              settings_instance))):
    file = get_redis_connector().getdel(key)
    year = int(key.strip().split('.')[0])
    extract_use_case = await ExtractPDFUseCase()(file, year)
    await FillStatisticUseCase(session)(extract_use_case)
    return extract_use_case
