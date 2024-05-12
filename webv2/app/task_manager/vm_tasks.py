import libvirt
from libvirt import virDomain, virConnect
from configparser import ConfigParser

from .main import celery_app

conf = ConfigParser()
conf.read("config.conf", encoding="utf-8")

QEMU_PATH = conf.get('libvirt', 'qemu_path')

class VMTasks:

    @staticmethod
    @celery_app.task(ignore_result=True)
    def vm_poweron(name: str):
        conn: virConnect = libvirt.open(QEMU_PATH)
        vm: virDomain =  conn.lookupByName(name)
        vm.create()
        conn.close()

    @staticmethod
    @celery_app.task(ignore_result=True)
    def vm_poweroff(name: str):
        conn: virConnect = libvirt.open(QEMU_PATH)
        vm: virDomain =  conn.lookupByName(name)
        vm.destroy()
        conn.close()
