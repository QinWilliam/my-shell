import sys

from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QDialog, QVBoxLayout, QComboBox, QLabel)


# class ComboBoxDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("下拉列表示例")
#         self.setGeometry(1000, 200, 800, 600)
#
#         # 创建布局
#         layout = QVBoxLayout()
#         # 创建下拉列表并添加选项
#         self.combo = QComboBox(self)
#         self.combo.addItems(["选项1", "选项2", "选项3"])  # 静态添加选项
#         # 显示当前选择的标签
#         self.label = QLabel("当前选择：无", self)
#         # 连接信号槽：当下拉选项变化时更新标签
#         self.combo.currentTextChanged.connect(self.update_label)
#         # 将控件添加到布局
#         layout.addWidget(self.combo)
#         layout.addWidget(self.label)
#         self.setLayout(layout)
#     def update_label(self, text):
#         """当下拉选项变化时自动调用"""
#         self.label.setText(f"当前选择：{text}")
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("主窗口")
#         self.setGeometry(100, 100, 400, 300)
#
#         # 添加按钮用于打开子窗口
#         self.button = QPushButton("打开下拉列表窗口", self)
#         self.button.clicked.connect(self.open_dialog)
#         self.setCentralWidget(self.button)
#
#     def open_dialog(self):
#         dialog = ComboBoxDialog()
#         dialog.exec_()
#
#
# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()

# 1.打开模态窗口
class DialogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("文件管理")
        self.setGeometry(300, 300, 800, 600)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主窗口")

        self.setGeometry(100, 100, 400, 300)
        self.btn = QPushButton("打开模态窗口", self)
        self.btn.setGeometry(150, 100, 120, 40)
        self.btn.clicked.connect(self.open_modal)
    def open_modal(self):
        dialog = DialogWindow()
        # 设置模态并隐藏问号按钮
        dialog.exec_()  # 使用 exec_() 创建模态对话框

 # 2.使用非模态窗口：允许用户同时与主窗口和子窗口交互
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
# class SecondWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("子窗口")
#         self.setGeometry(300, 300, 1000, 800)
#         layout = QVBoxLayout()
#         # 创建下拉列表并添加选项
#         self.combo = QComboBox(self)
#         self.combo.addItems(["请选择操作","添加用户", "删除用户", "查看用户","查看所有用户"])  # 静态添加选项
#         # 显示当前选择的标签
#         self.label = QLabel("当前选择：无", self)
#         # 连接信号槽：当下拉选项变化时更新标签
#         self.combo.currentTextChanged.connect(self.update_label)
#         # 将控件添加到布局
#         layout.addWidget(self.combo)
#         layout.addWidget(self.label)
#         self.setLayout(layout)
#     def update_label(self, text):
#         """当下拉选项变化时自动调用"""
#         self.label.setText(f"当前选择：{text}")
#         # self.combo.setCurrentText(text)
#         # print(text)
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("主窗口")
#         self.setGeometry(100, 100, 400, 300)
#
#         # 创建按钮
#         self.btn = QPushButton("打开非模态窗口", self)
#         self.btn.setGeometry(150, 100, 120, 40)
#         self.btn.clicked.connect(self.open_non_modal)
#         # 保存子窗口引用防止被回收
#         self.child_window = None
#
#     def open_non_modal(self):
#         if not self.child_window:
#             self.child_window = SecondWindow()
#         self.child_window.show()  # 使用 show() 创建非模态窗口

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

