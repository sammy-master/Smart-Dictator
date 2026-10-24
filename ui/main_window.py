"""
Smart Dictator — Main Window
Assembles: Sidebar | TopBar | QStackedWidget (6 pages)
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
    QSizePolicy, QScrollArea
)
import webbrowser
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QScreen

from ui.styles import APP_STYLE
from ui.widgets.mic_button import ToggleSwitch


NAV_ITEMS = [
    ("🏠", "Home",          0),
    ("🎙", "Dictation",     1),
    ("👁", "Screen Reader", 2),
    ("📄", "Documents",     3),
    ("🕐", "History",       4),
    ("⚙",  "Settings",     5),
]


# ═══════════════════════════════════════════════════════════════════════════
#  Sidebar
# ═══════════════════════════════════════════════════════════════════════════

class Sidebar(QWidget):
    page_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(210)
        self._btns: list[QPushButton] = []
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._logo())

        nav_w = QWidget()
        nav_l = QVBoxLayout(nav_w)
        nav_l.setContentsMargins(0, 8, 0, 8)
        nav_l.setSpacing(0)

        for icon, label, idx in NAV_ITEMS:
            btn = self._nav_btn(icon, label, idx)
            self._btns.append(btn)
            nav_l.addWidget(btn)

        nav_l.addStretch()
        root.addWidget(nav_w, 1)

        root.addWidget(self._promo_card())
        root.addSpacing(6)
        root.addWidget(self._user_area())

        self._set_active(0)

    def _logo(self) -> QWidget:
        wrapper = QWidget()
        wrapper.setObjectName("logo_area")
        wl = QVBoxLayout(wrapper)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.setSpacing(0)

        inner = QWidget()
        inner.setFixedHeight(64)
        lay = QHBoxLayout(inner)
        lay.setContentsMargins(14, 0, 14, 0)
        lay.setSpacing(10)

        badge = QLabel("◈")
        badge.setObjectName("logo_badge")
        badge.setFixedSize(36, 36)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFont(QFont("Segoe UI", 16))

        text = QWidget()
        tl = QVBoxLayout(text)
        tl.setContentsMargins(0, 0, 0, 0)
        tl.setSpacing(1)

        name = QLabel("SMART DICTATOR")
        name.setObjectName("logo_name")
        name.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        sub = QLabel("AI ACCESSIBILITY AGENT")
        sub.setObjectName("logo_sub")
        sub.setFont(QFont("Segoe UI", 7))

        tl.addWidget(name)
        tl.addWidget(sub)

        lay.addWidget(badge)
        lay.addWidget(text)
        lay.addStretch()

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background:#1e2d4a; max-height:1px; min-height:1px;")

        wl.addWidget(inner)
        wl.addWidget(sep)
        return wrapper

    def _nav_btn(self, icon: str, label: str, idx: int) -> QPushButton:
        btn = QPushButton(f"   {icon}   {label}")
        btn.setObjectName("nav_btn")
        btn.setFixedHeight(42)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 12))
        btn.clicked.connect(lambda _=False, i=idx: self._on_click(i))
        return btn

    def _promo_card(self) -> QWidget:
        wrap = QWidget()
        wl = QHBoxLayout(wrap)
        wl.setContentsMargins(8, 0, 8, 0)

        card = QWidget()
        card.setObjectName("promo_card")
        card.setFixedHeight(100)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 8, 12, 8)
        cl.setSpacing(2)
        cl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        emoji = QLabel("🎤")
        emoji.setFont(QFont("Segoe UI Emoji", 18))
        emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for text, obj in [
            ("Your Voice. Your Commands.", "promo_main"),
            ("Complete Freedom.",          "promo_accent"),
            ("Empowering accessibility.",  "promo_sub"),
        ]:
            lbl = QLabel(text)
            lbl.setObjectName(obj)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cl.addWidget(lbl)

        cl.insertWidget(0, emoji)
        wl.addWidget(card)
        return wrap

    def _user_area(self) -> QWidget:
        w = QWidget()
        w.setObjectName("user_area")
        w.setFixedHeight(56)

        lay = QHBoxLayout(w)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(10)

        avatar = QLabel("S")
        avatar.setObjectName("user_avatar")
        avatar.setFixedSize(34, 34)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

        info = QWidget()
        info.setStyleSheet("background:transparent;")
        il = QVBoxLayout(info)
        il.setContentsMargins(0, 0, 0, 0)
        il.setSpacing(1)

        name = QLabel("Saksham Sharma")
        name.setObjectName("user_name")
        name.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

        role = QLabel("Student  ·  SIH 2026")
        role.setObjectName("user_role")
        role.setFont(QFont("Segoe UI", 9))

        il.addWidget(name)
        il.addWidget(role)

        lay.addWidget(avatar)
        lay.addWidget(info)
        lay.addStretch()
        
        port_btn = QPushButton("??")
        port_btn.setToolTip("Open Saksham Sharma Portfolio")
        port_btn.setFixedSize(26, 26)
        port_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        port_btn.setStyleSheet("background: rgba(168,85,247,0.15); border: 1px solid rgba(168,85,247,0.3); border-radius: 6px; color: #c084fc; font-size: 11px;")
        port_btn.clicked.connect(lambda: webbrowser.open("https://saksham-personalportfolio.vercel.app"))
        lay.addWidget(port_btn)
        
        return w

    def _on_click(self, idx: int):
        self._set_active(idx)
        self.page_changed.emit(idx)

    def _set_active(self, idx: int):
        for i, btn in enumerate(self._btns):
            btn.setProperty("active", i == idx)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def navigate_to(self, idx: int):
        self._set_active(idx)


# ═══════════════════════════════════════════════════════════════════════════
#  TopBar
# ═══════════════════════════════════════════════════════════════════════════

class TopBar(QWidget):
    offline_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("top_bar")
        self.setFixedHeight(46)
        self._build()

    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 0, 18, 0)
        lay.setSpacing(12)

        ham = QPushButton("≡")
        ham.setObjectName("hamburger_btn")
        ham.setFixedSize(34, 34)
        ham.setFont(QFont("Segoe UI", 19))
        ham.setCursor(Qt.CursorShape.PointingHandCursor)
        lay.addWidget(ham)

        lay.addStretch()

        offline_lbl = QLabel("Offline Mode")
        offline_lbl.setObjectName("top_bar_label")
        offline_lbl.setFont(QFont("Segoe UI", 12))

        self.toggle = ToggleSwitch(checked=False)
        self.toggle.toggled.connect(self.offline_toggled.emit)

        lang = QPushButton("🌐   English  ▾")
        lang.setObjectName("lang_btn")
        lang.setCursor(Qt.CursorShape.PointingHandCursor)

        lay.addWidget(offline_lbl)
        lay.addWidget(self.toggle)
        lay.addSpacing(10)
        lay.addWidget(lang)


# ═══════════════════════════════════════════════════════════════════════════
#  MainWindow
# ═══════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Dictator  —  AI Voice Accessibility  |  SIH 2026")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(APP_STYLE)
        self._build()

    def _build(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        rl = QHBoxLayout(root)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._go)
        rl.addWidget(self.sidebar)

        right = QWidget()
        right.setObjectName("content_area")
        rr = QVBoxLayout(right)
        rr.setContentsMargins(0, 0, 0, 0)
        rr.setSpacing(0)

        self.top_bar = TopBar()
        rr.addWidget(self.top_bar)

        self.stack = QStackedWidget()
        self.stack.setObjectName("pages")
        rr.addWidget(self.stack, 1)

        rl.addWidget(right, 1)

        self._load_pages()

    def _load_pages(self):
        from ui.pages.home_page          import HomePage
        from ui.pages.dictation_page     import DictationPage
        from ui.pages.screen_reader_page import ScreenReaderPage
        from ui.pages.documents_page     import DocumentsPage
        from ui.pages.history_page       import HistoryPage
        from ui.pages.settings_page      import SettingsPage

        for PageClass in [HomePage, DictationPage, ScreenReaderPage,
                          DocumentsPage, HistoryPage, SettingsPage]:
            self.stack.addWidget(PageClass(self))

        self.stack.setCurrentIndex(0)

    def _go(self, idx: int):
        self.stack.setCurrentIndex(idx)
