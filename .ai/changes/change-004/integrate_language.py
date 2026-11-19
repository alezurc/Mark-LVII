from pathlib import Path
import ast
root=Path('.')
def edit(name,fn):
 p=root/name;raw=p.read_bytes();s=raw.decode('utf-8').replace('\r\n','\n')
 backup=root/'.ai/changes/change-004/develop-before'/name.replace('/','_')
 if not backup.exists():backup.write_bytes(raw)
 s=fn(s);ast.parse(s);p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))

def cfg(s):
 return s+'''

# Interface language is independent from the speech/model language.
def get_ui_language() -> str:
    value = load_api_keys().get("ui_language", "en")
    return value if isinstance(value, str) and value in ("en", "pt-BR") else "en"


@_locked
def save_ui_language(language: str) -> None:
    value = language if isinstance(language, str) and language in ("en", "pt-BR") else "en"
    data = _read_for_write()
    data["ui_language"] = value
    _write_config(data)
'''
edit('memory/config_manager.py',cfg)
edit('ui.py',lambda s:s.replace('        self._win = MainWindow(face_path)', '''        from memory.config_manager import get_ui_language
        from gui.i18n import set_language
        set_language(get_ui_language())
        self._win = MainWindow(face_path)'''))

def overlay(s):
 start=s.index('class CustomizeOverlay(');end=s.index('\nclass PluginManagerOverlay(',start)
 c=s[start:end]
 c=c.replace('_OW, _OH = 400, 588','_OW, _OH = 480, 660')
 c=c.replace('        lay = QVBoxLayout(self)', '''        from gui.i18n import LANGUAGES, get_language
        self.on_language_save = None
        self._initial_fields = (assistant_name, user_name, ui_color, voice or "Charon")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        body = QWidget()
        scroll.setWidget(body)
        outer.addWidget(scroll, 1)
        lay = QVBoxLayout(body)''')
 c=c.replace('        # ── Assistant voice', '''        lay.addWidget(_lbl(tr("INTERFACE LANGUAGE"), 8, color=C.TEXT_DIM,
                            align=Qt.AlignmentFlag.AlignLeft))
        self._language_combo = QComboBox()
        self._language_combo.setFont(hud_font(10))
        for code, label in LANGUAGES:
            self._language_combo.addItem(label, code)
        self._language_combo.setCurrentIndex(
            self._language_combo.findData(get_language()))
        lay.addWidget(self._language_combo)
        self._language_error = QLabel()
        self._language_error.setWordWrap(True)
        self._language_error.setFont(hud_font(9))
        self._language_error.setStyleSheet(f"color: {C.RED}; background: transparent;")
        self._language_error.hide()
        lay.addWidget(self._language_error)

        # ── Assistant voice''')
 c=c.replace('        lay.addLayout(btn_row)','        outer.addLayout(btn_row)')
 c=c.replace('        self.saved.emit(name, user, self._sel_color or DEFAULT_UI_COLOR, self._sel_voice)', '''        from gui.i18n import get_language
        language = self._language_combo.currentData()
        if language != get_language():
            try:
                if self.on_language_save is None:
                    raise RuntimeError("Language save handler unavailable")
                self.on_language_save(language)
            except Exception as exc:
                self._language_error.setText(tr("Could not save interface language: {error}", error=str(exc)))
                self._language_error.show()
                return
        fields = (name, user, self._sel_color or DEFAULT_UI_COLOR, self._sel_voice)
        if fields != self._initial_fields:
            self.saved.emit(*fields)''')
 return s[:start]+c+s[end:]
edit('gui/overlays.py',overlay)

def window(s):
 s=s.replace('        ov.saved.connect(self._apply_name_update)','        ov.saved.connect(self._apply_name_update)\n        ov.on_language_save = self._apply_ui_language')
 s=s.replace('    def _preview_ui_color(self, hex_color: str):', '''    def _apply_ui_language(self, language: str):
        from memory.config_manager import save_ui_language
        from gui.i18n import set_language
        # Persist first: a failed write leaves the active language unchanged.
        save_ui_language(language)
        set_language(language)

    def _preview_ui_color(self, hex_color: str):''')
 s=s.replace('mark, colour = "✓  correct", C.GREEN','mark, colour = tr("✓  correct"), C.GREEN')
 s=s.replace('mark, colour = "…  noted — I\'ll go over this one with you", C.ACC2','mark, colour = tr("…  noted — I\'ll go over this one with you"), C.ACC2')
 return s
edit('gui/window.py',window)

def widgets(s):
 s=s.replace('str(title or ""), str(code or "")','title or "", code or ""')
 s=s.replace('self._title = str(text or "")','self._title = text or ""')
 s=s.replace('self._code = str(text or "")','self._code = text or ""')
 # Rendering happens before measurement and elision, never after truncation.
 s=s.replace('elidedText(self._title,','elidedText(render(self._title),')
 s=s.replace('horizontalAdvance(self._code)','horizontalAdvance(render(self._code))')
 s=s.replace('elidedText(self._state,','elidedText(render(tr(self._state)),')
 s=s.replace('horizontalAdvance(self._key)','horizontalAdvance(render(self._key))')
 return s
edit('gui/widgets.py',widgets)
edit('gui/hud.py', lambda s:s.replace('        tw = p.fontMetrics().horizontalAdvance(txt)','        txt = render(tr(txt))\n        tw = p.fontMetrics().horizontalAdvance(txt)'))
print('Preference and selector integrated; AST valid')