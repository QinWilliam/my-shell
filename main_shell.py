import sys
from PyQt5.QtGui import QFont, QIcon
import remote_connect as rc
import file_tran as ftr
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QDialog,
                             QTextEdit, QInputDialog, QComboBox)
class FileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("文件管理")
        self.setGeometry(1000, 200, 800, 600)
        self.op1 = QLabel("请输入文件名:", self)
        self.op1.setGeometry(10, 10, 200, 50)
        self.op1.setFont(QFont("Arial", 12))
        self.op2 = QLabel("请选择操作:", self)
        self.op2.setGeometry(390, 10, 200, 50)
        self.op2.setFont(QFont("Arial", 12))
        try:
            self.file_info = QLineEdit(self)
            self.file_info.setClearButtonEnabled(True)
            self.file_info.setGeometry(10, 65, 380, 50)
            self.file_info.setPlaceholderText(r"文件名(避免使用* ? < > | ” ' \)")
        except SyntaxWarning as e:
            print(e)
        self.bt1 = QPushButton("创建文件", self)
        self.bt2 = QPushButton("创建目录", self)
        self.bt3 = QPushButton("重命名", self)
        self.bt4 = QPushButton("查看", self)
        for button in [self.bt1, self.bt2, self.bt3, self.bt4]:
            button.setFont(QFont("Arial", 11))
            self.bt1.setStyleSheet("background-color:green")
            self.bt1.setGeometry(400, 65, 90, 50)
            self.bt2.setStyleSheet("background-color:yellow")
            self.bt2.setGeometry(500, 65, 90, 50)
            self.bt3.setStyleSheet("background-color:pink")
            self.bt3.setGeometry(600, 65, 90, 50)
            self.bt4.setStyleSheet("background-color:gray")
            self.bt4.setGeometry(700, 65, 90, 50)
        self.show_info = QTextEdit(self)
        self.show_info.setGeometry(10, 120, 780, 700)

        self.bt1.clicked.connect(self.bt1_showed)
        self.bt2.clicked.connect(self.bt2_showed)
        self.bt3.clicked.connect(self.bt3_showed)
        self.bt4.clicked.connect(self.bt4_showed)
    def bt1_showed(self):
        text = self.file_info.text()
        if not text:
            self.show_info.setText("文件名不能为空")
        else:
            cmd = "touch  "+text
            stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
            print(stdout.readline())
            self.show_info.setText(f"{text}文件创建成功")
    def bt2_showed(self):
        text = self.file_info.text()
        if not text:
            self.show_info.setText("目录名不能为空")
        else:
            cmd = "mkdir -p  "+text
            stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
            print(stdout.readline())
            self.show_info.setText(f"{text}目录创建成功")
    def bt3_showed(self):
        text = self.file_info.text()
        if text:
            new_name, ok = QInputDialog.getText(self, "重命名", "请输入新文件名：")
            # 如果用户点击了 OK 按钮并且输入了文本
            if ok and new_name:
                cmd = "mv  " + text + "  " + new_name
                stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
                print(stdout.readline())
            self.show_info.setText(f"文件已重命名为{new_name}")
        else:
            self.show_info.setText("文件或目录名不能为空")
    def bt4_showed(self):
        text = self.file_info.text()
        try:
            if text:
                cmd = "cat  "+text
                stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
                self.show_info.setText(stdout.readline())
            else:
                self.show_info.setText("文件或目录名不能为空")
        except Exception as e:
            self.show_info.setText("请检查文件是否存在",e)
class UsersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户管理")
        self.setGeometry(1000, 200, 800, 600)
        # 创建下拉列表并添加选项
        self.lb_op1 = QLabel("请输入用户名:",self)
        self.lb_op1.setGeometry(10,10,200,50)
        self.lb_op1.setFont(QFont("Arial",12))
        self.lb_op2 = QLabel("请选择操作:",self)
        self.lb_op2.setGeometry(410,10,200,50)
        self.lb_op2.setFont(QFont("Arial",12))
        self.user_info = QLineEdit(self)
        self.user_info.setClearButtonEnabled(True)
        self.user_info.setGeometry(10, 65, 400, 50)
        self.user_info.setPlaceholderText("按Enter确认")
        self.combo = QComboBox(self)
        self.combo.addItems(["","添加用户", "删除用户","查看用户组","查看所有用户"])  # 静态添加选项
        self.combo.setGeometry(410,65,380,50)
        self.combo.setFont(QFont("Arial",11))
        self.cmd_info = QTextEdit(self)
        self.cmd_info.setGeometry(10,120,780,500)
        self.cmd_info.setFont(QFont("Arial",11))
        # 连接信号槽：当下拉选项变化时更新标签
        self.combo.currentTextChanged.connect(self.update_cmd)
    def update_cmd(self,text):
        # lambda表达式也可以 print(text)
        text_user = self.user_info.text()
        self.combo.setCurrentText(text)
        try:
            if not text_user and text != "查看所有用户":
                self.cmd_info.setText("操作指定用户名时不能为空")
            elif  text == "添加用户":
                cmd = f"useradd {text_user}"
                stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
                print(stdout.read().decode("utf-8"))
                self.cmd_info.setText(f"{text_user}用户添加成功！")
            elif text == "删除用户":
                cmd = f"userdel {text_user}"
                stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
                print(stdout.read().decode("utf-8"))
                self.cmd_info.setText(f"{text_user}用户删除成功！")
            elif text == "查看用户组":
                cmd = f"groups {text_user}"
                stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
                self.cmd_info.setText(stdout.read().decode("utf-8"))
            elif text == "查看所有用户":
                cmd = "awk -F: '$3 >= 1000 && $3 < 60000 {print $1,$4}' /etc/passwd"
                stdin, stdout, stderr = rc.ssh_client.exec_command(cmd)
                self.cmd_info.setText(stdout.read().decode("utf-8"))
            else:
                self.cmd_info.setText("请选择正确选项")
        except Exception as e:
            self.cmd_info.setText(f"异常处理错误{e}")
class ServicesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("服务管理")
        self.setGeometry(1000, 200, 800, 700)
        # 创建下拉列表并添加选项
        self.lb_op1 = QLabel("请输入服务名:", self)
        self.lb_op1.setGeometry(10, 10, 200, 50)
        self.lb_op1.setFont(QFont("Arial", 12))
        self.lb_op2 = QLabel("请选择操作:", self)
        self.lb_op2.setGeometry(400, 10, 200, 50)
        self.lb_op2.setFont(QFont("Arial", 12))
        self.server_info = QLineEdit(self)
        self.server_info.setClearButtonEnabled(True)
        self.server_info.setGeometry(10, 65, 350, 50)
        self.server_info.setPlaceholderText("如httpd(Enter)")
        self.server_info.setFont(QFont("Arial", 11))
        self.bt1 = QPushButton("启动", self)
        self.bt2 = QPushButton("状态", self)
        self.bt3 = QPushButton("关闭", self)
        self.bt4 = QPushButton("禁用", self)
        self.bt5 = QPushButton("服务日志", self)
        for btn in [self.bt1,self.bt2,self.bt3,self.bt4,self.bt5]:
            btn.setFont(QFont("Arial", 12))
            self.bt1.setStyleSheet("background-color:green")
            self.bt1.setGeometry(400,65,60,50)
            self.bt2.setStyleSheet("background-color:gray")
            self.bt2.setGeometry(470,65,60,50)
            self.bt3.setStyleSheet("background-color:pink")
            self.bt3.setGeometry(540,65,60,50)
            self.bt4.setStyleSheet("background-color:red")
            self.bt4.setGeometry(610,65,60,50)
            self.bt5.setStyleSheet("background-color:yellow")
            self.bt5.setGeometry(680,65,110,50)
        self.bt1.clicked.connect(self.bt1_clicked)
        self.bt2.clicked.connect(self.bt2_clicked)
        self.bt3.clicked.connect(self.bt3_clicked)
        self.bt4.clicked.connect(self.bt4_clicked)
        self.bt5.clicked.connect(self.bt5_clicked)
        self.cmd_info = QTextEdit(self)
        self.cmd_info.setGeometry(10,120,780,580)
    def bt1_clicked(self):
        text = self.server_info.text()
        word = "systemctl start  "+text
        stdin, stdout, stderr = rc.ssh_client.exec_command(word)
        # print(stdout.read().decode("utf-8"))
        self.cmd_info.setText(stdout.read().decode("utf-8"))
        self.cmd_info.setText(f"{text}服务已开启!")
    def bt2_clicked(self):
        text = self.server_info.text()
        word = "systemctl status  "+text
        stdin, stdout, stderr = rc.ssh_client.exec_command(word)
        # print(stdout.read().decode("utf-8"))
        self.cmd_info.setText(stdout.read().decode("utf-8"))
    def bt3_clicked(self):
        text = self.server_info.text()
        word = "systemctl stop  "+text
        # self.cmd_info.setText(word)
        stdin, stdout, stderr = rc.ssh_client.exec_command(word)
        print(f"{text}服务已关闭!")
        self.cmd_info.setText(stdout.read().decode("utf-8"))
        self.cmd_info.setText(f"{text}服务已关闭!")
    def bt4_clicked(self):
        text = self.server_info.text()
        word = "systemctl disable  "+text
        # self.cmd_info.setText(word)
        stdin, stdout, stderr = rc.ssh_client.exec_command(word)
        print(f"{text}服务已禁用!")
        self.cmd_info.setText(stdout.read().decode("utf-8"))
        self.cmd_info.setText(f"{text}服务已禁用!")
    def bt5_clicked(self):
        text = self.server_info.text()
        word = "journalctl -u  "+text
        stdin, stdout, stderr = rc.ssh_client.exec_command(word)
        # print(stdout.read().decode("utf-8"))
        self.cmd_info.setText(stdout.read().decode("utf-8"))
