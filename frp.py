# 使用的库
import subprocess
import os
import threading

use_frpc = True
frp_token = "****"   # 这里填服务器密码（token）
port1 = "00000"   # 这里填第一个端口
port2 = "00000"   # 这里填第二个端口

config1 = f"""
[common]
server_addr = 45.194.32.78
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
server_addr = 45.194.32.78
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
subprocess.run(['cp', '/kaggle/input/d/yiyiooo/net-tools/frpc', '/kaggle/working'])
subprocess.run(['cp', '/kaggle/input/net-tools/frpc', '/kaggle/working'])
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

