from celery import Celery

from app.core import config

celery_app = Celery("worker", broker=f"redis://{config.REDIS_URL_PORT_DB}",
                    backend=f'db+postgresql://{config.POSTGRES_USER_NAME}:{config.POSTGRES_PASSWORD}@postgres:5432'
                            f'/postgres')

celery_app.conf.task_routes = {"app.tasks.*": "main-queue"}
