import remote_connect as rc
def upload_file(cf,rf):
    # 创建SFTP客户端
    sftp = rc.ssh_client.open_sftp()
    sftp.put(cf,rf)
    # sftp.close()
# 文件下载
def download_file(rf,cf):
    sftp = rc.ssh_client.open_sftp()
    sftp.get(rf,cf)
    # sftp.close()

