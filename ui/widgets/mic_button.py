"""
Smart Dictator — Custom Widgets
  • ToggleSwitch  — animated on/off toggle
  • WaveformBars  — animated audio waveform visualizer
  • MicButton     — the main glowing animated microphone button
"""
import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, Signal, QRect, QPointF
from PySide6.QtGui import (
    QPainter, QPen, QBrush, QColor, QRadialGradient,
    QFont, QPainterPath
)


# ═══════════════════════════════════════════════════════════════════════════
#  ToggleSwitch
# ═══════════════════════════════════════════════════════════════════════════

class ToggleSwitch(QWidget):
    """Animated iOS-style toggle switch."""

    toggled = Signal(bool)

    def __init__(self, parent=None, checked: bool = False):
        super().__init__(parent)
        self._checked = checked
        self.setFixedSize(46, 26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._thumb_x = 22.0 if checked else 3.0
        self._anim = QTimer(self)
        self._anim.timeout.connect(self._step)

    def is_checked(self) -> bool:
        return self._checked

    def set_checked(self, val: bool):
        self._checked = val
        self._anim.start(12)

    def _step(self):
        target = 22.0 if self._checked else 3.0
        diff = target - self._thumb_x
        if abs(diff) < 0.6:
            self._thumb_x = target
            self._anim.stop()
        else:
            self._thumb_x += diff * 0.28
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        track = QColor(124, 58, 237) if self._checked else QColor(30, 45, 74)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(track))
        p.drawRoundedRect(0, 0, 46, 26, 13, 13)
        p.setBrush(QBrush(QColor(255, 255, 255)))
        p.drawEllipse(int(self._thumb_x), 3, 20, 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked
            self._anim.start(12)
            self.toggled.emit(self._checked)


# ═══════════════════════════════════════════════════════════════════════════
#  WaveformBars  — configurable size so home page can use smaller bars
# ═══════════════════════════════════════════════════════════════════════════

class WaveformBars(QWidget):
    """Animated audio waveform bars — sits beside the mic button."""

    def __init__(self, parent=None, mirrored: bool = False,
                 w: int = 80, h: int = 110):
        super().__init__(parent)
        self.mirrored = mirrored
        self.setFixedSize(w, h)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._active = False
        self._t = 0.0
        self._n = 9
        self._base = [0.28, 0.45, 0.62, 0.80, 1.00, 0.80, 0.62, 0.45, 0.28]
        self._cur  = list(self._base)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(50)

    def set_active(self, active: bool):
        self._active = active
        if not active:
            self._cur = [b * 0.18 for b in self._base]
        self.update()

    def _animate(self):
        self._t += 0.18
        speed = 1.0 if self._active else 0.25
        scale = 0.85 if self._active else 0.16
        for i in range(self._n):
            phase = self._t * speed + i * 0.45
            self._cur[i] = (scale * abs(math.sin(phase)) + (1 - scale) * 0.12) * self._base[i]
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        bar_w = 3
        total_gap = w - self._n * bar_w
        gap = total_gap / (self._n + 1)
        max_h = h * 0.88

        for i, val in enumerate(self._cur):
            bh = max(4, int(val * max_h))
            x = int(gap + i * (bar_w + gap))
            if self.mirrored:
                x = w - x - bar_w
            y = (h - bh) // 2

            if self._active:
                t = val
                r = int(124 + (34  - 124) * t)
                g = int(58  + (211 - 58 ) * t)
                b = int(237 + (238 - 237) * t)
                alpha = int(140 + 100 * t)
            else:
                r, g, b = 45, 65, 120
                alpha = int(60 + 40 * val)

            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(QColor(r, g, b, alpha)))
            p.drawRoundedRect(x, y, bar_w, bh, 2, 2)


# ═══════════════════════════════════════════════════════════════════════════
#  MicButton
# ═══════════════════════════════════════════════════════════════════════════

