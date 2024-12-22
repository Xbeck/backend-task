from celery import Celery

from src.config import settings

###################################### 88 probels ######################################
########################################################################################
# FIFO -> first in first out
celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["src.tasks.tasks"],
    broker_connection_retry_on_startup = True
)



# celery -A app.tasks.celery_:celery_app worker --loglevel=INFO --pool=solo
