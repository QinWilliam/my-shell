import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QMainWindow, QVBoxLayout, QLabel, QPushButton, QTabWidget

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("My Shell")
#         self.setGeometry(500, 300, 1000, 800)
#         # 创建主窗口中的中央控件，QMainWindow 需要设置中央控件
#         central_widget = QWidget(self)
#
#         self.setCentralWidget(central_widget)
#         self.user_edit = QLineEdit(self)
#         self.user_edit.returnPressed.connect(self.return_user)
#         # self.pwd_edit = QLineEdit(self)
#         # self.pwd_edit.returnPressed.connect(self.return_user)
#
#         # print(textwrap)
#     text = ''
#     def return_user(self):
#         text = self.user_edit.text()
#         print(text)
#     print(text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 标签页示例")
        self.setGeometry(100, 100, 1000, 800)

        # 创建 QTabWidget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)  # 将 TabWidget 设置为主窗口的中心部件

        # 添加标签页
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()

    def create_tab1(self):
        """创建第一个标签页"""
        tab1 = QWidget()
        layout = QVBoxLayout()

        # 在标签页中添加控件
        label = QLabel("这是标签页1的内容")
        button = QPushButton("点击按钮")
        button.clicked.connect(lambda: print("标签页1的按钮被点击了！"))

        layout.addWidget(label)
        layout.addWidget(button)
        tab1.setLayout(layout)

        # 将标签页添加到 TabWidget
        self.tab_widget.addTab(tab1, "基本信息")

    def create_tab2(self):
        """创建第二个标签页"""
        tab2 = QWidget()
        layout = QVBoxLayout()

        label = QLabel("这是标签页2的内容")
        layout.addWidget(label)
        tab2.setLayout(layout)


        self.tab_widget.addTab(tab2, "系统信息")
        tab2.setEnabled(False)

    def create_tab3(self):
        """创建第三个标签页（空页面）"""
        tab3 = QWidget()
        self.tab_widget.addTab(tab3, "服务与日志")


# 创建应用程序对象
app = QApplication(sys.argv)
# 创建主窗口
window = MainWindow()
window.show()
# 进入应用程序的事件循环
sys.exit(app.exec_())