# Smart Dictator — AI Voice Dictation, Document Reader & Accessibility Suite

**Smart Dictator** is a native desktop assistive technology application built with **Python** and **PySide6 (Qt 6)** for **Smart India Hackathon (SIH 2026)**. It provides a unified, accessible desktop environment for real-time voice dictation, document reading, screen narration, session history tracking, and customizable visual/audio accessibility settings.

---

## Key Features

- **Home Dashboard (`ui/pages/home_page.py`)**: Quick-access launcher with session statistics, recent activity cards, and voice-first shortcuts.
- **Live Voice Dictation Studio (`ui/pages/dictation_page.py` & `ui/widgets/mic_button.py`)**:
  - Interactive animated microphone trigger button (`MicButton`), real-time transcription canvas, punctuation/formatting controls, and one-click copy/export.
- **Document Reader (`ui/pages/documents_page.py`)**:
  - Import and read documents aloud with synchronized highlighting and playback controls.
- **Screen Reader Assistant (`ui/pages/screen_reader_page.py`)**:
  - Assistive screen narration mode for reading active text selections and UI regions.
- **Session History (`ui/pages/history_page.py`)**:
  - Searchable archive of past dictated transcripts and read documents.
- **Accessibility Settings (`ui/pages/settings_page.py` & `ui/styles.py`)**:
  - Adjustable font scaling, high-contrast themes, speech rate, pitch, and input device selection.

---

## Project Structure

```text
Smart Dictator/
├── main.py                      # Application entrypoint (QApplication bootstrap)
├── requirements.txt             # Python dependencies (PySide6>=6.6.0)
└── ui/
    ├── main_window.py           # Sidebar navigation & QStackedWidget window host
    ├── styles.py                # Global Qt Stylesheets (QSS) & theme tokens
    ├── pages/
    │   ├── home_page.py         # Overview & quick actions page
    │   ├── dictation_page.py    # Live Speech-to-Text dictation workspace
    │   ├── documents_page.py    # Document import & Text-to-Speech reader
    │   ├── screen_reader_page.py# Assistive screen reader controller
    │   ├── history_page.py      # Transcript & reading history log
    │   └── settings_page.py     # Voice, audio & visual accessibility preferences
    └── widgets/
        └── mic_button.py        # Custom animated Qt microphone button widget
```

---

## Getting Started

1. **Create a Virtual Environment & Install Dependencies**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Run the Application**:
   ```bash
   python main.py
   ```
