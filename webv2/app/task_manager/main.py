from celery import Celery
from configparser import ConfigParser

conf = ConfigParser()
conf.read("config.conf", encoding="utf-8")

CELERY_BROKER_URL = conf.get('celery', 'celery_broker_url')
CELERY_RESULT_BACKEND = conf.get('celery', 'celery_result_backend')



celery_app = Celery('controller', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery_app.conf.update(task_track_started=True, task_serializer="msgpack", accept_content=["msgpack", "json"])
celery_app.set_default()
