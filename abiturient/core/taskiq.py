from redis import ConnectionPool

from abiturient.utils.config_reader import get_config
# app = Celery('apps',
#              include=['abiturient.apps.ent.tasks'],
#              broker=)
#
# app.conf.update(
#     result_backend=get_config().ABITURIENT_CELERY_RESULT_BACKEND,
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='Asia/Almaty',
#     enable_utc=True,
# )
# app.autodiscover_tasks()
from dotenv import load_dotenv
import taskiq_fastapi
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend


redis_async_result = RedisAsyncResultBackend(
    redis_url=get_config().ABITURIENT_CELERY_RESULT_BACKEND,
)

broker = ListQueueBroker(
    url=get_config().ABITURIENT_CELERY_BROKER_URL,
).with_result_backend(result_backend=redis_async_result)

taskiq_fastapi.init(broker, 'abiturient.utils.app_start:get_current_app')
