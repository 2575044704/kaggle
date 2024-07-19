# 使用的库
import subprocess
import os

use_frpc = True
frp_token = "****"   # 这里填服务器密码（token）
port1 = "00000"   # 这里填第一个端口
port2 = "00000"   # 这里填第二个端口

config = f"""
[common]
server_addr = 45.194.32.78
server_port = 7000
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
        subprocess.run(['cp', '/kaggle/input/d/yiyiooo/net-tools/frpc', '/kaggle/working'])
        subprocess.run(['cp', '/kaggle/input/net-tools/frpc', '/kaggle/working'])
        subprocess.run(['chmod', '+x', '/kaggle/working/frpc'], check=True)
        print(f'正在启动frp ，端口{port}')
        subprocess.run(['sleep', '2'])
        subprocess.Popen(['/kaggle/working/frpc', '-c', './cyanfrp.ini'])

port_all = port1 + "、" + port2
install_Frpc(port_all, use_frpc)
