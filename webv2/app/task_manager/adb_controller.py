import asyncio
from datetime import datetime
from typing import Optional
from celery.result import AsyncResult
import redis.asyncio as redis
import signal
from uuid import uuid4

from .main import celery_app
from .model import TaskMsg
from .adb_tasks import ADBTask, task_dict
from ..db import redis_pool
from ..exception import AppException


class ADBController:

    @staticmethod
    @celery_app.task()
    def __launch(adb_task_id: int, target_ip_address: str) -> None:
        adb_task_instance: ADBTask = task_dict[adb_task_id](target_ip_address)
        adb_task_instance.setup()
        if adb_task_instance.task_info.is_loop:
            while 1:
                adb_task_instance.loop()

    @staticmethod
    async def adb_task_handler(adb_task_id: Optional[int], target_mac_address: str) -> None:
        if adb_task_id is None or task_dict.get(adb_task_id) is None: raise AppException("Invalid task id")
        celery_uuid: str = str(uuid4())
        task_msg = TaskMsg(adb_task_id=adb_task_id, celery_uuid=celery_uuid, launch_at=datetime.now())
        mac = target_mac_address.replace(':', '-')
        async with redis.Redis.from_pool(redis_pool) as redis_conn:
            redis_result = await asyncio.gather(redis_conn.get(f"ip:{mac}"),
                                                redis_conn.set(f"task:{mac}", task_msg.model_dump_json()))
            target_ip_address: str = redis_result[0]
        print(target_ip_address)
        ADBController.__launch.apply_async(args=(adb_task_id, target_ip_address), task_id=celery_uuid)

    @staticmethod
    def terminate(task_uuid: str) -> None:
        task = AsyncResult(task_uuid)
        if task.state == "STARTED":
            task.revoke(terminate=True, signal=signal.SIGQUIT)
