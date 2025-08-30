# 爱心例子动画逻辑

# animation/heart_particles.py

import math
import random
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QPointF


class Particle:
    def __init__(self, x, y, dx, dy, color, life):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.life = life  # 粒子寿命

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, painter: QPainter):
        if self.life > 0:
            alpha = max(0, min(255, int(255 * (self.life / 60))))
            painter.setBrush(QColor(self.color.red(), self.color.green(), self.color.blue(), alpha))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawEllipse(QPointF(self.x, self.y), 3, 3)

class HeartParticleSystem:
    def __init__(self, center_x, center_y, num_particles=150):
        self.center_x = center_x
        self.center_y = center_y
        self.num_particles = num_particles
        self.particles = []

    def heart_function(self, t, scale=10):
        x = scale * 16 * math.sin(t) ** 3
        y = -scale * (13 * math.cos(t) - 5 * math.cos(2 * t)
                      - 2 * math.cos(3 * t) - math.cos(4 * t))
        return x + self.center_x, y + self.center_y

    def emit(self):
        for _ in range(8):
            t = random.uniform(0, 2 * math.pi)
            x, y = self.heart_function(t)
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            color = QColor(255, random.randint(50, 150), random.randint(100, 200))
            self.particles.append(Particle(x, y, dx, dy, color, life=60))

    def update(self):
        self.emit()
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, painter):
        for p in self.particles:
            p.draw(painter)
