import remote_connect as rc
rc.connect('192.168.10.19','root','123666')
def exec_cmd(cmd):
    stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
    print(stdout.read().decode("utf-8"))
    # print(stderr.read().decode("utf-8"))
# while True:
#         cmd = input('[root@localhost]#')
#         if cmd == 'exit' or cmd == 'q':
#             break
#         exec_cmd(cmd)
# 关闭SSH连接
# rc.disconnect()
