"""
You can add your own adb task to this file!
Inherit "ADBTask" to create a new adb task.
Write basic information of the task to "task_info" property.
Define what to do by overriding setup() and loop() methods, so that the ADBController can handle your task.
Get your ADB connection by using "self.conn". Set up proxy config for mitmproxy by "adb_set_proxy"
Finally, register your task to task_list at the bottom of this file.
"""

from abc import ABC, abstractmethod
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from time import sleep
from typing import TypeAlias
from os import path
from configparser import ConfigParser

from .model import TaskInfo
from .utils import adb_set_proxy

conf = ConfigParser()
conf.read("config.conf", encoding="utf-8")

KEY_PATH = conf.get('adb', 'key_path')

class ADBTask(ABC):

    task_info: TaskInfo = NotImplemented

    def __init__(self, ip: str) -> None:
        self.conn = AdbDeviceTcp(ip)
        key_path: str = KEY_PATH
        with open(path.join(key_path, "adbkey.pub")) as pub, open(path.join(key_path, "adbkey")) as priv:
            self.conn.connect(rsa_keys=[PythonRSASigner(pub.read(), priv.read())])

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def loop(self) -> None:
        pass


class ShutdownTask(ADBTask):

    task_info = TaskInfo(
        task_id=0, task_name="ADB shutdown", is_loop=False, controller="ADB",
        description="Shut down Android vm via adb shell"
    )

    def setup(self) -> None:
        self.conn.shell("poweroff")

    def loop(self) -> None:
        pass


class TencentNews(ADBTask):

    task_info = TaskInfo(
        task_id=1, task_name="Tencent News task", is_loop=True, controller="ADB",
        description="Run Tencent News"
    )

    def setup(self) -> None:
        adb_set_proxy(self.conn)
        self.conn.shell("monkey -p com.tencent.news 1")
        sleep(8.0)

    def loop(self) -> None:
        self.conn.shell("input tap 640 320")
        sleep(1.0)
        for _ in range(3):
            self.conn.shell("input swipe 640 500 640 200 500")
        self.conn.shell("input keyevent KEYCODE_BACK")
        sleep(1)
        self.conn.shell("input swipe 640 500 640 200 500")


task_list: list[type[ADBTask]] = [ShutdownTask, TencentNews] # Do not forget to register your task here!

TaskID: TypeAlias = int
task_dict: dict[TaskID, type[ADBTask]] = {i.task_info.task_id: i for i in task_list}
