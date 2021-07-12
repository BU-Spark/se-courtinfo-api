from celery import Celery

from app.core import config

celery_app = Celery("worker", broker=config.REDIS_DB_URL,
                    backend=f'db+${config.SQLALCHEMY_DATABASE_URI}')

celery_app.conf.task_routes = {"app.tasks.*": "main-queue"}
