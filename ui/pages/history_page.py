"""
Smart Dictator — History Page
Scrollable log of all voice commands, dictation sessions, and reading activity.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


_HISTORY = [
    # (emoji, type, time, description, status, status_color)
    ("🎤", "Command",   "10:32 PM", "Open Chrome",                 "✓ Completed", "#10b981"),
    ("🎙", "Dictation", "10:28 PM", "Dictated 124 words",           "✓ Completed", "#10b981"),
    ("📄", "Document",  "10:21 PM", "Read DBMS assignment PDF",     "✓ Completed", "#10b981"),
    ("📂", "Command",   "10:14 PM", "Opened Downloads folder",      "✓ Completed", "#10b981"),
    ("👁", "Screen",    "10:08 PM", "Read screen content",          "✓ Completed", "#10b981"),
    ("🎤", "Command",   "09:55 PM", "Find my resume",               "✓ Completed", "#10b981"),
    ("🎙", "Dictation", "09:41 PM", "Dictated 88 words",            "✓ Completed", "#10b981"),
    ("🎤", "Command",   "09:32 PM", "What's on my screen?",         "✓ Completed", "#10b981"),
    ("📄", "Document",  "09:21 PM", "Summarized lecture notes PDF", "✓ Completed", "#10b981"),
    ("🎤", "Command",   "09:08 PM", "Increase volume",              "✓ Completed", "#10b981"),
    ("🎙", "Dictation", "08:55 PM", "Dictated 200 words",           "✓ Completed", "#10b981"),
    ("📄", "Document",  "08:40 PM", "Read assignment PDF",          "✗ Cancelled", "#ef4444"),
]

_FILTERS = ["All", "Commands", "Dictation", "Screen", "Documents"]

_TYPE_COLORS = {
    "Command":   "#7c3aed",
    "Dictation": "#3b82f6",
    "Screen":    "#06b6d4",
    "Document":  "#10b981",
}


class HistoryPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._active = "All"
        self._build()

    # ── build ───────────────────────────────────────────────────────────────

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 22, 28, 22)
        lay.setSpacing(16)

        lay.addWidget(self._header())
        lay.addWidget(self._filter_row())
        lay.addWidget(self._history_list(), 1)

    # ── header ──────────────────────────────────────────────────────────────

    def _header(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        col = QWidget()
        col.setStyleSheet("background:transparent;")
        cl = QVBoxLayout(col)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(4)

        t = QLabel("🕐   Activity History")
        t.setObjectName("page_title")
        t.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        t.setStyleSheet("color:#f0f4ff;")

        s = QLabel(
            "A complete log of all your voice commands, "
            "dictation sessions, and reading activities."
        )
        s.setObjectName("page_sub")
        s.setFont(QFont("Segoe UI", 13))
        s.setWordWrap(True)

        cl.addWidget(t)
        cl.addWidget(s)
        lay.addWidget(col, 1)

        # Summary badge
        badge = QWidget()
        badge.setStyleSheet(
            "background:#111827; border-radius:12px; border:1px solid #1e2d4a;"
        )
        bl = QVBoxLayout(badge)
        bl.setContentsMargins(20, 10, 20, 10)
        bl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cnt = QLabel(str(len(_HISTORY)))
        cnt.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        cnt.setStyleSheet("color:#f0f4ff;")
        cnt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Activities Today")
        sub.setFont(QFont("Segoe UI", 10))
        sub.setStyleSheet("color:#8b9bc8;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bl.addWidget(cnt)
        bl.addWidget(sub)
        lay.addWidget(badge)

        return w

    # ── filter row ───────────────────────────────────────────────────────────

    def _filter_row(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        self._tabs: dict[str, QPushButton] = {}
        for name in _FILTERS:
            btn = QPushButton(name)
            btn.setObjectName("tab_btn")
            btn.setFixedHeight(36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _=False, n=name: self._set_tab(n))
            self._tabs[name] = btn
            lay.addWidget(btn)

        lay.addStretch()

        clear = QPushButton("🗑   Clear History")
        clear.setObjectName("btn_danger")
        clear.setFixedHeight(36)
        clear.setCursor(Qt.CursorShape.PointingHandCursor)
        lay.addWidget(clear)

        self._set_tab("All")
        return w

    def _set_tab(self, name: str):
        self._active = name
        for n, btn in self._tabs.items():
            btn.setProperty("active", n == name)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ── history list ─────────────────────────────────────────────────────────

    def _history_list(self) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background:transparent; border:none;")

        inner = QWidget()
        inner.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        for row in _HISTORY:
            lay.addWidget(self._item(*row))

        lay.addStretch()
        scroll.setWidget(inner)
        return scroll

    def _item(self, icon, type_, time, desc, status, sc) -> QWidget:
        w = QWidget()
        w.setObjectName("hist_item")
        w.setFixedHeight(58)

        lay = QHBoxLayout(w)
        lay.setContentsMargins(14, 0, 14, 0)
        lay.setSpacing(12)

        tc = _TYPE_COLORS.get(type_, "#7c3aed")

        # Icon badge
        badge = QLabel(icon)
        badge.setFixedSize(36, 36)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFont(QFont("Segoe UI Emoji", 14))
        badge.setStyleSheet(
            f"background:{tc}22; border-radius:10px; border:1px solid {tc}55;"
        )

        # Type label
        type_l = QLabel(type_)
        type_l.setFixedWidth(70)
        type_l.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        type_l.setStyleSheet(f"color:{tc};")

        # Description
        desc_l = QLabel(desc)
        desc_l.setObjectName("hist_cmd")
        desc_l.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        desc_l.setStyleSheet("color:#e2e8f0;")

        lay.addWidget(badge)
        lay.addWidget(type_l)
        lay.addWidget(desc_l)
        lay.addStretch()

        time_l = QLabel(time)
        time_l.setObjectName("hist_time")
        time_l.setFont(QFont("Segoe UI", 11))
        time_l.setStyleSheet("color:#4a5780;")

        status_l = QLabel(status)
        status_l.setFixedWidth(88)
        status_l.setFont(QFont("Segoe UI", 11))
        status_l.setStyleSheet(f"color:{sc};")
        status_l.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        lay.addWidget(time_l)
        lay.addWidget(status_l)
        return w
