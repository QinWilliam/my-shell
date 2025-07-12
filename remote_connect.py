import paramiko
# 连接到远程服务端
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def connect(host,user,password):
    ssh_client.connect(hostname=host, username=user, password=password)
    # stdin, stdout, stderr = ssh_client.exec_command('ls /')
    # print(stdout.read().decode("utf-8"))
    # ssh_client.close()
    # print(f"{user}@{host} is connected")
    return host
def disconnect():
    print("SSH is disconnected")
    ssh_client.close()

