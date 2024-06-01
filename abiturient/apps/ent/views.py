from fastapi import UploadFile, status, File
from fastapi.responses import Response

from abiturient.utils.redis_utils import get_redis_connector
from .tasks import async_process_pdf


async def parse_pdf(file: UploadFile = File(...),
                    ) -> Response:
    file_bytes = await file.read()
    get_redis_connector().set(file.filename, file_bytes)
    task = await async_process_pdf.kiq(file.filename)
    return Response(status_code=status.HTTP_202_ACCEPTED)
