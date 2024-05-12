from pydantic import BaseModel
from typing import Optional
import redis.asyncio as redis
from celery import result

from ..db import redis_pool
from ..task_manager import TaskInfo, TaskMsg, task_dict


class VMPowerStatus(BaseModel):
    is_running: bool


class VMTaskStatus(BaseModel):
    on_task: bool
    task_uuid: Optional[str] = None
    current_task_info: Optional[TaskInfo] = None


class VMInfo(BaseModel):
    uuid: str
    name: str
    memory: int
    isAndroid: bool
    mac_address: str
    power_status: VMPowerStatus


class VMStatus(VMInfo):
    ip_address: Optional[str] = None
    task_info: Optional[VMTaskStatus] = None

    async def post_init(self) -> None: # must be manually invoked after instance created.
        if self.isAndroid and self.power_status.is_running:
            mac = self.mac_address.replace(':', '-')
            async with redis.Redis.from_pool(redis_pool) as redis_conn:
                ip: Optional[str] = await redis_conn.get(f"ip:{mac}")
                task_msg_json: Optional[str] = await redis_conn.get(f"task:{mac}")
            self.ip_address = ip
            if ip is None or task_msg_json is None:
                self.task_info = VMTaskStatus(on_task=False)
                return
            task_msg = TaskMsg.model_validate_json(task_msg_json)
            if result.AsyncResult(task_msg.celery_uuid).state != "STARTED":
                self.task_info = VMTaskStatus(on_task=False)
                return
            self.task_info = VMTaskStatus(on_task=True, task_uuid=task_msg.celery_uuid,
                                          current_task_info=task_dict[task_msg.adb_task_id].task_info)


class VMTaskRequest(BaseModel):
    on_task: bool
    request_task_id: Optional[int] = None


class Message(BaseModel):
    msg: str

