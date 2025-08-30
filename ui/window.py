from PyQt5 import QtWidgets, QtCore, QtGui
from animation.heart_particles import HeartParticleSystem
from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

import sys
import os
import random

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 设置无边框+置顶窗口
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        # 防止窗口出现在任务栏
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Tool)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(QtWidgets.QDesktopWidget().screenGeometry())

        # 创建粒子系统
        self.particle_system = HeartParticleSystem(
            center_x=self.width() // 2,
            center_y=self.height() // 2
        )

        # 启动动画刷新定时器label.raise_()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)  # 每30ms刷新一次

        # 托盘图标
        self.create_tray_icon()

        self.love_messages_pool = [
            "我想你啦~ 💭",
            "偷偷亲你一下 😚",
            "今天也要开心哦 ☀️",
            "你的小心心上线啦！💗",
            "你笑起来好好看 😍",
            "此刻在想你 🥺",
            "你是我心里最亮的星 ✨",
            "爱你比昨天多一点 💖",
            "不许不理我喔 🐰",
            "记得喝水哦 💧",
            "学习也要想我哦 😎",
            "哼！刚才是不是在偷懒 👀",
            "喜欢你最可爱的时候 🧸",
            "给你发射一颗小心心 💘",
            "你今天有想我吗 🤔",
            "抱一下，不许躲 🙈",
            "今晚梦里见 💫",
            "不许太累，要休息 💤"
        ]
        # 复制一份初始的轮播池
        self._message_queue = self.love_messages_pool.copy()
        random.shuffle(self._message_queue)

        # 自动触发短语提示
        self.message_timer = QtCore.QTimer()
        self.message_timer.timeout.connect(self.show_love_message)
        self.message_timer.start(10000)  # 每15秒触发一次

    def update_animation(self):
        self.particle_system.update()
        self.update()  # 触发 repaint

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.particle_system.draw(painter)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def create_tray_icon(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        # 获取图标路径：打包模式用 _MEIPASS，否则用本地路径
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'assets', 'heart.png')
        else:
            icon_path = os.path.join('assets', 'heart.png')

        self.tray_icon.setIcon(QtGui.QIcon(icon_path))
        # self.tray_icon.setIcon(QtGui.QIcon("assets/heart.png"))  # 你可以替换为 QtGui.QIcon("assets/heart.png")
        self.tray_icon.setToolTip("要开心哦")

        menu = QtWidgets.QMenu()
        exit_action = menu.addAction("退出")
        exit_action.triggered.connect(QtWidgets.qApp.quit)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def show_love_message(self):
        # 若消息用完，则重新洗牌一轮
        if not self._message_queue:
            self._message_queue = self.love_messages_pool.copy()
            random.shuffle(self._message_queue)

        text = self._message_queue.pop(0)

        label = QLabel(text, self)
        label.setStyleSheet("""
            QLabel {
                color: pink;
                font-size: 32px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0);
            }
        """)
        label.adjustSize()

        x = (self.width() - label.width()) // 2
        y = self.height() // 3 + 20
        label.move(x, y)
        label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        label.raise_()  # ✨ 关键：浮到最顶层
        label.show()

        opacity_effect = QGraphicsOpacityEffect(label)
        label.setGraphicsEffect(opacity_effect)

        # 淡入动画
        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(800)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.InOutQuad)

        # 淡出动画
        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(800)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        fade_out.finished.connect(label.deleteLater)

        # 动画链：淡入 → 停顿 → 淡出
        def start_fade_out():
            fade_out.start()

        fade_in.finished.connect(lambda: QtCore.QTimer.singleShot(500, start_fade_out))
        fade_in.start()

        # 防止动画被垃圾回收
        label.fade_in = fade_in
        label.fade_out = fade_out
