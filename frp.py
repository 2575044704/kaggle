## 提示（必看！！）：
## 1.使用前请先导入net tools工具，链接：https://www.kaggle.com/datasets/leaffallen/net-tools-new 
## 2.如果有问题联系qq2575044704
## 3.密码严禁分享给他人，禁止放在公开的互联网上。造成法律责任后果自负
## 4.使用此frp代码，请勿将notebook设置为public(共享)，否则密码会泄露

import subprocess
import os
import threading
import requests

use_frpc = True
frp_token = "*******"   # 这里填服务器密码（token）
port1 = "00000"   # 这里填第一个端口
port2 = "00000"   # 这里填第二个端口

# URL of the file
url = 'https://hf-mirror.com/datasets/nyan102/kagglemodel/resolve/main/ip'
# Send a GET request to the URL
response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    # Store the content in the variable dynamic_ip
    dynamic_ip = response.text
    print(f"获取的IP为{dynamic_ip}，将使用此IP进行连接")  # Optional: print the content
else:
    print(f"出错了，联系管理员！ Status code: {response.status_code}")
# webui默认的local_port 为 7860，ComfyUI的local_port为8188，如果你想映射其它应用端口，请自行修改

config1 = f"""
[common]
server_addr = {dynamic_ip}
server_port = 7000
token = {frp_token} 
heartbeat_interval = 30
tcpKeepalive = 10
heartbeat_timeout = 43200

[sdwebuip_{port1}] 
type = tcp
local_ip = 127.0.0.1
local_port = 7860
remote_port = {port1} 
"""

config2 = f"""
[common]
server_addr = {dynamic_ip}
server_port = 7000
token = {frp_token} 
heartbeat_interval = 30
tcpKeepalive = 10
heartbeat_timeout = 43200

[sdwebuip_{port2}] 
type = tcp
local_ip = 127.0.0.1
local_port = 7861
remote_port = {port2} 
"""

with open('./cyanfrp1.ini', 'w') as config_file:
    config_file.write(config1)
with open('./cyanfrp2.ini', 'w') as config_file:
    config_file.write(config2)
print(f"配置文件已创建")
subprocess.run(['cp', '/kaggle/input/net-tools/frpc', '/kaggle/working'])
subprocess.run(['cp', '/kaggle/input/net-tools-new/frpc', '/kaggle/working'])
subprocess.run(['chmod', '+x', '/kaggle/working/frpc'], check=True)
def install_Frpc(file_path, port, use_frpc, log_file_path):
    if use_frpc:
        print(f'正在启动frp ，端口{port}')
        with open(log_file_path, 'w') as log_file:
            process = subprocess.Popen(['/kaggle/working/frpc', '-c', file_path], stdout=log_file, stderr=log_file)
        subprocess.run(['sleep', '4'])
        subprocess.run(['cat', log_file_path])
thread1 = threading.Thread(target=install_Frpc, args=('./cyanfrp1.ini', port1, use_frpc, '/kaggle/frp_log1.txt'))
thread2 = threading.Thread(target=install_Frpc, args=('./cyanfrp2.ini', port2, use_frpc, '/kaggle/frp_log2.txt'))
thread1.start()
thread2.start()
thread1.join()
thread2.join()

