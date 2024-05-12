import libvirt
from libvirt import virConnect, virDomain, libvirtError
from configparser import ConfigParser
from fastapi import HTTPException
from xml.dom.minidom import parseString

from .model import VMInfo, VMStatus, VMPowerStatus, VMTaskRequest, VMTaskStatus, TaskInfo
from ..task_manager import VMTasks, ADBController, task_dict
from ..exception import AppException

conf = ConfigParser()
conf.read("config.conf", encoding="utf-8")

QEMU_PATH = conf.get('libvirt', 'qemu_path')


class VMController:

    @staticmethod
    def __load_vm_info(vm: virDomain) -> VMInfo:
        return VMInfo(uuid=vm.UUIDString(), name=vm.name(), memory=vm.maxMemory()//1024, power_status=VMPowerStatus(is_running=bool(vm.isActive())),
                       mac_address=parseString(vm.XMLDesc()).documentElement.getElementsByTagName("mac")[0].getAttribute("address"),
                       isAndroid=("android-x86" in parseString(vm.XMLDesc()).documentElement.getElementsByTagName("libosinfo:os")[0].getAttribute("id")))

    @staticmethod
    def get_vm_list() -> list[VMInfo]:
        conn: virConnect = libvirt.open(QEMU_PATH)
        domainsList: list[virDomain] =  conn.listAllDomains()
        conn.close()
        return [VMController.__load_vm_info(vm) for vm in domainsList]

    @staticmethod
    def get_task_list() -> list[TaskInfo]:
        return [task_dict[i].task_info for i in task_dict]

    @staticmethod
    async def get_vm_status(name: str) -> VMStatus:
        conn: virConnect = libvirt.open(QEMU_PATH)
        try: vm: virDomain =  conn.lookupByName(name)
        except libvirtError: raise HTTPException(404, detail="Domain not found")
        else: vm_status = VMStatus.model_validate(VMController.__load_vm_info(vm).model_dump())
        finally: conn.close()
        await vm_status.post_init()
        return vm_status

    @staticmethod
    def get_vm_power_status(name: str) -> VMPowerStatus:
        conn: virConnect = libvirt.open(QEMU_PATH)
        try: vm: virDomain =  conn.lookupByName(name)
        except libvirtError: raise HTTPException(404, detail="Domain not found")
        else: return VMPowerStatus(is_running=bool(vm.isActive()))
        finally: conn.close()

    @staticmethod
    async def get_vm_task_status(name: str) -> VMTaskStatus:
        vm_status = await VMController.get_vm_status(name)
        if vm_status.task_info is None:
            raise HTTPException(400, detail="VM unavailable")
        return vm_status.task_info

    @staticmethod
    def vm_power_control(name: str, request_power_status: VMPowerStatus) -> None:
        current_status: VMPowerStatus = VMController.get_vm_power_status(name)
        if current_status.is_running and not request_power_status.is_running:
            VMTasks.vm_poweroff.delay(name)
        elif not current_status.is_running and request_power_status.is_running:
            VMTasks.vm_poweron.delay(name)

    @staticmethod
    async def vm_task_control(name: str, request_task: VMTaskRequest) -> None:
        vm: VMStatus = await VMController.get_vm_status(name)
        if vm.task_info is None or vm.ip_address is None: raise HTTPException(400, detail="VM unavailable")
        if request_task.on_task is False:
            if vm.task_info.on_task is False or vm.task_info.task_uuid is None: raise HTTPException(400, detail="Current task not found")
            ADBController.terminate(vm.task_info.task_uuid)
        elif request_task.on_task is True:
            if vm.task_info.on_task is True: raise HTTPException(400, detail="VM busy")
            try: await ADBController.adb_task_handler(request_task.request_task_id, vm.mac_address)
            except (AppException) as e: raise HTTPException(status_code=200, detail=str(e))

