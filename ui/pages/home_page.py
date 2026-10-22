"""
Smart Dictator — Home Page (responsive)
Hero mic button, quick actions, right-panel stats/status
"""
import math

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from ui.widgets.mic_button import MicButton, WaveformBars


_STATES = [
    MicButton.STATE_READY,
    MicButton.STATE_LISTENING,
    MicButton.STATE_PROCESSING,
    MicButton.STATE_EXECUTING,
    MicButton.STATE_SPEAKING,
    MicButton.STATE_DONE,
]

_STATE_TEXT = {
    MicButton.STATE_READY:      ("Tap to Speak",   "Click the mic or press Space to start"),
    MicButton.STATE_LISTENING:  ("Listening...",    "Speak clearly into your microphone"),
    MicButton.STATE_PROCESSING: ("Processing...",   "Understanding your request..."),
    MicButton.STATE_EXECUTING:  ("Executing...",    "Performing the action..."),
    MicButton.STATE_SPEAKING:   ("Speaking...",     "Smart Dictator is responding"),
    MicButton.STATE_DONE:       ("Done  ✓",         "Ready for your next command"),
}

_CHIPS = [
    "🔊 Open Chrome",
    "🔊 Start dictation",
    "🔊 Read my screen",
    "🔊 Open Downloads",
    "🔊 Read this PDF",
]

_QUICK_ACTIONS = [
    ("🎙", "#7c3aed", "Dictate",        "Speech to text",   1),
    ("👁", "#3b82f6", "Read Screen",    "OCR visible text", 2),
    ("📄", "#06b6d4", "Read Document",  "Listen to a file", 3),
    ("⌨",  "#10b981", "Voice Commands", "Control your PC",  1),
]

_RECENT = [
    ("✓ Opened Chrome",      "10:32 PM"),
    ("✓ Dictated 124 words", "10:28 PM"),
    ("✓ Read PDF document",  "10:21 PM"),
    ("✓ Opened Downloads",   "10:14 PM"),
]

_COMMANDS = [
    ("Open my resume",        "10:24 AM"),
    ("Find DBMS assignment",  "10:15 AM"),
    ("Read this PDF",         "09:58 AM"),
    ("What's on my screen?",  "09:32 AM"),
]

_STATS = [
    ("12", "Tasks Done",    "#10b981", "✅"),
    ("2",  "Docs Read",     "#ec4899", "📄"),
    ("5",  "Screen Reads",  "#3b82f6", "👁"),
    ("8",  "Dictation",     "#f59e0b", "🎙"),
]


