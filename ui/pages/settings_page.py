"""
Smart Dictator — Settings Page
Voice, Language, Accessibility, AI, Voice Programs, System sections.
"""
import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSlider, QScrollArea,
    QFrame, QLineEdit, QFileDialog, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.widgets.mic_button import ToggleSwitch


# ── Default registered programs ─────────────────────────────────────────────
_DEFAULT_PROGRAMS = [
    ("Chrome",        r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    ("VS Code",       r"C:\Users\admin\AppData\Local\Programs\Microsoft VS Code\Code.exe"),
    ("Notepad",       r"C:\Windows\System32\notepad.exe"),
    ("File Explorer", r"C:\Windows\explorer.exe"),
    ("VLC",           r"C:\Program Files\VideoLAN\VLC\vlc.exe"),
]


# ═══════════════════════════════════════════════════════════════════════════
#  ProgramsManager — inline add/remove widget
# ═══════════════════════════════════════════════════════════════════════════

class ProgramsManager(QWidget):
    """
    Shows registered voice→program mappings and lets the user
    add new ones (browse .exe) or remove existing ones.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:transparent;")
        self._items: list[QWidget] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # List
        self._list_w = QWidget()
        self._list_w.setStyleSheet("background:transparent;")
        self._list_lay = QVBoxLayout(self._list_w)
        self._list_lay.setContentsMargins(0, 0, 0, 0)
        self._list_lay.setSpacing(5)

        for name, path in _DEFAULT_PROGRAMS:
            self._add_item(name, path, startup=True)

        root.addWidget(self._list_w)
        root.addSpacing(10)
        root.addWidget(self._add_form())

    # ── item row ─────────────────────────────────────────────────────────────

    def _add_item(self, name: str, path: str, startup: bool = False):
        row = QWidget()
        row.setFixedHeight(38)
        row.setStyleSheet(
            "background:#0f1a30; border-radius:8px; border:1px solid #1e2d4a;"
        )

        lay = QHBoxLayout(row)
        lay.setContentsMargins(12, 0, 10, 0)
        lay.setSpacing(10)

        icon = QLabel("⚡")
        icon.setFixedWidth(14)
        icon.setFont(QFont("Segoe UI", 11))
        icon.setStyleSheet("color:#7c3aed; background:transparent; border:none;")

        name_l = QLabel(name)
        name_l.setFixedWidth(120)
        name_l.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        name_l.setStyleSheet("color:#f0f4ff; background:transparent; border:none;")

        # Truncate long paths for display
        disp = path if len(path) <= 52 else "…" + path[-50:]
        path_l = QLabel(disp)
        path_l.setFont(QFont("Segoe UI", 10))
        path_l.setStyleSheet("color:#4a5780; background:transparent; border:none;")
        path_l.setToolTip(path)

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(26, 26)
        del_btn.setStyleSheet("""
            QPushButton {
                background:#1a0a0a; color:#ef4444;
                border:1px solid #3d1a1a; border-radius:6px;
                font-size:10px; font-weight:bold;
            }
            QPushButton:hover { background:#2d0a0a; }
        """)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.clicked.connect(lambda _=False, r=row: self._remove_item(r))

        lay.addWidget(icon)
        lay.addWidget(name_l)
        lay.addWidget(path_l, 1)
        lay.addWidget(del_btn)

        self._items.append(row)
        if startup:
            self._list_lay.addWidget(row)
        else:
            # Insert before stretch (if any) — just append
            self._list_lay.addWidget(row)

    def _remove_item(self, row: QWidget):
        if row in self._items:
            self._items.remove(row)
        self._list_lay.removeWidget(row)
        row.deleteLater()

    # ── add form ─────────────────────────────────────────────────────────────

    def _add_form(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        self._name_in = QLineEdit()
        self._name_in.setObjectName("qa_input")
        self._name_in.setPlaceholderText("Voice name  (e.g. Chrome)")
        self._name_in.setFixedHeight(36)
        self._name_in.setFixedWidth(155)
        self._name_in.setFont(QFont("Segoe UI", 12))

        self._path_in = QLineEdit()
        self._path_in.setObjectName("qa_input")
        self._path_in.setPlaceholderText("Application path  (.exe)…")
        self._path_in.setFixedHeight(36)
        self._path_in.setFont(QFont("Segoe UI", 12))

        browse = QPushButton("📂  Browse")
        browse.setObjectName("btn_secondary")
        browse.setFixedHeight(36)
        browse.setCursor(Qt.CursorShape.PointingHandCursor)
        browse.clicked.connect(self._browse)

        add = QPushButton("＋  Add")
        add.setObjectName("btn_primary")
        add.setFixedHeight(36)
        add.setFixedWidth(82)
        add.setCursor(Qt.CursorShape.PointingHandCursor)
        add.clicked.connect(self._add_new)

        lay.addWidget(self._name_in)
        lay.addWidget(self._path_in, 1)
        lay.addWidget(browse)
        lay.addWidget(add)
        return w

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Application",
            r"C:\Program Files",
            "Executables (*.exe);;All Files (*.*)"
        )
        if path:
            self._path_in.setText(path)
            if not self._name_in.text().strip():
                self._name_in.setText(
                    os.path.splitext(os.path.basename(path))[0]
                )

    def _add_new(self):
        name = self._name_in.text().strip()
        path = self._path_in.text().strip()
        if name and path:
            self._add_item(name, path)
            self._name_in.clear()
            self._path_in.clear()


# ═══════════════════════════════════════════════════════════════════════════
#  SettingsPage
# ═══════════════════════════════════════════════════════════════════════════

class SettingsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setObjectName("page_scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        lay = QVBoxLayout(content)
        lay.setContentsMargins(26, 18, 26, 18)
        lay.setSpacing(14)

        lay.addWidget(self._header())
        lay.addWidget(self._voice_section())
        lay.addWidget(self._language_section())
        lay.addWidget(self._accessibility_section())
        lay.addWidget(self._ai_section())
        lay.addWidget(self._programs_section())   # ← new
        lay.addWidget(self._system_section())
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
        lay.setSpacing(3)

        t = QLabel("⚙   Settings")
        t.setObjectName("page_title")
        t.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        t.setStyleSheet("color:#f0f4ff;")

        s = QLabel(
            "Configure Smart Dictator to match your preferences "
            "and accessibility needs."
        )
        s.setObjectName("page_sub")
        s.setFont(QFont("Segoe UI", 12))
        s.setWordWrap(True)

        lay.addWidget(t)
        lay.addWidget(s)
        return w

    # ── section factory ──────────────────────────────────────────────────────

    def _section(self, icon: str, title: str) -> tuple[QWidget, QVBoxLayout]:
        card = QWidget()
        card.setObjectName("settings_section")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(18, 14, 18, 16)
        cl.setSpacing(12)

        header = QLabel(f"  {icon}   {title.upper()}")
        header.setObjectName("section_header")
        header.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        header.setStyleSheet("color:#7c3aed; letter-spacing:2px;")
        cl.addWidget(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background:#1e2d4a; max-height:1px; min-height:1px;")
        cl.addWidget(sep)

        return card, cl

    def _row(self, name: str, desc: str, ctrl: QWidget) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 3, 0, 3)
        lay.setSpacing(20)

        col = QWidget()
        col.setStyleSheet("background:transparent;")
        cl = QVBoxLayout(col)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(2)

        nl = QLabel(name)
        nl.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        nl.setStyleSheet("color:#f0f4ff;")

        dl = QLabel(desc)
        dl.setFont(QFont("Segoe UI", 10))
        dl.setStyleSheet("color:#4a5780;")

        cl.addWidget(nl)
        cl.addWidget(dl)

        lay.addWidget(col, 1)
        lay.addWidget(ctrl)
        return w

    # ── controls ─────────────────────────────────────────────────────────────

    def _combo(self, items: list[str], current: str = "") -> QComboBox:
        cb = QComboBox()
        cb.setObjectName("settings_combo")
        cb.addItems(items)
        if current and current in items:
            cb.setCurrentIndex(items.index(current))
        cb.setCursor(Qt.CursorShape.PointingHandCursor)
        return cb

    def _slider(self, lo=0, hi=100, val=50) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        w.setFixedWidth(200)
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        sl = QSlider(Qt.Orientation.Horizontal)
        sl.setMinimum(lo); sl.setMaximum(hi); sl.setValue(val)
        sl.setFixedWidth(155)

        vl = QLabel(str(val))
        vl.setFont(QFont("Segoe UI", 10))
        vl.setStyleSheet("color:#8b9bc8;")
        vl.setFixedWidth(30)

        sl.valueChanged.connect(lambda v: vl.setText(str(v)))
        lay.addWidget(sl)
        lay.addWidget(vl)
        return w

    def _toggle(self, on: bool = False) -> ToggleSwitch:
        return ToggleSwitch(checked=on)

    # ── sections ─────────────────────────────────────────────────────────────

    def _voice_section(self) -> QWidget:
        card, cl = self._section("🎤", "Voice")
        cl.addWidget(self._row(
            "Microphone Input",
            "Select your input device for voice recognition",
            self._combo(["Default Microphone", "Headset Microphone", "USB Microphone"])
        ))
        cl.addWidget(self._row(
            "TTS Voice",
            "Text-to-speech voice for spoken feedback",
            self._combo(["Microsoft Zira (Female)",
                         "Microsoft David (Male)",
                         "Microsoft Aria (Neural)"])
        ))
        cl.addWidget(self._row(
            "Speech Speed",
            "How fast Smart Dictator speaks back  (50 – 200 %)",
            self._slider(50, 200, 100)
        ))
        cl.addWidget(self._row(
            "Microphone Sensitivity",
            "Input volume threshold for voice detection",
            self._slider(0, 100, 60)
        ))
        return card

    def _language_section(self) -> QWidget:
        card, cl = self._section("🌐", "Language")
        cl.addWidget(self._row(
            "Primary Language",
            "Main language for speech recognition and interface",
            self._combo(
                ["English (India)", "English (US)", "Hindi", "Marathi"],
                "English (India)"
            )
        ))
        cl.addWidget(self._row(
            "Multilingual Mode",
            "Auto-detect English, Hindi, and Marathi",
            self._toggle(on=True)
        ))
        cl.addWidget(self._row(
            "Translation Target",
            "Default target language for 'Translate this'",
            self._combo(["Hindi", "English", "Marathi", "Tamil", "Telugu"])
        ))
        return card

    def _accessibility_section(self) -> QWidget:
        card, cl = self._section("♿", "Accessibility")
        cl.addWidget(self._row("High Contrast Mode",
                               "Increase UI contrast for better visibility",
                               self._toggle(on=False)))
        cl.addWidget(self._row("Large Text",
                               "Increase UI text size throughout the application",
                               self._toggle(on=False)))
        cl.addWidget(self._row("Voice Feedback",
                               "Speak a confirmation after every action",
                               self._toggle(on=True)))
        cl.addWidget(self._row("Safe Mode",
                               "Require confirmation before potentially destructive actions",
                               self._toggle(on=True)))
        return card

    def _ai_section(self) -> QWidget:
        card, cl = self._section("🤖", "AI Configuration")
        cl.addWidget(self._row(
            "AI Provider",
            "Generative AI backend for intent understanding and text assistance",
            self._combo(["OpenAI GPT-4o",
                         "OpenAI GPT-3.5 Turbo",
                         "Google Gemini",
                         "Offline (No AI)"])
        ))
        cl.addWidget(self._row(
            "Speech Recognition Engine",
            "Engine used to transcribe your voice to text",
            self._combo(["Faster-Whisper (Local)",
                         "OpenAI Whisper API",
                         "Google Speech API"])
        ))
        cl.addWidget(self._row(
            "OCR Engine",
            "Backend for screen text extraction",
            self._combo(["Tesseract OCR (Local)", "Google Cloud Vision"])
        ))

        # API key row
        api_row = QWidget()
        api_row.setStyleSheet("background:transparent;")
        arl = QHBoxLayout(api_row)
        arl.setContentsMargins(0, 3, 0, 3)
        arl.setSpacing(20)

        tc = QWidget()
        tc.setStyleSheet("background:transparent;")
        tcl = QVBoxLayout(tc)
        tcl.setContentsMargins(0, 0, 0, 0)
        tcl.setSpacing(2)

        nl = QLabel("API Key")
        nl.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        nl.setStyleSheet("color:#f0f4ff;")

        dl = QLabel("Your OpenAI or Gemini API key for online AI features")
        dl.setFont(QFont("Segoe UI", 10))
        dl.setStyleSheet("color:#4a5780;")

        tcl.addWidget(nl); tcl.addWidget(dl)

        cfg = QPushButton("⚙   Configure API Key")
        cfg.setObjectName("btn_secondary")
        cfg.setFixedHeight(36)
        cfg.setCursor(Qt.CursorShape.PointingHandCursor)

        arl.addWidget(tc, 1)
        arl.addWidget(cfg)
        cl.addWidget(api_row)
        return card

    # ── PROGRAMS SECTION ─────────────────────────────────────────────────────

    def _programs_section(self) -> QWidget:
        card, cl = self._section("⚡", "Voice Programs")

        # Description
        desc = QLabel(
            "Register applications that Smart Dictator can open by voice command.\n"
            'Example: say  "Open Chrome"  →  launches chrome.exe'
        )
        desc.setFont(QFont("Segoe UI", 11))
        desc.setStyleSheet("color:#8b9bc8;")
        desc.setWordWrap(True)
        cl.addWidget(desc)

        # Column headers
        headers = QWidget()
        headers.setStyleSheet("background:transparent;")
        hl = QHBoxLayout(headers)
        hl.setContentsMargins(12, 0, 36, 0)
        hl.setSpacing(10)

        for txt, w in [("Voice Name", 120), ("Application Path", 0)]:
            lbl = QLabel(txt)
            lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            lbl.setStyleSheet("color:#4a5780; letter-spacing:1px;")
            if w:
                lbl.setFixedWidth(w + 14)
            hl.addWidget(lbl, 0 if w else 1)

        cl.addWidget(headers)

        # Programs manager
        self._prog_mgr = ProgramsManager()
        cl.addWidget(self._prog_mgr)

        return card

    def _system_section(self) -> QWidget:
        card, cl = self._section("💻", "System")
        cl.addWidget(self._row(
            "Connection Mode",
            "Switch between online (full AI) and offline (local only) mode",
            self._combo(["Online Mode", "Offline Mode"])
        ))
        cl.addWidget(self._row("Start with Windows",
                               "Launch Smart Dictator on system startup",
                               self._toggle(on=False)))
        cl.addWidget(self._row("System Tray Icon",
                               "Keep accessible from the system tray",
                               self._toggle(on=True)))

        # Footer
        footer = QWidget()
        footer.setStyleSheet("background:#0f1a30; border-radius:10px;")
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(14, 8, 14, 8)

        ver = QLabel(
            "Smart Dictator  v1.0.0   ·   SIH 2026"
        )
        ver.setFont(QFont("Segoe UI", 10))
        ver.setStyleSheet("color:#4a5780;")

        reset = QPushButton("↺   Reset to Defaults")
        reset.setObjectName("btn_danger")
        reset.setFixedHeight(34)
        reset.setCursor(Qt.CursorShape.PointingHandCursor)

        fl.addWidget(ver)
        fl.addStretch()
        fl.addWidget(reset)
        cl.addWidget(footer)

        return card