"""系统监控子类和子窗口"""
class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 打开非模态窗口
        self.setWindowTitle("系统监控信息")
        self.setGeometry(1000, 200,1200, 1000)
        self.btn1 = QPushButton("CPU信息", self)
        self.btn1.setGeometry(0, 10, 1200, 30)
        self.btn1.clicked.connect(self.return_cpu)
        self.cpu_edit = QTextEdit(self)
        self.cpu_edit.setGeometry(0,40,1200,90)
        self.btn2 = QPushButton("内存信息", self)
        self.btn2.setGeometry(0, 130, 1200, 30)
        self.btn2.clicked.connect(self.return_mem)
        self.mem_edit = QTextEdit(self)
        self.mem_edit.setGeometry(0,160,1200,90)
        self.btn3 = QPushButton("负载均衡", self)
        self.btn3.setGeometry(0, 250, 1200, 30)
        self.btn3.clicked.connect(self.return_load)
        self.load_edit = QTextEdit(self)
        self.load_edit.setGeometry(0,280,1200,90)
        self.btn4 = QPushButton("系统进程", self)
        self.btn4.setGeometry(0, 370, 1200, 30)
        self.btn4.clicked.connect(self.return_psx)
        self.psx_edit = QTextEdit(self)
        self.psx_edit.setGeometry(0,400,1200,300)
        self.btn5 = QPushButton("磁盘冗余", self)
        self.btn5.setGeometry(0, 700, 1200, 30)
        self.btn5.clicked.connect(self.return_disk)
        self.fisk_edit = QTextEdit(self)
        self.fisk_edit.setGeometry(0,730,1200,300)
        for btn in [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5]:
            btn.setFont(QFont("Arial", 11))
            # btn.setStyleSheet("background-color:green")
        for control in [self.cpu_edit,self.mem_edit,self.load_edit,self.psx_edit,self.fisk_edit]:
            control.setFont(QFont("Arial", 12))
            control.setReadOnly(True)
            control.setStyleSheet("background-color:gray;")
        # central_widget1.setLayout(vbox)
    def return_cpu(self):
        stdin, stdout, stderr = rc.ssh_client.exec_command('cat /proc/cpuinfo|grep -E "cpu|model|cache"')
        cpu_info = stdout.read().decode("utf-8")
        self.cpu_edit.setText(cpu_info)
    def return_mem(self):
        stdin, stdout, stderr = rc.ssh_client.exec_command("free -h")
        mem_info = stdout.read().decode("utf-8")
        self.mem_edit.setText(mem_info)
    def return_psx(self):
        stdin, stdout, stderr = rc.ssh_client.exec_command("ps aux --sort=-%mem | head -10")
        psx_info = stdout.read().decode("utf-8")
        self.psx_edit.setText(psx_info)
    def return_disk(self):
        stdin, stdout, stderr = rc.ssh_client.exec_command("df -hT")
        disk_info = stdout.read().decode("utf-8")
        self.fisk_edit.setText(disk_info)
    def return_load(self):
        stdin, stdout, stderr = rc.ssh_client.exec_command("uptime | grep load | awk '{print $6,$7,$8,$9,$10,$11}'")
        load = stdout.read().decode("utf-8")
        self.load_edit.setText(load)
