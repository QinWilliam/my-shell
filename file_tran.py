
import remote_connect as rc
def upload_file(cf,rf):
    # 创建SFTP客户端
    sftp = rc.ssh_client.open_sftp()
    sftp.put(cf,rf)
    # sftp.close()
def download_file(rf,cf):
    sftp = rc.ssh_client.open_sftp()
    sftp.get(rf,cf)
    # sftp.close()
# client_file = 'C:\\Users\\z1337\\Desktop\\网址导航.txt'
# remote_file = '/tmp/navicat.txt'
# upload_file(client_file,remote_file)
# download_file(remote_file,client_file)
# rc.disconnect()
