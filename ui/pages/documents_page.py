"""
Smart Dictator — Document Reader Page
Drop zone, file info, content/summary split, Q&A section.
"""
import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QLineEdit, QFrame,
    QScrollArea, QSizePolicy, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


_PLACEHOLDER_DOC = (
    "Document text will appear here after you open a file.\n\n"
    "Supported formats:\n"
    "  •  PDF    — extracted with PyMuPDF\n"
    "  •  DOCX   — extracted with python-docx\n"
    "  •  TXT    — read directly\n\n"
    "Click  📂 Browse File  or drop a document above."
)

_PLACEHOLDER_SUM = "AI-generated summary will appear here after you click Summarize."
_PLACEHOLDER_ANS = "Answer will appear here after you ask a question."


class DocumentsPage(QWidget):

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
        lay.addWidget(self._file_row())
        lay.addWidget(self._doc_info_bar())  # initially hidden
        lay.addWidget(self._action_bar())    # initially disabled
        lay.addWidget(self._content_split(), 1)
        lay.addWidget(self._qa_section())
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

        t = QLabel("📄   Document Reader")
        t.setObjectName("page_title")
        t.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        t.setStyleSheet("color:#f0f4ff;")

        s = QLabel(
            "Open PDF, DOCX, or TXT files — listen, summarize, and ask questions "
            "about any document using your voice."
        )
        s.setObjectName("page_sub")
        s.setFont(QFont("Segoe UI", 13))
        s.setWordWrap(True)

        lay.addWidget(t)
        lay.addWidget(s)
        return w

    # ── drop zone + browse button ────────────────────────────────────────────

    def _file_row(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Drop zone
        drop = QWidget()
        drop.setObjectName("drop_zone")
        drop.setFixedHeight(100)
        drop.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        drop.setCursor(Qt.CursorShape.PointingHandCursor)

        dl = QVBoxLayout(drop)
        dl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dl.setSpacing(4)

        di = QLabel("📂")
        di.setFont(QFont("Segoe UI Emoji", 26))
        di.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dt = QLabel("Drop a document here  or  click to browse")
        dt.setFont(QFont("Segoe UI", 13))
        dt.setStyleSheet("color:#8b9bc8;")
        dt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ds = QLabel("Supports  PDF · DOCX · TXT")
        ds.setFont(QFont("Segoe UI", 10))
        ds.setStyleSheet("color:#4a5780;")
        ds.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dl.addWidget(di)
        dl.addWidget(dt)
        dl.addWidget(ds)

        # Separator
        sep = QLabel("or")
        sep.setFont(QFont("Segoe UI", 12))
        sep.setStyleSheet("color:#4a5780;")
        sep.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sep.setFixedWidth(30)

        # Browse column
        col = QWidget()
        col.setStyleSheet("background:transparent;")
        cl = QVBoxLayout(col)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cl.setSpacing(8)

        browse = QPushButton("📂   Browse File")
        browse.setObjectName("btn_primary")
        browse.setFixedSize(150, 46)
        browse.setCursor(Qt.CursorShape.PointingHandCursor)
        browse.clicked.connect(self._browse)

        fmt = QLabel("PDF  •  DOCX  •  TXT")
        fmt.setFont(QFont("Segoe UI", 10))
        fmt.setStyleSheet("color:#4a5780;")
        fmt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cl.addWidget(browse)
        cl.addWidget(fmt)

        lay.addWidget(drop, 1)
        lay.addWidget(sep)
        lay.addWidget(col)
        return w

    # ── document info bar (hidden until file loaded) ─────────────────────────

    def _doc_info_bar(self) -> QWidget:
        self._info_bar = QWidget()
        self._info_bar.setObjectName("rp_card")
        self._info_bar.setVisible(False)

        lay = QHBoxLayout(self._info_bar)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(12)

        icon = QLabel("📄")
        icon.setFont(QFont("Segoe UI Emoji", 26))
        icon.setFixedWidth(36)

        info = QWidget()
        info.setStyleSheet("background:transparent;")
        il = QVBoxLayout(info)
        il.setContentsMargins(0, 0, 0, 0)
        il.setSpacing(2)

        self._doc_name = QLabel("No document loaded")
        self._doc_name.setFont(QFont("Segoe UI", 14, QFont.Weight.DemiBold))
        self._doc_name.setStyleSheet("color:#f0f4ff;")

        self._doc_meta = QLabel("—")
        self._doc_meta.setFont(QFont("Segoe UI", 11))
        self._doc_meta.setStyleSheet("color:#4a5780;")

        il.addWidget(self._doc_name)
        il.addWidget(self._doc_meta)

        close = QPushButton("✕   Close")
        close.setObjectName("btn_danger")
        close.setFixedHeight(36)
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.clicked.connect(self._close_doc)

        lay.addWidget(icon)
        lay.addWidget(info)
        lay.addStretch()
        lay.addWidget(close)

        return self._info_bar

    # ── action bar ───────────────────────────────────────────────────────────

    def _action_bar(self) -> QWidget:
        self._actions = QWidget()
        self._actions.setEnabled(False)

        lay = QHBoxLayout(self._actions)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        for icon, label, style in [
            ("🔊", "Read Aloud",   "btn_mic_start"),
            ("⏹",  "Stop",        "btn_secondary"),
            ("📋", "Copy Text",   "btn_secondary"),
            ("💾", "Save Text",   "btn_secondary"),
            ("📝", "Summarize",   "btn_ai"),
        ]:
            btn = QPushButton(f"{icon}   {label}")
            btn.setObjectName(style)
            btn.setFixedHeight(44)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            lay.addWidget(btn)

        lay.addStretch()
        return self._actions

    # ── content / summary split ──────────────────────────────────────────────

    def _content_split(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # Left — document text
        left = QWidget()
        left.setStyleSheet("background:transparent;")
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(8)

        lbl = QLabel("Document Content")
        lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        lbl.setStyleSheet("color:#f0f4ff;")

        self._doc_view = QTextEdit()
        self._doc_view.setObjectName("ocr_output")
        self._doc_view.setMinimumHeight(260)
        self._doc_view.setFont(QFont("Segoe UI", 13))
        self._doc_view.setReadOnly(True)
        self._doc_view.setPlaceholderText(_PLACEHOLDER_DOC)

        ll.addWidget(lbl)
        ll.addWidget(self._doc_view)

        # Right — AI summary
        right = QWidget()
        right.setStyleSheet("background:transparent;")
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)

        shr = QWidget()
        shr.setStyleSheet("background:transparent;")
        shrl = QHBoxLayout(shr)
        shrl.setContentsMargins(0, 0, 0, 0)

        slbl = QLabel("✨   AI Summary")
        slbl.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        slbl.setStyleSheet("color:#f0f4ff;")

        sbtn = QPushButton("Summarize")
        sbtn.setObjectName("btn_ai")
        sbtn.setCursor(Qt.CursorShape.PointingHandCursor)

        shrl.addWidget(slbl)
        shrl.addStretch()
        shrl.addWidget(sbtn)

        self._sum_view = QTextEdit()
        self._sum_view.setObjectName("ocr_output")
        self._sum_view.setMinimumHeight(260)
        self._sum_view.setFont(QFont("Segoe UI", 13))
        self._sum_view.setReadOnly(True)
        self._sum_view.setPlaceholderText(_PLACEHOLDER_SUM)

        rl.addWidget(shr)
        rl.addWidget(self._sum_view)

        lay.addWidget(left, 3)
        lay.addWidget(right, 2)
        return w

    # ── Q&A section ──────────────────────────────────────────────────────────

    def _qa_section(self) -> QWidget:
        card = QWidget()
        card.setObjectName("rp_card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(16, 14, 16, 14)
        cl.setSpacing(10)

        # Title row
        tr = QWidget()
        tr.setStyleSheet("background:transparent;")
        trl = QHBoxLayout(tr)
        trl.setContentsMargins(0, 0, 0, 0)

        title = QLabel("🤔   Ask About This Document")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        title.setStyleSheet("color:#f0f4ff;")

        hint = QLabel('e.g.  "What is the deadline?"   "Summarize chapter 2"')
        hint.setFont(QFont("Segoe UI", 11))
        hint.setStyleSheet("color:#4a5780; font-style:italic;")

        trl.addWidget(title)
        trl.addStretch()
        trl.addWidget(hint)
        cl.addWidget(tr)

        # Input row
        ir = QWidget()
        ir.setStyleSheet("background:transparent;")
        irl = QHBoxLayout(ir)
        irl.setContentsMargins(0, 0, 0, 0)
        irl.setSpacing(10)

        self._qa_input = QLineEdit()
        self._qa_input.setObjectName("qa_input")
        self._qa_input.setPlaceholderText("Type or speak your question about the document...")
        self._qa_input.setFixedHeight(42)
        self._qa_input.setFont(QFont("Segoe UI", 13))

        ask = QPushButton("Ask →")
        ask.setObjectName("btn_primary")
        ask.setFixedSize(80, 42)
        ask.setCursor(Qt.CursorShape.PointingHandCursor)

        mic = QPushButton("🎤")
        mic.setObjectName("btn_icon")
        mic.setFixedSize(42, 42)
        mic.setCursor(Qt.CursorShape.PointingHandCursor)

        irl.addWidget(self._qa_input)
        irl.addWidget(ask)
        irl.addWidget(mic)
        cl.addWidget(ir)

        # Answer area
        self._qa_answer = QTextEdit()
        self._qa_answer.setObjectName("ocr_output")
        self._qa_answer.setFixedHeight(72)
        self._qa_answer.setFont(QFont("Segoe UI", 13))
        self._qa_answer.setReadOnly(True)
        self._qa_answer.setPlaceholderText(_PLACEHOLDER_ANS)
        cl.addWidget(self._qa_answer)

        return card

    # ── slots ────────────────────────────────────────────────────────────────

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Document", "",
            "Documents (*.pdf *.docx *.txt);;"
            "PDF Files (*.pdf);;Word Documents (*.docx);;Text Files (*.txt)"
        )
        if not path:
            return
        name = os.path.basename(path)
        size = os.path.getsize(path)
        size_str = f"{size // 1024} KB" if size < 1024**2 else f"{size / 1024**2:.1f} MB"
        ext = path.rsplit(".", 1)[-1].upper()

        self._doc_name.setText(name)
        self._doc_meta.setText(f"{ext}  •  {size_str}  •  {path}")
        self._info_bar.setVisible(True)
        self._actions.setEnabled(True)

    def _close_doc(self):
        self._info_bar.setVisible(False)
        self._actions.setEnabled(False)
        self._doc_name.setText("No document loaded")
        self._doc_meta.setText("—")
        self._doc_view.clear()
        self._sum_view.clear()
        self._qa_answer.clear()