"""创建一个主窗口类，继承自 QMainWindow"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Shell")
        self.setGeometry(600, 300, 1150, 800)
        # 创建主窗口中的中央控件，QMainWindow 需要设置中央控件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # vbox_layout = QVBoxLayout()
        hbox_layout = QHBoxLayout()
        lb_ip = QLabel("IP地址:", self)
        lb_user = QLabel("用户名:",self)
        lb_pwd = QLabel("密码:",self)
        lb_cmd = QLabel("显示面板:",self)
        bt1 = QPushButton("远程连接", self)
        bt1.setFont(QFont("Arial", 12))
        bt1.setFixedSize(QSize(150, 40))
        bt1.setStyleSheet("background-color:green")
        bt1.clicked.connect(self.return_mes)
        bt2 = QPushButton("网络地址", self)
        bt2.setFont(QFont("Arial", 12))
        bt2.setFixedSize(QSize(150, 60))
        bt2.clicked.connect(self.return_network)
        bt9 =QPushButton("文件管理", self)
        bt9.setFont(QFont("Arial", 12))
        bt9.setFixedSize(QSize(150, 60))
        bt9.clicked.connect(self.dialog_file)
        bt3 = QPushButton("文件上传", self)
        bt3.setFont(QFont("Arial", 12))
        bt3.setFixedSize(QSize(150, 60))
        bt3.clicked.connect(self.open_file)
        bt4 = QPushButton("文件下载", self)
        bt4.setFont(QFont("Arial", 12))
        bt4.setFixedSize(QSize(150, 60))
        bt4.clicked.connect(self.save_file)
        bt5 = QPushButton("系统监控", self)
        bt5.setFont(QFont("Arial", 12))
        bt5.setFixedSize(QSize(150, 60))
        bt5.clicked.connect(self.open_no_modal)
        self.child_window = None  # 防止子窗口被回收
        bt6 = QPushButton("用户管理", self)
        bt6.setFont(QFont("Arial", 12))
        bt6.setFixedSize(QSize(150, 60))
        bt6.clicked.connect(self.open_users)
        self.child1_window = None  # 防止子窗口被回收
        bt7 = QPushButton("服务管理", self)
        bt7.setFont(QFont("Arial", 12))
        bt7.setFixedSize(QSize(150, 60))
        bt7.clicked.connect(self.open_services)
        self.child2_window = None  # 防止子窗口被回收
        bt8 = QPushButton("关闭连接", self)
        bt8.setFont(QFont("Arial", 13))
        bt8.setFixedSize(QSize(150, 40))
        bt8.setStyleSheet("background-color:red")
        bt8.clicked.connect(self.return_bt8)
        self.lb_word = QLabel(self)
        self.lb_word.setGeometry(150, 0, 1000, 50)
        self.lb_word.setAlignment(Qt.AlignCenter)
        self.lb_word.setStyleSheet("background-color:gray")
        for lb in [self.lb_word,lb_ip,lb_user,lb_pwd,lb_cmd,bt2,bt3,bt4,bt5,bt6,bt7,bt8,bt9]:
            lb.setFont(QFont("Arial", 11))
            lb_ip.setGeometry(30, 30, 100, 60)
            lb_user.setGeometry(30,60, 100, 60)
            lb_pwd.setGeometry(30, 90, 100, 60)
            lb_cmd.setGeometry(30, 140, 100, 60)
            bt2.setGeometry(0, 200, 100, 60)
            bt9.setGeometry(0, 280, 100, 50)
            bt3.setGeometry(0, 360, 100, 60)
            bt4.setGeometry(0, 430, 100, 60)
            bt5.setGeometry(0, 510, 100, 60)
            bt6.setGeometry(0, 590, 100, 60)
            bt7.setGeometry(0, 670, 100, 60)
            bt8.setGeometry(0, 750, 100, 60)
        self.ip_edit = QLineEdit(self)
        self.user_edit = QLineEdit(self)
        self.pwd_edit = QLineEdit(self)
        self.cmd_edit = QTextEdit(self)
        self.input_edit = QLineEdit(self)
        self.input_edit.setClearButtonEnabled(True)
        self.input_edit.setGeometry(155,740,990,50)
        self.input_edit.setFont(QFont("Arial", 11))
        self.input_edit.setPlaceholderText("请输入您想要执行的命令,按enter结束:")
        self.input_edit.setStyleSheet("border:1px solid;border-radius:15px")
        self.input_edit.returnPressed.connect(self.return_input)
        for line_edit in [self.ip_edit,self.user_edit,self.pwd_edit,self.cmd_edit]:
            line_edit.setFont(QFont("Arial", 10))
            line_edit.setPlaceholderText("请输入:")
            self.ip_edit.setGeometry(150,40,1000,35)
            self.user_edit.setGeometry(150,70,1000,35)
            self.pwd_edit.setGeometry(150,100,1000,35)
            self.cmd_edit.setGeometry(150,136,1000,600)
            self.cmd_edit.setPlaceholderText("This is a sample shell console")
            hbox_layout.addWidget(line_edit)
    def return_input(self):
        text = self.input_edit.text()
        stdin, stdout, stderr = rc.ssh_client.exec_command(text)
        input_ifo = stdout.read().decode("utf-8")
        self.cmd_edit.setText(input_ifo)
    def return_mes(self):
        ip = self.ip_edit.text()
        user = self.user_edit.text()
        pwd = self.pwd_edit.text()
        # print(ip,user,pwd)
        ssh1 = rc.connect(ip,user,pwd)
        self.setWindowTitle(f"My Shell~{ssh1}")
        self.lb_word.setText(f"{user}~Welcome to My Shell")
        self.cmd_edit.setPlaceholderText("Connecting successfully")
        self.input_edit.setEnabled(True)
        self.pwd_edit.clear() # 密码输入登录后被清空
    def return_network(self):
        stdin, stdout, stderr = rc.ssh_client.exec_command("ip a")
        net = stdout.read().decode("utf-8")
        self.cmd_edit.setText(net)

    # 创建模态窗口
    def dialog_file(self):
        dialog = FileDialog()
        dialog.exec_()

    def open_file(self):
        self.cmd_edit.clear() # 先清空命令行信息
        text, ok = QInputDialog.getText(self, "remote", "请输入文件远程地址：")
        # 如果用户点击了 OK 按钮并且输入了文本
        if ok and text:
            self.cmd_edit.setText(text)
            print(f"用户输入：{text}")
        file_name, _ = QFileDialog.getOpenFileName(self, "本地文件", "", "所有文件 (*);;文本文件 (*.txt)")
        if file_name:
            remote = self.cmd_edit.toPlainText()
            ftr.upload_file(file_name,remote)
            self.cmd_edit.setText("文件上传成功!")
    def save_file(self):
        self.cmd_edit.clear()
        text, ok = QInputDialog.getText(self, "remote", "请输入文件远程地址：")
        # 如果用户点击了 OK 按钮并且输入了文本
        if ok and text:
            self.cmd_edit.setText(text)
        file_name,_ = QFileDialog.getSaveFileName(self, "本地文件", "", "所有文件 (*);;文本文件 (*.txt)")
        remote = self.cmd_edit.toPlainText()
        ftr.download_file(remote,file_name)
        self.cmd_edit.setText("文件下载成功!")
    # 创建非模态窗口
    def open_no_modal(self):
        if not self.child_window:
            self.child_window = SecondWindow()
        self.child_window.show()  # 使用 show() 创建非模态窗口
    def open_users(self):
        if not self.child1_window:
            self.child1_window = UsersWindow()
        self.child1_window.show()
    def open_services(self):
        if not self.child2_window:
            self.child2_window = ServicesWindow()
        self.child2_window.show()
    def return_bt8(self):
        rc.disconnect()
        self.setWindowTitle(f"My Shell")
        self.lb_word.setText(f"Thank you use My Shell,Welcome next coming")
        self.cmd_edit.clear()
        self.input_edit.clear()
        self.input_edit.setEnabled(False)
        self.cmd_edit.setPlaceholderText("This is a sample shell console")
if __name__ == '__main__':
    # 创建应用程序对象
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # 进入应用程序的事件循环
    sys.exit(app.exec_())