class MicButton(QWidget):
    """
    Large animated microphone button.
    States: ready · listening · processing · executing · speaking · done
    """

    clicked = Signal()

    STATE_READY      = "ready"
    STATE_LISTENING  = "listening"
    STATE_PROCESSING = "processing"
    STATE_EXECUTING  = "executing"
    STATE_SPEAKING   = "speaking"
    STATE_DONE       = "done"

    _COLORS = {
        STATE_READY:      (QColor(109, 40,  217), QColor( 37,  99, 235)),
        STATE_LISTENING:  (QColor(139, 92,  246), QColor( 59, 130, 246)),
        STATE_PROCESSING: (QColor( 59, 130, 246), QColor( 34, 211, 238)),
        STATE_EXECUTING:  (QColor(245, 158,  11), QColor(234, 179,   8)),
        STATE_SPEAKING:   (QColor( 16, 185, 129), QColor( 34, 211, 238)),
        STATE_DONE:       (QColor( 16, 185, 129), QColor(  5, 150, 105)),
    }

    def __init__(self, parent=None, size: int = 175):
        super().__init__(parent)
        self._size = size
        self._base_r = int(size * 0.435)          # proportional ring radius
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._state = self.STATE_READY
        self._rings: list[dict] = []
        self._spawn_counter = 0
        self._glow_t = 0.0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def get_state(self) -> str:
        return self._state

    def set_state(self, state: str):
        self._state = state
        if state in (self.STATE_READY, self.STATE_DONE):
            self._rings.clear()
        self.update()

    def _tick(self):
        self._glow_t += 0.05
        if self._state in (self.STATE_LISTENING,
                            self.STATE_PROCESSING,
                            self.STATE_SPEAKING):
            self._spawn_counter += 1
            if self._spawn_counter >= 36:
                self._spawn_counter = 0
                self._rings.append({"r": float(self._base_r + 13), "a": 180})
            for ring in self._rings:
                ring["r"] += 1.8
                ring["a"] -= 5
            self._rings = [r for r in self._rings if r["a"] > 0]
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        BR = self._base_r

        c1, c2 = self._COLORS.get(self._state, self._COLORS[self.STATE_READY])

        # Pulse rings
        for ring in self._rings:
            mid = QColor(
                (c1.red()   + c2.red())   // 2,
                (c1.green() + c2.green()) // 2,
                (c1.blue()  + c2.blue())  // 2,
                ring["a"]
            )
            p.setPen(QPen(mid, 1.5))
            p.setBrush(Qt.BrushStyle.NoBrush)
            r = int(ring["r"])
            p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        # Soft glow halo
        glow_r = BR + 10 + 5 * math.sin(self._glow_t)
        glow_grad = QRadialGradient(QPointF(cx, cy), glow_r)
        glow_grad.setColorAt(0.72, QColor(0, 0, 0, 0))
        glow_grad.setColorAt(0.88, QColor(c1.red(), c1.green(), c1.blue(), 55))
        glow_grad.setColorAt(1.00, QColor(0, 0, 0, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(glow_grad))
        gr = int(glow_r)
        p.drawEllipse(cx - gr, cy - gr, gr * 2, gr * 2)

        # Outer gradient ring
        grad = QRadialGradient(QPointF(cx, cy), BR + 4)
        grad.setColorAt(0.00, QColor(0, 0, 0, 0))
        grad.setColorAt(0.86, QColor(0, 0, 0, 0))
        grad.setColorAt(0.92, c1)
        grad.setColorAt(0.97, c2)
        grad.setColorAt(1.00, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(grad))
        p.drawEllipse(cx - BR - 4, cy - BR - 4,
                      (BR + 4) * 2, (BR + 4) * 2)

        # Inner dark circle
        IR = BR - 6
        inner = QRadialGradient(QPointF(cx - 8, cy - 12), IR * 0.85)
        inner.setColorAt(0, QColor(32, 40, 68))
        inner.setColorAt(0.6, QColor(13, 20, 38))
        inner.setColorAt(1.0, QColor(5,  10, 22))
        p.setBrush(QBrush(inner))
        p.drawEllipse(cx - IR, cy - IR, IR * 2, IR * 2)

        self._draw_mic(p, cx, cy)

    def _draw_mic(self, p: QPainter, cx: int, cy: int):
        s = self._size / 175.0          # scale factor vs reference size
        color = QColor(235, 240, 255, 230)

        bw = int(22 * s); bh = int(38 * s); br = int(11 * s)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(color))
        body = QPainterPath()
        body.addRoundedRect(cx - bw//2, cy - bh//2 - int(7*s), bw, bh, br, br)
        p.drawPath(body)

        pen = QPen(color, max(2, int(3 * s)), Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)

        a = int(19 * s)
        p.drawArc(QRect(cx - a, cy + int(8*s), a*2, int(24*s)), 0, -180 * 16)
        p.drawLine(cx, cy + int(20*s), cx, cy + int(30*s))
        p.drawLine(cx - int(11*s), cy + int(30*s), cx + int(11*s), cy + int(30*s))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            cx, cy = self.width() // 2, self.height() // 2
            dx = event.position().x() - cx
            dy = event.position().y() - cy
            if dx * dx + dy * dy <= self._base_r * self._base_r:
                self.clicked.emit()
