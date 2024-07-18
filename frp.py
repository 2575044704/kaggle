# 定义配置文件内容
#使用的库
from pathlib import Path
import subprocess
import shutil
import os
import time
import re
import gc
import requests
import zipfile
import threading
import time
import socket
from concurrent.futures import ProcessPoolExecutor
use_frpc = True
frp_token = "****"   # 这里填服务器密码（token）
port1 = "00000"   # 这里填第一个端口
port2 = "00000"   # 这里填第二个端口


config = f"""
[common]
server_addr = 154.44.10.30
server_port = 7500
token = {frp_token} 

[sdwebuip_{port1}] 
type = tcp
local_ip = 127.0.0.1
local_port = 7860
remote_port = {port1} 

[sdwebuip_{port2}] 
type = tcp
local_ip = 127.0.0.1
local_port = 7861
remote_port = {port2} 
"""
print(config)

file_path = './cyanfrp.ini'

# 将配置内容写入文件
with open(file_path, 'w') as config_file:
    config_file.write(config)

print(f"配置文件已创建为 {file_path}")
def install_Frpc(port, use_frpc):
    if use_frpc:
        !cp /kaggle/input/d/yiyiooo/net-tools/frpc /kaggle/working
        !cp /kaggle/input/net-tools/frpc /kaggle/working
        subprocess.run(['chmod', '+x', '/kaggle/working/frpc'], check=True)
        print(f'正在启动frp ，端口{port}')
        !sleep 2 
        subprocess.Popen(['/kaggle/working/frpc', '-c', './cyanfrp.ini'])
port_all = port1 + "、" + port2
install_Frpc(port_all, use_frpc)
