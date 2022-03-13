import urllib.request
import subprocess
import sys
import socket
import requests
from random import randrange

def printf(*args):
    for it in args:
        print(args)


ostype = 0
if (sys.platform.startswith("linux")):
    print("[INFO]Linux detected.")
    ostype = 1
elif (sys.platform.startswith("win32")):
    print("[INFO]Native windows detected.")
    ostype = 2
elif (sys.platform.startswith("cygwin")):
    print("[INFO]Cygwin detected.")
    ostype = 3
else:
    print("[FATL]Go get a windows laptop and install linux on it, or sponsor the maintainer the device you use for testing.\n暂不支持该系统诊断")
    print("[FATL]Exiting Now...")
    exit

isConnected = 0

if (ostype == 1):
    if ("DLUT-EDA" in subprocess.check_output("iwgetid").decode('utf-8')):
        isConnected = 1
elif ("DLUT-EDA" in subprocess.check_output("netsh wlan show interfaces").decode('utf-8')):
        isConnected = 1

if (isConnected == 1):
    print("[INFO]WLAN已连接。继续测试...")
else:
    print("[WARN]WLAN未连接！")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("202.118.66.6", 53))
    ip = s.getsockname()[0]
except socket.error as exc:
    print("[WARN]DNS connection error!")
    print("[WARN]", exc)
finally:
    s.close()
print("[INFO]IP addr:", ip)

if (ostype == 1):
    with open('/etc/resolv.conf') as f:
        if "202.118.66.6" in f. read():
            print("[INFO]DNS Settings OK")
        else:
            print("[WARN]DNS is not school provided. Might occur block.")
elif ("202.118.66.6" in subprocess.check_output("ipconfig /all").decode('utf-8')):
    print("[INFO]DNS setting might be OK")
else:
    print("[WARN]DNS is not school provided. Might occur block.")


session =requests.Session()
session.trust_env = False
key = str(randrange(1,100000))
try:
    r = session.post('http://172.20.20.1:801/include/auth_action.php?k='+key,
        data={"action":"get_online_info","key":key},timeout=3)
except Exception as exc:
    print("[WARN]error connecting to auth server\n[WARN]",exc)
print('[INFO]',r.text)

x = urllib.request.getproxies()
if (x!={}):
    print("Proxy settings is not empty. Try clearing the settings. \n 存在系统代理设置，可尝试清除。")

