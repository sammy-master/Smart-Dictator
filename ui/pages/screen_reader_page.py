"""
Smart Dictator — Screen Reader Page
OCR capture, text display, AI summary, TTS read-aloud.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


_PLACEHOLDER_OCR = (
    "Extracted text will appear here after you capture the screen.\n\n"
    "Steps performed automatically:\n"
    "  1. Screenshot your current screen\n"
    "  2. OCR extracts all visible text (Tesseract)\n"
    "  3. Text is cleaned and organised\n"
    "  4. You can then read it aloud or ask questions\n\n"
    "Press  📸  Read My Screen  to begin."
)

_PLACEHOLDER_SUM = (
    "AI description will appear here.\n\n"
    "After OCR, Smart Dictator can:\n"
    "  • Summarise what is on screen\n"
    "  • Describe the main content in natural language\n"
    "  • Answer voice questions about what is visible"
)


class ScreenReaderPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
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
        lay.addWidget(self._how_it_works())
        lay.addWidget(self._action_bar())
        lay.addWidget(self._output_area(), 1)
        lay.addStretch()

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

        t = QLabel("👁   Screen Reader")
        t.setObjectName("page_title")
        t.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        t.setStyleSheet("color:#f0f4ff;")

        s = QLabel(
            "Capture visible text from your screen using AI-powered OCR, "
            "then read it aloud or ask questions about it."
        )
        s.setObjectName("page_sub")
        s.setFont(QFont("Segoe UI", 13))
        s.setWordWrap(True)

        lay.addWidget(t)
        lay.addWidget(s)
        return w

    # ── how it works steps ───────────────────────────────────────────────────

    def _how_it_works(self) -> QWidget:
        card = QWidget()
        card.setObjectName("rp_card")
        lay = QHBoxLayout(card)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(0)

        steps = [
            ("📸", "Capture",   "Screenshots\nyour screen"),
            ("🔍", "OCR",       "Extracts all\nvisible text"),
            ("🧹", "Clean",     "Organises &\nformats output"),
            ("🔊", "Read Aloud","Speaks via\nText-to-Speech"),
        ]

        for i, (icon, name, desc) in enumerate(steps):
            step_w = QWidget()
            step_w.setStyleSheet("background:transparent;")
            sl = QVBoxLayout(step_w)
            sl.setContentsMargins(0, 0, 0, 0)
            sl.setSpacing(4)
            sl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            ic = QLabel(icon)
            ic.setFont(QFont("Segoe UI Emoji", 24))
            ic.setAlignment(Qt.AlignmentFlag.AlignCenter)

            nl = QLabel(name)
            nl.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
            nl.setStyleSheet("color:#f0f4ff;")
            nl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            dl = QLabel(desc)
            dl.setFont(QFont("Segoe UI", 10))
            dl.setStyleSheet("color:#4a5780;")
            dl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            sl.addWidget(ic)
            sl.addWidget(nl)
            sl.addWidget(dl)
            lay.addWidget(step_w, 1)

            if i < len(steps) - 1:
                arrow = QLabel("→")
                arrow.setFont(QFont("Segoe UI", 18))
                arrow.setStyleSheet("color:#2d4070;")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lay.addWidget(arrow)

        return card

    # ── action buttons ───────────────────────────────────────────────────────

    def _action_bar(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        for icon, label, style in [
            ("📸", "Read My Screen", "btn_mic_start"),
            ("🔊", "Read Aloud",     "btn_secondary"),
            ("⏹",  "Stop",           "btn_icon"),
            ("📋", "Copy Text",      "btn_secondary"),
        ]:
            btn = QPushButton(f"{icon}   {label}")
            btn.setObjectName(style)
            btn.setFixedHeight(50)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            lay.addWidget(btn)

        lay.addStretch()
        return w

    # ── dual output panes ────────────────────────────────────────────────────

    def _output_area(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Left — OCR raw
        left = QWidget()
        left.setStyleSheet("background:transparent;")
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(8)

        ocr_lbl = QLabel("Extracted Text (OCR)")
        ocr_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        ocr_lbl.setStyleSheet("color:#f0f4ff;")

        self._ocr = QTextEdit()
        self._ocr.setObjectName("ocr_output")
        self._ocr.setPlaceholderText(_PLACEHOLDER_OCR)
        self._ocr.setMinimumHeight(260)
        self._ocr.setFont(QFont("Segoe UI", 13))
        self._ocr.setReadOnly(True)

        ll.addWidget(ocr_lbl)
        ll.addWidget(self._ocr)

        # Right — AI summary
        right = QWidget()
        right.setStyleSheet("background:transparent;")
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)

        # Summary header row
        shr = QWidget()
        shr.setStyleSheet("background:transparent;")
        shrl = QHBoxLayout(shr)
        shrl.setContentsMargins(0, 0, 0, 0)

        sum_lbl = QLabel("✨   AI Summary / Description")
        sum_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        sum_lbl.setStyleSheet("color:#f0f4ff;")

        sum_btn = QPushButton("Summarize")
        sum_btn.setObjectName("btn_ai")
        sum_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        shrl.addWidget(sum_lbl)
        shrl.addStretch()
        shrl.addWidget(sum_btn)

        self._summary = QTextEdit()
        self._summary.setObjectName("ocr_output")
        self._summary.setPlaceholderText(_PLACEHOLDER_SUM)
        self._summary.setMinimumHeight(260)
        self._summary.setFont(QFont("Segoe UI", 13))
        self._summary.setReadOnly(True)

        rl.addWidget(shr)
        rl.addWidget(self._summary)

        lay.addWidget(left, 1)
        lay.addWidget(right, 1)
        return w
