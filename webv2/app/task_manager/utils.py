from adb_shell.adb_device import AdbDeviceTcp
from configparser import ConfigParser

conf = ConfigParser()
conf.read("config.conf", encoding="utf-8")

MITM_PROXY_HOST = conf.get('adb', 'mitm_proxy_host')

def adb_set_proxy(conn: AdbDeviceTcp) -> None:
    if conn.available:
        conn.shell(f"settings put global http_proxy {MITM_PROXY_HOST}")