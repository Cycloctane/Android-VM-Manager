from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from ..model import Message, VMPowerStatus, VMInfo, VMStatus, VMTaskStatus, TaskInfo, VMTaskRequest
from ..vm_controller import VMController


router = APIRouter(tags=["VMs"], default_response_class=ORJSONResponse)


@router.get("/vms")
async def get_vm_list() -> list[VMInfo]:
    return VMController.get_vm_list()


@router.get("/vms/{name}")
async def get_vm_status(name: str) -> VMStatus:
    return await VMController.get_vm_status(name)


@router.get("/vms/{name}/power")
async def get_vm_power_status(name: str) -> VMPowerStatus:
    return VMController.get_vm_power_status(name)


@router.patch("/vms/{name}/power", status_code=202)
async def power_status_ctrl(name: str, request_status: VMPowerStatus) -> Message:
    VMController.vm_power_control(name, request_status)
    return Message(msg="task accepted")


@router.get("/vms/{name}/task")
async def get_vm_current_task(name: str) -> VMTaskStatus:
    return await VMController.get_vm_task_status(name)


@router.patch("/vms/{name}/task", status_code=202)
async def vm_task_ctrl(name: str, request_task: VMTaskRequest) -> Message:
    await VMController.vm_task_control(name, request_task)
    return Message(msg="task accepted")


@router.get("/tasks", status_code=200)
async def list_task() -> list[TaskInfo]:
    return VMController.get_task_list()
