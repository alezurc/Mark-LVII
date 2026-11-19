"""Qt behavior in a bounded child with source-only disposable project data."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

from providers._tests import isolated_project


CHILD = r'''
from pathlib import Path
from unittest.mock import patch, Mock
import threading
from providers._tests import install_child_guard
root = Path.cwd()
violations = install_child_guard(root)
with patch.object(threading.Thread, 'start'):
    import ui
from memory import config_manager as config
config.update_config(local_only=True, os_system='windows', assistant_name='JARVIS', ui_language='pt-BR')
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QLabel as NativeLabel
from gui import i18n
from gui.overlays import CustomizeOverlay, ConfirmBanner
# The fixture redirects USERPROFILE/LOCALAPPDATA; register an existing OS font
# explicitly so those disposable directories do not hide Windows' font cache.
from PyQt6.QtGui import QFontDatabase
font_file = Path(__import__('os').environ['WINDIR']) / 'Fonts' / 'segoeui.ttf'
app = QApplication.instance() or QApplication([])
assert QFontDatabase.addApplicationFont(str(font_file)) >= 0
with patch.object(QTimer, 'start'), patch.object(ui.MainWindow, '_update_metrics'), patch.object(ui.MainWindow, '_on_clipboard_changed'):
    player = ui.JarvisUI(str(root / 'missing-face.png'))
    win = player._win
    app = player._app
    win.resize(1280, 900)
    win.show()
    app.processEvents()
    assert i18n.get_language() == 'pt-BR'
    assert win._input.placeholderText() == 'Digite um comando ou pergunta…'
    sentinel = 'CLOSE / TASKS / usuário: coração'
    win._input.setText(sentinel)
    win._show_content('CLOSE', sentinel)
    voice_change = Mock()
    win.on_voice_change = voice_change
    win._open_customize()
    ov = win._customize_overlay
    ov._language_combo.setCurrentIndex(ov._language_combo.findData('en'))
    ov._cancel()
    assert config.get_ui_language() == 'pt-BR'
    assert i18n.get_language() == 'pt-BR'
    win._open_customize()
    ov = win._customize_overlay
    ov._language_combo.setCurrentIndex(ov._language_combo.findData('en'))
    ov._save()
    assert config.get_ui_language() == 'en'
    assert i18n.get_language() == 'en'
    assert win._input.placeholderText() == 'Type a command or question…'
    assert win._input.text() == sentinel
    assert win._content_display.toPlainText() == sentinel
    assert not voice_change.called
    win._open_customize()
    en_overlay = win._customize_overlay
    en_overlay.resize(480, 420)
    app.processEvents()
    assert en_overlay.grab().save(str(root / 'customize-en.png'))
    en_overlay._cancel()
    app.processEvents()
    assert win.grab().save(str(root / 'language-en.png'))
    # Existing native wrappers, new panels and painted states.
    raw = i18n.QLabel('CLOSE')
    bound = i18n.QLabel(i18n.tr('CLOSE'))
    combo = i18n.QComboBox()
    combo.addItem(i18n.tr('CLOSE'), 'stable-id')
    combo.setCurrentIndex(0)
    combo_changes = Mock()
    combo.currentIndexChanged.connect(combo_changes)
    win._apply_state('LISTENING')
    win._apply_ui_language('pt-BR')
    assert raw.text() == 'CLOSE' and bound.text() == 'FECHAR'
    assert combo.currentData() == 'stable-id' and combo.itemText(0) == 'FECHAR'
    assert not combo_changes.called
    editable = i18n.QComboBox()
    editable.setEditable(True)
    editable.addItem(i18n.tr('CLOSE'), 'stable')
    editable.setEditText(sentinel)
    assert win.hud.state == 'LISTENING'
    assert win._input.text() == sentinel and win._content_display.toPlainText() == sentinel
    assert not voice_change.called
    panel = ConfirmBanner('CLOSE', sentinel, parent=win.centralWidget())
    assert any(x.text() == '▸  CONFIRMAR' for x in panel.findChildren(i18n.QPushButton))
    assert any(x.text() == sentinel for x in panel.findChildren(NativeLabel))
    panel.hide()
    app.processEvents()
    assert win.grab().save(str(root / 'language-pt-BR.png'))
    win._open_customize()
    ov = win._customize_overlay
    ov.resize(480, 420)
    ov.show()
    app.processEvents()
    assert ov.grab().save(str(root / 'customize-pt-BR.png'))
    # Persistence failure keeps both active locale and overlay; no false success.
    ov._language_combo.setCurrentIndex(ov._language_combo.findData('en'))
    with patch.object(config, 'save_ui_language', side_effect=OSError('synthetic failure')):
        ov._save()
    assert not ov.isHidden()
    assert not ov._language_error.isHidden()
    assert i18n.get_language() == 'pt-BR' and config.get_ui_language() == 'pt-BR'
    ov._cancel()
    i18n.set_language('en')
    assert editable.currentText() == sentinel
    assert bound.text() == 'CLOSE'
    assert combo.itemText(0) == 'CLOSE'
    assert win._input.placeholderText() == 'Type a command or question…'
    # Rich text's own labels update; generated/user text is kept verbatim.
    win._show_code_job({'request': sentinel, 'status': 'reading', 'folder': 'CLOSE',
                        'model': 'TASKS', 'files': {'CLOSE.py': {'state': 'done', 'what': sentinel}},
                        'steps': [(0, sentinel)]})
    assert 'REQUEST' in win._content_display.toPlainText()
    i18n.set_language('pt-BR')
    assert 'PEDIDO' in win._content_display.toPlainText()
    assert 'ARQUIVOS' in win._content_display.toPlainText()
    assert sentinel in win._content_display.toPlainText()
    from gui.providers_panel import ProvidersOverlay
    with patch.object(threading.Thread, 'start'):
        providers = ProvidersOverlay(parent=win.centralWidget())
        providers._mode = 'pipeline'
        providers._rebuild_body()
    providers.adjustSize()
    providers.show()
    i18n.set_language('pt-BR')
    assert providers._first_combo.itemText(0) == 'Tentar Gemini primeiro  —  mais rápido'
    selected = providers._first_combo.currentData()
    app.processEvents()
    assert providers.grab().save(str(root / 'providers-pt-BR.png'))
    i18n.set_language('en')
    assert providers._first_combo.itemText(0) == 'Try Gemini first  —  faster'
    assert providers._first_combo.currentData() == selected
    app.processEvents()
    assert providers.grab().save(str(root / 'providers-en.png'))
    providers.hide()
    i18n.set_language('pt-BR')
    win._show_review('CLOSE', sentinel, [], [sentinel])
    assert 'O documento não esclarece:' in win._content_display.toPlainText()
    i18n.set_language('en')
    assert 'The document does not settle:' in win._content_display.toPlainText()
    assert sentinel in win._content_display.toPlainText()
    # A raw setter releases the old translation binding.
    bound.setText(sentinel)
    i18n.set_language('pt-BR')
    assert bound.text() == sentinel
    # Worker calls must fail before changing global locale or widgets.
    errors = []
    def worker():
        try: i18n.set_language('en')
        except RuntimeError as exc: errors.append(str(exc))
    thread = threading.Thread(target=worker)
    thread.start(); thread.join(3)
    assert not thread.is_alive() and errors
    assert i18n.get_language() == 'pt-BR'
    win.close()
    raw.deleteLater(); bound.deleteLater(); combo.deleteLater()
    app.processEvents()
assert not violations, violations
print('QT_LANGUAGE_BEHAVIOR_OK')
'''


class QtLanguageTests(unittest.TestCase):
    def test_window_switch_persistence_and_user_content(self):
        with isolated_project() as (root, env):
            env['QT_SCALE_FACTOR'] = '1'
            result = subprocess.run([sys.executable, '-c', CHILD], cwd=root, env=env,
                                    capture_output=True, text=True, encoding='utf-8', timeout=60,
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            self.assertEqual(result.returncode, 0, result.stdout + '\n' + result.stderr)
            self.assertIn('QT_LANGUAGE_BEHAVIOR_OK', result.stdout)
            output = os.environ.get('JARVIS_LANGUAGE_RENDER_DIR')
            if output:
                folder = Path(output)
                folder.mkdir(parents=True, exist_ok=True)
                for name in ('language-en.png', 'language-pt-BR.png', 'customize-pt-BR.png',
                             'customize-en.png', 'providers-en.png', 'providers-pt-BR.png'):
                    shutil.copyfile(root / name, folder / name)


if __name__ == '__main__':
    unittest.main()
