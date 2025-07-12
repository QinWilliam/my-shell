from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QMovie
def gif():
    app = QApplication([])
    window = QWidget()
    layout = QHBoxLayout()
    # 创建QLabel用于显示GIF
    gif_label = QLabel()
    gif_label.setStyleSheet("background-color:black;")
    movie = QMovie("进度条.gif")
    gif_label.setMovie(movie)
    movie.start()
    layout.addWidget(gif_label)
    window.setLayout(layout)
    window.show()
    app.exec_()