class HomePage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state_idx = 0
        self._build()

    # ── layout ──────────────────────────────────────────────────────────────

    def _build(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── scrollable left content ──────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setObjectName("page_scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(22, 16, 16, 16)
        ll.setSpacing(12)

        ll.addWidget(self._greeting())
        ll.addWidget(self._mic_card())
        ll.addWidget(self._section_lbl("Quick Actions"))
        ll.addWidget(self._quick_actions())
        ll.addWidget(self._section_lbl("Recent Activity"))
        ll.addWidget(self._recent_activity())
        ll.addStretch()
        ll.addWidget(self._safe_bar())

        scroll.setWidget(left)
        outer.addWidget(scroll, 1)

        # ── right panel (fixed, compact) ─────────────────────────────────────
        outer.addWidget(self._right_panel())

    # ── greeting ────────────────────────────────────────────────────────────

    def _greeting(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(3)

        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        hello = QLabel("Hello, ")
        hello.setObjectName("greeting")
        hello.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))

        user = QLabel("User!")
        user.setObjectName("greeting_user")
        user.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))

        rl.addWidget(hello)
        rl.addWidget(user)
        rl.addStretch()

        sub = QLabel("Your voice is your interface.  Speak to take control of your computer.")
        sub.setObjectName("greeting_sub")
        sub.setFont(QFont("Segoe UI", 12))
        sub.setWordWrap(True)

        lay.addWidget(row)
        lay.addWidget(sub)
        return w

    # ── mic card ─────────────────────────────────────────────────────────────

    def _mic_card(self) -> QWidget:
        card = QWidget()
        card.setObjectName("mic_card")
        card.setMinimumHeight(230)

        outer = QVBoxLayout(card)
        outer.setContentsMargins(16, 14, 16, 12)
        outer.setSpacing(6)

        # Waveforms + mic row
        mid = QWidget()
        ml = QHBoxLayout(mid)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        self._wave_l = WaveformBars(mirrored=True,  w=70, h=100)
        self._mic    = MicButton(size=170)
        self._wave_r = WaveformBars(mirrored=False, w=70, h=100)
        self._mic.clicked.connect(self._on_mic)

        ml.addStretch()
        ml.addWidget(self._wave_l)
        ml.addSpacing(6)
        ml.addWidget(self._mic)
        ml.addSpacing(6)
        ml.addWidget(self._wave_r)
        ml.addStretch()

        outer.addWidget(mid)

        # State / hint labels
        self._state_lbl = QLabel("Tap to Speak")
        self._state_lbl.setObjectName("mic_state")
        self._state_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._state_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.DemiBold))

        self._hint_lbl = QLabel("Click the mic or press Space to start")
        self._hint_lbl.setObjectName("mic_hint")
        self._hint_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hint_lbl.setFont(QFont("Segoe UI", 11))

        outer.addWidget(self._state_lbl)
        outer.addWidget(self._hint_lbl)
        outer.addSpacing(4)

        # Chips row
        chips_lbl = QLabel("Try saying:")
        chips_lbl.setObjectName("mic_hint")
        chips_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chips_lbl.setFont(QFont("Segoe UI", 10))

        chips_row = QWidget()
        crl = QHBoxLayout(chips_row)
        crl.setContentsMargins(0, 0, 0, 0)
        crl.setSpacing(6)
        crl.addStretch()
        for c in _CHIPS:
            btn = QPushButton(c)
            btn.setObjectName("chip")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFont(QFont("Segoe UI", 11))
            crl.addWidget(btn)
        crl.addStretch()

        outer.addWidget(chips_lbl)
        outer.addWidget(chips_row)
        return card

    def _on_mic(self):
        self._state_idx = (self._state_idx + 1) % len(_STATES)
        state = _STATES[self._state_idx]
        self._mic.set_state(state)

        label, hint = _STATE_TEXT[state]
        self._state_lbl.setText(label)
        self._hint_lbl.setText(hint)

        active = state in (MicButton.STATE_LISTENING, MicButton.STATE_SPEAKING)
        self._wave_l.set_active(active)
        self._wave_r.set_active(active)

        if state == MicButton.STATE_DONE:
            QTimer.singleShot(1400, self._reset)

    def _reset(self):
        self._state_idx = 0
        self._mic.set_state(MicButton.STATE_READY)
        self._state_lbl.setText("Tap to Speak")
        self._hint_lbl.setText("Click the mic or press Space to start")
        self._wave_l.set_active(False)
        self._wave_r.set_active(False)

    # ── quick actions ────────────────────────────────────────────────────────

    def _quick_actions(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        for icon, color, title, sub, _ in _QUICK_ACTIONS:
            lay.addWidget(self._qa_card(icon, color, title, sub))
        return w

    def _qa_card(self, icon, color, title, sub) -> QWidget:
        card = QWidget()
        card.setObjectName("qa_card")
        card.setFixedHeight(100)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setSpacing(4)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_w = QLabel(icon)
        icon_w.setFixedSize(40, 40)
        icon_w.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_w.setFont(QFont("Segoe UI Emoji", 18))
        icon_w.setStyleSheet(
            f"background:{color}22; border-radius:20px; border:1px solid {color}55;"
        )

        icon_row = QWidget()
        ir = QHBoxLayout(icon_row)
        ir.setContentsMargins(0, 0, 0, 0)
        ir.addStretch(); ir.addWidget(icon_w); ir.addStretch()

        title_l = QLabel(title)
        title_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_l.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        title_l.setStyleSheet("color:#f0f4ff;")

        sub_l = QLabel(sub)
        sub_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_l.setFont(QFont("Segoe UI", 9))
        sub_l.setStyleSheet("color:#4a5780;")

        lay.addWidget(icon_row)
        lay.addWidget(title_l)
        lay.addWidget(sub_l)
        return card

    # ── recent activity ──────────────────────────────────────────────────────

    def _recent_activity(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        for text, time in _RECENT:
            item = QWidget()
            item.setStyleSheet(
                "background:#111827; border-radius:10px; border:1px solid #1e2d4a;"
            )
            il = QHBoxLayout(item)
            il.setContentsMargins(10, 8, 10, 8)
            il.setSpacing(6)

            ck = QLabel("✓")
            ck.setStyleSheet("color:#10b981; font-size:13px;")

            tl = QLabel(text)
            tl.setFont(QFont("Segoe UI", 11))
            tl.setStyleSheet("color:#8b9bc8;")
            tl.setWordWrap(True)

            il.addWidget(ck)
            il.addWidget(tl)
            il.addStretch()
            lay.addWidget(item)

        return w

    # ── safe bar ─────────────────────────────────────────────────────────────

    def _safe_bar(self) -> QWidget:
        w = QWidget()
        w.setObjectName("safe_bar")
        w.setFixedHeight(46)

        lay = QHBoxLayout(w)
        lay.setContentsMargins(14, 0, 14, 0)
        lay.setSpacing(10)

        shield = QLabel("🛡")
        shield.setFont(QFont("Segoe UI Emoji", 16))

        col = QWidget()
        col.setStyleSheet("background:transparent;")
        cl = QVBoxLayout(col)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(1)

        t = QLabel("Safe Mode  —  All actions are verified for your safety")
        t.setObjectName("safe_title")
        t.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))

        cl.addWidget(t)

        btn = QPushButton("View Activity  →")
        btn.setObjectName("view_activity_btn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        lay.addWidget(shield)
        lay.addWidget(col)
        lay.addStretch()
        lay.addWidget(btn)
        return w

    # ── right panel ──────────────────────────────────────────────────────────

    def _right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(238)
        panel.setStyleSheet("background:#0a1020; border-left:1px solid #1e2d4a;")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background:transparent; border:none;")

        inner = QWidget()
        inner.setStyleSheet("background:transparent;")
        il = QVBoxLayout(inner)
        il.setContentsMargins(10, 14, 10, 14)
        il.setSpacing(12)

        il.addWidget(self._stats_card())
        il.addWidget(self._commands_card())
        il.addWidget(self._language_card())
        il.addWidget(self._sys_status_card())
        il.addStretch()

        scroll.setWidget(inner)

        pl = QVBoxLayout(panel)
        pl.setContentsMargins(0, 0, 0, 0)
        pl.addWidget(scroll)
        return panel

    def _rp_header(self, title: str, btn_text: str = "") -> QWidget:
        row = QWidget()
        row.setStyleSheet("background:transparent;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(title)
        lbl.setObjectName("rp_title")
        lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        rl.addWidget(lbl)
        rl.addStretch()

        if btn_text:
            btn = QPushButton(btn_text)
            btn.setObjectName("view_all_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFont(QFont("Segoe UI", 11))
            rl.addWidget(btn)

        return row

    def _stats_card(self) -> QWidget:
        card = QWidget()
        card.setObjectName("rp_card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 12)
        cl.setSpacing(8)
        cl.addWidget(self._rp_header("Today's Activity", "All"))

        grid = QWidget()
        grid.setStyleSheet("background:transparent;")
        gl = QGridLayout(grid)
        gl.setContentsMargins(0, 0, 0, 0)
        gl.setSpacing(6)

        for i, (cnt, lbl, color, icon) in enumerate(_STATS):
            stat = QWidget()
            stat.setObjectName("stat_item")
            stat.setFixedHeight(56)
            sl = QHBoxLayout(stat)
            sl.setContentsMargins(8, 6, 8, 6)
            sl.setSpacing(7)

            icon_l = QLabel(icon)
            icon_l.setFixedSize(26, 26)
            icon_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_l.setFont(QFont("Segoe UI Emoji", 11))
            icon_l.setStyleSheet(f"background:{color}25; border-radius:7px;")

            info = QWidget()
            info.setStyleSheet("background:transparent;")
            il2 = QVBoxLayout(info)
            il2.setContentsMargins(0, 0, 0, 0)
            il2.setSpacing(0)

            c_l = QLabel(cnt)
            c_l.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
            c_l.setStyleSheet("color:#f0f4ff;")

            lb_l = QLabel(lbl)
            lb_l.setFont(QFont("Segoe UI", 8))
            lb_l.setStyleSheet("color:#8b9bc8;")

            il2.addWidget(c_l)
            il2.addWidget(lb_l)
            sl.addWidget(icon_l)
            sl.addWidget(info)
            gl.addWidget(stat, i // 2, i % 2)

        cl.addWidget(grid)
        return card

    def _commands_card(self) -> QWidget:
        card = QWidget()
        card.setObjectName("rp_card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 12)
        cl.setSpacing(6)
        cl.addWidget(self._rp_header("Recent Commands", "All"))

        for cmd, time in _COMMANDS:
            item = QWidget()
            item.setObjectName("cmd_item")
            item.setFixedHeight(34)
            il = QHBoxLayout(item)
            il.setContentsMargins(8, 0, 8, 0)
            il.setSpacing(7)

            mic = QLabel("🎤")
            mic.setFont(QFont("Segoe UI Emoji", 9))
            mic.setFixedWidth(16)

            cmd_l = QLabel(cmd)
            cmd_l.setFont(QFont("Segoe UI", 11))
            cmd_l.setStyleSheet("color:#e2e8f0;")

            time_l = QLabel(time)
            time_l.setFont(QFont("Segoe UI", 9))
            time_l.setStyleSheet("color:#4a5780;")

            il.addWidget(mic)
            il.addWidget(cmd_l)
            il.addStretch()
            il.addWidget(time_l)
            cl.addWidget(item)

        return card

    def _language_card(self) -> QWidget:
        card = QWidget()
        card.setObjectName("rp_card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(8)
        cl.addWidget(self._rp_header("Language", "Change"))

        row = QWidget()
        row.setStyleSheet("background:#0f1a30; border-radius:10px;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(10, 7, 10, 7)
        rl.setSpacing(8)

        flag = QLabel("🇮🇳")
        flag.setFont(QFont("Segoe UI Emoji", 18))

        info = QWidget()
        info.setStyleSheet("background:transparent;")
        il = QVBoxLayout(info)
        il.setContentsMargins(0, 0, 0, 0)
        il.setSpacing(2)

        name = QLabel("English (India)")
        name.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        name.setStyleSheet("color:#f0f4ff;")

        desc = QLabel("English · Hindi · Marathi")
        desc.setFont(QFont("Segoe UI", 9))
        desc.setStyleSheet("color:#8b9bc8;")

        il.addWidget(name)
        il.addWidget(desc)
        rl.addWidget(flag)
        rl.addWidget(info)
        rl.addStretch()
        cl.addWidget(row)
        return card

    def _sys_status_card(self) -> QWidget:
        card = QWidget()
        card.setObjectName("rp_card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(6)

        title = QLabel("System Status")
        title.setObjectName("rp_title")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        cl.addWidget(title)

        for icon, label, status, color in [
            ("🎤", "Microphone", "● Working",   "#10b981"),
            ("🌐", "Internet",   "● Connected", "#10b981"),
            ("🤖", "AI Engine",  "● Ready",     "#10b981"),
        ]:
            row = QWidget()
            row.setStyleSheet("background:transparent;")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 3, 0, 3)
            rl.setSpacing(7)

            ic = QLabel(icon)
            ic.setFont(QFont("Segoe UI Emoji", 11))
            ic.setFixedWidth(20)

            nl = QLabel(label)
            nl.setFont(QFont("Segoe UI", 11))
            nl.setStyleSheet("color:#8b9bc8;")

            sl = QLabel(status)
            sl.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
            sl.setStyleSheet(f"color:{color};")

            rl.addWidget(ic)
            rl.addWidget(nl)
            rl.addStretch()
            rl.addWidget(sl)
            cl.addWidget(row)

        return card

    @staticmethod
    def _section_lbl(text: str) -> QLabel:
        l = QLabel(text)
        l.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        l.setStyleSheet("color:#f0f4ff;")
        return l
