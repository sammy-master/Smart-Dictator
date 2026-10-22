"""
Smart Dictator — Global QSS Stylesheet & Color Palette
Dark navy / purple / cyan design system
"""

# ── Color tokens ────────────────────────────────────────────────────────────
C = {
    "bg":            "#070d1f",   # deepest background
    "bg2":           "#0d1526",   # secondary background
    "bg3":           "#111827",   # card background
    "bg4":           "#1a2235",   # card hover
    "sidebar":       "#080e20",   # sidebar background
    "purple":        "#7c3aed",   # accent purple
    "purple_dark":   "#4c1d95",   # dim purple (for selection)
    "purple_nav":    "#2d1b69",   # active nav bg
    "blue":          "#3b82f6",   # accent blue
    "cyan":          "#22d3ee",   # accent cyan
    "text":          "#f0f4ff",   # primary text
    "text2":         "#8b9bc8",   # secondary text
    "text3":         "#4a5780",   # muted text
    "border":        "#1e2d4a",   # default border
    "border2":       "#243059",   # chip border
    "green":         "#10b981",   # success
    "yellow":        "#f59e0b",   # warning
    "red":           "#ef4444",   # error / danger
    "nav_text":      "#a78bfa",   # active nav text
    "safe_bg":       "#071510",   # safe mode bar bg
    "safe_border":   "#1a4a2a",   # safe mode border
    "safe_text":     "#34d399",   # safe mode text
}

