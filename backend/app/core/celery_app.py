from celery import Celery

from app.core import config

celery_app = Celery("worker", broker=config.REDIS_DB_URL,
                    backend=f'db+postgresql://{config.POSTGRES_USER_NAME}:{config.POSTGRES_PASSWORD}@'
                            f'{config.POSTGRES_DB_URL_PORT}/{config.POSTGRES_DB_NAME}')

celery_app.conf.task_routes = {"app.tasks.*": "main-queue"}
