"""
Smart Dictator — Dictation Page
Large editor, start/stop control, AI writing tools.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


_PLACEHOLDER = (
    "Start dictation to begin converting your speech to clean, formatted text.\n\n"
    "You can say things like:\n"
    '  •  "Dear Sir, comma, new paragraph, I wanted to inform you..."\n'
    '  •  "Full stop"  →  adds a period\n'
    '  •  "New line"   →  moves to the next line\n'
    '  •  "Delete last word"  →  removes the last word\n\n'
    "Your spoken text will appear here with proper punctuation and paragraphs."
)

_AI_TOOLS = [
    ("✨  Correct Grammar",    "btn_ai"),
    ("🎩  Make Professional",  "btn_ai"),
    ("📝  Summarize",          "btn_ai"),
    ("🔁  Rewrite",            "btn_ai"),
    ("🌐  Translate",          "btn_ai"),
]


class DictationPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dictating = False
        self._build()

    # ── build ───────────────────────────────────────────────────────────────

    def _build(self):
        scroll = QScrollArea()
        scroll.setObjectName("page_scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        lay = QVBoxLayout(content)
        lay.setContentsMargins(28, 22, 28, 22)
        lay.setSpacing(16)

        lay.addWidget(self._header())
        lay.addWidget(self._controls())
        lay.addWidget(self._editor(), 1)
        lay.addWidget(self._toolbar())
        lay.addWidget(self._ai_section())

        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    # ── header ──────────────────────────────────────────────────────────────

    def _header(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)

        t = QLabel("🎙   Smart Dictation")
        t.setObjectName("page_title")
        t.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        t.setStyleSheet("color:#f0f4ff;")

        s = QLabel(
            "Speak naturally — Smart Dictator converts your voice into "
            "clean, formatted text with proper punctuation and paragraphs."
        )
        s.setObjectName("page_sub")
        s.setFont(QFont("Segoe UI", 13))
        s.setWordWrap(True)

        lay.addWidget(t)
        lay.addWidget(s)
        return w

    # ── top controls (Start/Stop + word count) ───────────────────────────────

    def _controls(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        self._mic_btn = QPushButton("🎙   Start Dictation")
        self._mic_btn.setObjectName("btn_mic_start")
        self._mic_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self._mic_btn.setFixedHeight(52)
        self._mic_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._mic_btn.clicked.connect(self._toggle)

        self._status = QLabel("▪ ▪ ▪   Ready")
        self._status.setFont(QFont("Segoe UI", 12))
        self._status.setStyleSheet("color:#4a5780;")

        lay.addWidget(self._mic_btn)
        lay.addWidget(self._status)
        lay.addStretch()

        self._wc = QLabel("0 words")
        self._wc.setFont(QFont("Segoe UI", 12))
        self._wc.setStyleSheet("color:#4a5780;")
        lay.addWidget(self._wc)

        return w

    # ── main text editor ─────────────────────────────────────────────────────

    def _editor(self) -> QTextEdit:
        self._edit = QTextEdit()
        self._edit.setObjectName("dict_editor")
        self._edit.setMinimumHeight(300)
        self._edit.setPlaceholderText(_PLACEHOLDER)
        self._edit.setFont(QFont("Segoe UI", 14))
        self._edit.textChanged.connect(self._update_wc)
        return self._edit

    # ── editor toolbar ───────────────────────────────────────────────────────

    def _toolbar(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        for icon, label, style in [
            ("📋", "Copy Text",  "btn_secondary"),
            ("🗑",  "Clear All",  "btn_danger"),
            ("💾", "Save Note",  "btn_secondary"),
        ]:
            btn = QPushButton(f"{icon}   {label}")
            btn.setObjectName(style)
            btn.setFixedHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            lay.addWidget(btn)

        lay.addStretch()
        return w

    # ── AI writing tools ─────────────────────────────────────────────────────

    def _ai_section(self) -> QWidget:
        card = QWidget()
        card.setObjectName("rp_card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(16, 14, 16, 14)
        cl.setSpacing(10)

        # Header row
        hr = QWidget()
        hr.setStyleSheet("background:transparent;")
        hrl = QHBoxLayout(hr)
        hrl.setContentsMargins(0, 0, 0, 0)

        title = QLabel("✨   AI Writing Tools")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        title.setStyleSheet("color:#f0f4ff;")

        hint = QLabel("Select text in the editor, then choose an action")
        hint.setFont(QFont("Segoe UI", 11))
        hint.setStyleSheet("color:#4a5780; font-style:italic;")

        hrl.addWidget(title)
        hrl.addStretch()
        hrl.addWidget(hint)
        cl.addWidget(hr)

        # Button row
        br = QWidget()
        br.setStyleSheet("background:transparent;")
        brl = QHBoxLayout(br)
        brl.setContentsMargins(0, 0, 0, 0)
        brl.setSpacing(10)

        for label, style in _AI_TOOLS:
            btn = QPushButton(label)
            btn.setObjectName(style)
            btn.setFixedHeight(38)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            brl.addWidget(btn)

        brl.addStretch()
        cl.addWidget(br)
        return card

    # ── slots ────────────────────────────────────────────────────────────────

    def _toggle(self):
        self._dictating = not self._dictating
        if self._dictating:
            self._mic_btn.setText("⏹   Stop Dictation")
            self._mic_btn.setObjectName("btn_mic_stop")
            self._status.setText("▪ ▪ ▪   Listening...")
            self._status.setStyleSheet("color:#a78bfa;")
        else:
            self._mic_btn.setText("🎙   Start Dictation")
            self._mic_btn.setObjectName("btn_mic_start")
            self._status.setText("▪ ▪ ▪   Ready")
            self._status.setStyleSheet("color:#4a5780;")

        self._mic_btn.style().unpolish(self._mic_btn)
        self._mic_btn.style().polish(self._mic_btn)

    def _update_wc(self):
        txt = self._edit.toPlainText().strip()
        n = len(txt.split()) if txt else 0
        self._wc.setText(f"{n} word{'s' if n != 1 else ''}")
