import sys  # 导入sys，用于与Python解释器交互
from PyQt5.QtGui import QFont, QMovie
import remote_connect as rc
import  show_gif
import file_tran as ftr
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QDialog, QTextEdit)
# 创建一个主窗口类，继承自 QMainWindow
# mrqin:1236666
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Shell")
        self.setGeometry(200, 200, 1200, 1000)
        # 创建主窗口中的中央控件，QMainWindow 需要设置中央控件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # 创建垂直布局管理器
        vbox_layout = QVBoxLayout()
        # vbox_layout.setSpacing(10)
        # 创建水平布局管理器
        hbox_layout = QHBoxLayout()
        hbox_layout.setSpacing(10)
        gif_label = QLabel()
        gif_label.setGeometry(15, 20, 100, 50)
        movie = QMovie("进度条.gif")
        gif_label.setMovie(movie)
        movie.start()
        button1 = QPushButton("连接远程",self)
        button2 = QPushButton("关闭远程",self)
        button3 = QPushButton("上传文件",self)
        button4 = QPushButton("下载文件",self)
        # 设置按钮固定大小和背景颜色和字体格式
        for btn in [button1, button2, button3, button4]:
            btn.setFixedSize(QSize(150, 60))
            btn.setFont(QFont(QFont("Arial", 12)))
            button1.setStyleSheet("background-color:green")
            button2.setStyleSheet("background-color:#FF0000")
            vbox_layout.addWidget(btn)
        button1.clicked.connect(self.return_button1)
        button2.clicked.connect(self.return_button2)
        button3.clicked.connect(self.open_file)
        button4.clicked.connect(self.save_file)
        # vbox_layout.addWidget(button1)
        # vbox_layout.addWidget(button2)
        # vbox_layout.addWidget(button3)
        # vbox_layout.addWidget(button4)

        # 创建文本框添加到垂直布局
        self.line_edit = QLineEdit(self)
        self.text_edit = QTextEdit(self)
        self.line_edit.setGeometry(15,450, 500, 100)
        self.text_edit.setGeometry(650,450, 500, 100)
        self.line_edit.setEnabled(False)  # 默认禁用
        # self.text_edit.setEnabled(False)
        self.line_edit.setPlaceholderText("请输入命令(按Enter执行):")
        self.text_edit.setPlaceholderText("文件路径:")
        # self.line_edit.setFixedSize(QSize(500, 200))
        self.line_edit.setFont(QFont("Arial", 11))
        self.text_edit.setFont(QFont("Arial", 11))
        # 连接文本输入结束的信号到槽函数# 连接文本输入结束的信号到槽函数
        self.line_edit.returnPressed.connect(self.return_command)
        # 将垂直布局设置为中央控件的布局
        central_widget.setLayout(vbox_layout)
    def return_button1(self):
        ssh1=rc.connect('192.168.73.42','root','123666')
        self.setWindowTitle(f"My Shell~{ssh1}")
        self.line_edit.setEnabled(True)

    def return_button2(self):
        rc.disconnect()
        self.setWindowTitle("My Shell")
        self.line_edit.clear()
        self.line_edit.setEnabled(False)

    def return_command(self):
        # 获取用户输入的文本
        text = self.line_edit.text()
        stdin, stdout, stderr = rc.ssh_client.exec_command(text)
        print(stdout.read().decode("utf-8"))

    def open_file(self):
        # 弹出文件对话框，让用户选择文件;检查用户是否选择了文件
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*);;文本文件 (*.txt)")
        self.text_edit.setText(file_name)
        # self.text_edit.setEnabled(True)
        # remote = input("请输入远程文件名:")
        remote = '/tmp/ceshi2.txt'
        ftr.upload_file(file_name,remote)
        self.text_edit.clear()
    def save_file(self):
        file_name,_ = QFileDialog.getSaveFileName(self, "选择文件", "", "所有文件 (*);;文本文件 (*.txt)")
        if file_name:
            # 获取文本框中的内容
            remote = self.text_edit.toPlainText()
            ftr.download_file(remote,file_name)
            # 保存文件内容的
            # with open(file_name,'a+') as f:
            #     f.writelines("\n"+file_content)
            # self.text_edit.clear()

# 创建应用程序对象
app = QApplication(sys.argv)
# 创建主窗口
window = MainWindow()
window.show()
# 进入应用程序的事件循环
sys.exit(app.exec_())