APP_STYLE = f"""
/* =================================================================
   SMART DICTATOR  —  Global QSS Stylesheet
   ================================================================= */

* {{
    font-family: 'Segoe UI', Arial, sans-serif;
    outline: none;
    box-sizing: border-box;
}}

/* ---------- Scrollbar ------------------------------------------ */
QScrollBar:vertical {{
    background: {C['bg2']};
    width: 5px;
    border-radius: 3px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {C['purple_dark']};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {C['purple']};
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {C['bg2']};
    height: 5px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {C['purple_dark']};
    border-radius: 3px;
}}

/* ---------- Root / Window --------------------------------------- */
QMainWindow  {{ background: {C['bg']}; }}
QWidget      {{ background: transparent; color: {C['text']}; }}
QWidget#root {{ background: {C['bg']}; }}

/* ---------- Sidebar -------------------------------------------- */
QWidget#sidebar {{
    background: {C['sidebar']};
    border-right: 1px solid {C['border']};
    min-width: 210px;
    max-width: 210px;
}}

QWidget#logo_area {{
    background: transparent;
}}

QLabel#logo_badge {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 {C['purple']}, stop:1 {C['blue']});
    border-radius: 10px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    qproperty-alignment: AlignCenter;
}}

QLabel#logo_name {{
    color: {C['text']};
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QLabel#logo_sub {{
    color: {C['purple']};
    font-size: 8px;
    letter-spacing: 2px;
}}

/* ---------- Nav buttons ---------------------------------------- */
QPushButton#nav_btn {{
    background: transparent;
    color: {C['text2']};
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0px;
    padding: 9px 14px;
    text-align: left;
    font-size: 12px;
    font-weight: 500;
}}
QPushButton#nav_btn:hover {{
    background: #142040;
    color: #c4b5fd;
}}
QPushButton#nav_btn[active="true"] {{
    background: {C['purple_nav']};
    color: {C['nav_text']};
    font-weight: 600;
    border-left: 3px solid {C['purple']};
}}

/* ---------- Promo card ----------------------------------------- */
QWidget#promo_card {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #1a0e40, stop:1 #0d1535);
    border-radius: 14px;
    border: 1px solid #2d1b69;
}}

QLabel#promo_main   {{ color: {C['text']};  font-size: 11px; font-weight: 600; }}
QLabel#promo_accent {{ color: {C['nav_text']}; font-size: 13px; font-weight: 700; }}
QLabel#promo_sub    {{ color: {C['text3']}; font-size: 10px; }}

/* ---------- User area ------------------------------------------ */
QWidget#user_area {{
    background: #0a1020;
    border-top: 1px solid {C['border']};
}}

QLabel#user_avatar {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 {C['purple']}, stop:1 {C['blue']});
    border-radius: 18px;
    color: white;
    font-size: 14px;
    font-weight: bold;
    qproperty-alignment: AlignCenter;
}}

QLabel#user_name {{ color: {C['text']};  font-size: 13px; font-weight: 600; }}
QLabel#user_role {{ color: {C['text3']}; font-size: 10px; }}

/* ---------- Top bar -------------------------------------------- */
QWidget#top_bar {{
    background: {C['bg']};
    border-bottom: 1px solid {C['border']};
    min-height: 46px;
    max-height: 46px;
}}

QPushButton#hamburger_btn {{
    background: transparent;
    color: {C['text2']};
    border: none;
    font-size: 20px;
    padding: 4px 8px;
    border-radius: 6px;
}}
QPushButton#hamburger_btn:hover {{
    background: #142040;
    color: {C['text']};
}}

QLabel#top_bar_label {{
    color: {C['text2']};
    font-size: 12px;
}}

QPushButton#lang_btn {{
    background: #142040;
    color: {C['text2']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 5px 14px;
    font-size: 12px;
}}
QPushButton#lang_btn:hover {{
    border-color: {C['purple']};
    color: {C['text']};
}}

/* ---------- Content & scroll ----------------------------------- */
QWidget#content_area {{ background: {C['bg']}; }}

QScrollArea#page_scroll {{
    background: {C['bg']};
    border: none;
}}

/* ---------- Page headers --------------------------------------- */
QLabel#page_title {{
    color: {C['text']};
    font-size: 24px;
    font-weight: 700;
}}
QLabel#page_sub {{
    color: {C['text2']};
    font-size: 13px;
}}

/* ---------- Greeting ------------------------------------------- */
QLabel#greeting      {{ color: {C['text']};   font-size: 32px; font-weight: 700; }}
QLabel#greeting_user {{ color: {C['purple']}; font-size: 32px; font-weight: 700; }}
QLabel#greeting_sub  {{ color: {C['text2']};  font-size: 13px; }}

/* ---------- Mic card ------------------------------------------- */
QWidget#mic_card {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #0e1628, stop:1 #080e1e);
    border-radius: 14px;
    border: 1px solid {C['border']};
}}

QLabel#mic_state {{ color: {C['text']};  font-size: 17px; font-weight: 600; }}
QLabel#mic_hint  {{ color: {C['text3']}; font-size: 12px; }}

/* ---------- Chips ---------------------------------------------- */
QPushButton#chip {{
    background: #131e38;
    color: {C['text2']};
    border: 1px solid {C['border2']};
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 11px;
}}
QPushButton#chip:hover {{
    background: #1e2d4a;
    color: {C['cyan']};
    border-color: {C['cyan']};
}}

/* ---------- Quick action cards --------------------------------- */
QWidget#qa_card {{
    background: {C['bg3']};
    border-radius: 12px;
    border: 1px solid {C['border']};
}}
QWidget#qa_card:hover {{
    border-color: {C['purple']};
    background: #1a2440;
}}

/* ---------- Safe mode bar -------------------------------------- */
QWidget#safe_bar {{
    background: {C['safe_bg']};
    border: 1px solid {C['safe_border']};
    border-radius: 8px;
}}
QLabel#safe_title {{ color: {C['safe_text']}; font-size: 12px; font-weight: 700; }}
QLabel#safe_sub   {{ color: #5a8a6e;          font-size: 11px; }}

QPushButton#view_activity_btn {{
    background: transparent;
    color: {C['text2']};
    border: none;
    font-size: 12px;
    padding: 0 4px;
}}
QPushButton#view_activity_btn:hover {{ color: {C['purple']}; }}

/* ---------- Right-panel cards ---------------------------------- */
QWidget#rp_card {{
    background: {C['bg3']};
    border-radius: 12px;
    border: 1px solid {C['border']};
}}
QLabel#rp_title {{ color: {C['text']};   font-size: 13px; font-weight: 600; }}

QPushButton#view_all_btn {{
    background: transparent;
    color: {C['purple']};
    border: none;
    font-size: 12px;
    padding: 0;
}}
QPushButton#view_all_btn:hover {{ color: {C['cyan']}; }}

/* ---------- Stat items ----------------------------------------- */
QWidget#stat_item {{ background: #0f1a30; border-radius: 10px; }}
QLabel#stat_count {{ color: {C['text']};  font-size: 20px; font-weight: 700; }}
QLabel#stat_label {{ color: {C['text2']}; font-size: 10px; }}

/* ---------- Command items -------------------------------------- */
QWidget#cmd_item  {{ background: #0f1a30; border-radius: 8px; }}
QLabel#cmd_text   {{ color: {C['text']};  font-size: 12px; font-weight: 500; }}
QLabel#cmd_time   {{ color: {C['text3']}; font-size: 10px; }}

/* ---------- System status ------------------------------------- */
QLabel#sys_label {{ color: {C['text2']};  font-size: 12px; }}
QLabel#sys_ok    {{ color: {C['green']};  font-size: 12px; font-weight: 600; }}
QLabel#sys_warn  {{ color: {C['yellow']}; font-size: 12px; font-weight: 600; }}

/* ---------- Dictation editor ----------------------------------- */
QTextEdit#dict_editor {{
    background: #0d1424;
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 18px;
    font-size: 15px;
    selection-background-color: {C['purple_dark']};
}}
QTextEdit#dict_editor:focus {{ border-color: {C['purple']}; }}

/* ---------- OCR / doc output ----------------------------------- */
QTextEdit#ocr_output {{
    background: #0d1424;
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 16px;
    font-size: 14px;
    selection-background-color: {C['purple_dark']};
}}

/* ---------- Document drop zone --------------------------------- */
QWidget#drop_zone {{
    background: #0d1424;
    border: 2px dashed {C['border']};
    border-radius: 16px;
}}
QWidget#drop_zone:hover {{ border-color: {C['purple']}; }}

/* ---------- Q&A input ------------------------------------------ */
QLineEdit#qa_input {{
    background: #0d1424;
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 13px;
    selection-background-color: {C['purple_dark']};
}}
QLineEdit#qa_input:focus {{ border-color: {C['purple']}; }}

/* ---------- History items -------------------------------------- */
QWidget#hist_item {{
    background: {C['bg3']};
    border: 1px solid {C['border']};
    border-radius: 8px;
}}
QLabel#hist_time   {{ color: {C['text3']}; font-size: 11px; }}
QLabel#hist_cmd    {{ color: {C['text']};  font-size: 13px; font-weight: 500; }}
QLabel#hist_status {{ color: {C['green']}; font-size: 11px; }}

/* ---------- Tab filter buttons --------------------------------- */
QPushButton#tab_btn {{
    background: transparent;
    color: {C['text3']};
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 6px 18px;
    font-size: 12px;
    font-weight: 500;
}}
QPushButton#tab_btn:hover {{
    background: #142040;
    color: {C['text']};
}}
QPushButton#tab_btn[active="true"] {{
    background: {C['purple_nav']};
    color: {C['nav_text']};
    border-color: {C['purple_dark']};
    font-weight: 600;
}}

/* ---------- Settings ------------------------------------------- */
QWidget#settings_section {{
    background: {C['bg3']};
    border-radius: 12px;
    border: 1px solid {C['border']};
}}
QLabel#section_header {{ color: {C['purple']}; font-size: 9px; font-weight: 700; letter-spacing: 2px; }}
QLabel#setting_name   {{ color: {C['text']};   font-size: 13px; font-weight: 500; }}
QLabel#setting_desc   {{ color: {C['text3']};  font-size: 11px; }}

QComboBox#settings_combo {{
    background: #142040;
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    min-width: 160px;
}}
QComboBox#settings_combo:hover {{ border-color: {C['purple']}; }}
QComboBox#settings_combo::drop-down {{ border: none; width: 20px; }}
QComboBox QAbstractItemView {{
    background: #0d1424;
    color: {C['text']};
    border: 1px solid {C['border']};
    selection-background-color: {C['purple_dark']};
    border-radius: 6px;
    padding: 4px;
    outline: none;
}}

QSlider::groove:horizontal {{
    background: #1e2d4a;
    height: 4px;
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {C['purple']};
    width: 16px; height: 16px;
    border-radius: 8px;
    margin: -6px 0;
    border: 2px solid #0d1526;
}}
QSlider::sub-page:horizontal {{
    background: {C['purple']};
    border-radius: 2px;
}}

/* ============================================================
   GENERIC BUTTON STYLES
   ============================================================ */

QPushButton#btn_primary {{
    background: {C['purple']};
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
}}
QPushButton#btn_primary:hover   {{ background: #6d28d9; }}
QPushButton#btn_primary:pressed {{ background: #5b21b6; }}

QPushButton#btn_secondary {{
    background: #142040;
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 500;
}}
QPushButton#btn_secondary:hover {{ background: #1e2d4a; border-color: {C['blue']}; }}

QPushButton#btn_ai {{
    background: #0f1f3d;
    color: {C['cyan']};
    border: 1px solid #1a3a5c;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 500;
}}
QPushButton#btn_ai:hover {{ background: #142b4d; border-color: {C['cyan']}; }}

QPushButton#btn_danger {{
    background: transparent;
    color: {C['red']};
    border: 1px solid {C['red']};
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
}}
QPushButton#btn_danger:hover {{ background: #2d0a0a; }}

QPushButton#btn_icon {{
    background: #142040;
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
}}
QPushButton#btn_icon:hover {{ background: #1e2d4a; border-color: {C['purple']}; }}

QPushButton#btn_mic_start {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {C['purple']}, stop:1 {C['blue']});
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: 700;
}}
QPushButton#btn_mic_start:hover {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #6d28d9, stop:1 {C['purple']});
}}

QPushButton#btn_mic_stop {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #9f1239, stop:1 {C['red']});
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: 700;
}}
QPushButton#btn_mic_stop:hover {{ background: {C['red']}; }}

/* ---------- Status bar ---------------------------------------- */
QStatusBar {{
    background: #050a15;
    color: {C['text3']};
    font-size: 11px;
    border-top: 1px solid {C['border']};
}}
"""
