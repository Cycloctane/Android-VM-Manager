from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TaskInfo(BaseModel):
    task_id: int
    task_name: str
    is_loop: bool
    controller: Optional[str] = None
    description: Optional[str] = None


class TaskMsg(BaseModel):
    adb_task_id: int
    celery_uuid: str
    launch_at: datetime
