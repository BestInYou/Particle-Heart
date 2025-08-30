# main.py
import sys
from PyQt5 import QtWidgets
from ui.window import TransparentWindow

# 进入 cd D:\Study_Software\PycharmProjects\ToZQ
# 打包：pyinstaller main.py --noconfirm --onefile --windowed --add-data "assets/heart.png;assets" --icon="assets/heart.ico"

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = TransparentWindow()
    win.show()
    sys.exit(app.exec_())
