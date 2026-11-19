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
with patch.object(threading.Thread, 'start'), patch('platform.system', return_value='Windows'):
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
    def run_regression(self, scenario):
        with isolated_project() as (root, env):
            env['QT_SCALE_FACTOR'] = '1'
            result = subprocess.run([sys.executable, '-c', REGRESSION_SETUP + scenario],
                                    cwd=root, env=env, capture_output=True, text=True,
                                    encoding='utf-8', timeout=60,
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            self.assertEqual(result.returncode, 0, result.stdout + '\n' + result.stderr)
            output = os.environ.get('JARVIS_LANGUAGE_RENDER_DIR')
            if output:
                folder = Path(output)
                folder.mkdir(parents=True, exist_ok=True)
                for path in root.glob('rev2-*.png'):
                    shutil.copyfile(path, folder / path.name)

    def test_dismissed_content_stays_dismissed_for_all_payloads(self):
        self.run_regression(r'''
for kind in ('plain', 'code', 'review'):
    i18n.set_language('en')
    show_payload(kind)
    win._content_panel.hide()
    app.processEvents()
    before = win._center_split.sizes()
    with patch.object(win.hud, 'glance') as glance, patch.object(win, '_reveal_below_hud', wraps=win._reveal_below_hud) as reveal:
        for language in ('pt-BR', 'en'):
            win._apply_ui_language(language)
            app.processEvents()
            assert win._content_panel.isHidden(), (kind, language, 'dismissed panel reopened')
            assert win._center_split.sizes() == before, (kind, language, 'splitter moved')
        glance.assert_not_called()
        reveal.assert_not_called()
    # A genuinely new result must still open the panel normally.
    show_payload(kind)
    app.processEvents()
    assert not win._content_panel.isHidden()
    assert win._center_split.sizes()[1] > 0
assert not violations, violations
print('DISMISSED_CONTENT_PRESERVED_ALL_PAYLOADS')
''')

    def test_active_quiz_keeps_space_question_and_typed_answer(self):
        self.run_regression(r'''
from copy import deepcopy
from gui.i18n import QLineEdit
for kind in ('plain', 'code', 'review'):
    i18n.set_language('en')
    show_payload(kind)
    grader = Mock(return_value=True)
    win._show_quiz('CLOSE', [
        {'question': 'first CLOSE', 'options': [], 'answer': 'CLOSE'},
        {'question': 'second FOLDER', 'options': [], 'answer': 'FOLDER'}], grader)
    win._quiz_submit('CLOSE')
    win._quiz_next()
    row = win._quiz_answers_lay.itemAt(0).widget()
    field = row.findChild(QLineEdit)
    field.setText(sentinel)
    app.processEvents()
    before = win._center_split.sizes()
    before_hidden = (win._content_panel.isHidden(), win._quiz_panel.isHidden())
    before_quiz = deepcopy({k: v for k, v in win._quiz.items() if k != 'grader'})
    assert before[1] == 0 and before[2] > 0
    assert before_quiz['i'] == 1 and len(before_quiz['results']) == 1
    grader.reset_mock()
    command, voice = Mock(), Mock()
    win.on_text_command, win.on_voice_change = command, voice
    with patch.object(win.hud, 'glance') as glance, patch.object(win, '_reveal_below_hud', wraps=win._reveal_below_hud) as reveal:
        for language in ('pt-BR', 'en'):
            win._apply_ui_language(language)
            app.processEvents()
            assert win._center_split.sizes() == before, (kind, language, 'quiz lost its space')
            assert (win._content_panel.isHidden(), win._quiz_panel.isHidden()) == before_hidden
            assert {k: v for k, v in win._quiz.items() if k != 'grader'} == before_quiz
            assert row.findChild(QLineEdit) is field and field.text() == sentinel
            assert win._quiz_q_lbl.text() == 'second FOLDER'
            if kind == 'plain':
                assert sentinel in win._content_display.toPlainText()
            elif kind == 'code':
                assert ('PEDIDO' if language == 'pt-BR' else 'REQUEST') in win._content_display.toPlainText()
            else:
                assert ('O documento não esclarece:' if language == 'pt-BR' else 'The document does not settle:') in win._content_display.toPlainText()
            from PyQt6.QtTest import QTest
            QTest.qWait(50)
            win.repaint()
            app.processEvents()
            assert win.grab().save(str(root / ('rev2-quiz-' + kind + '-' + language + '.png')))
        glance.assert_not_called()
        reveal.assert_not_called()
    grader.assert_not_called(); command.assert_not_called(); voice.assert_not_called()
    win._hide_quiz()
assert not violations, violations
print('QUIZ_STATE_AND_SPLITTER_PRESERVED_ALL_PAYLOADS')
''')

    def test_visible_content_keeps_selection_and_scroll_while_retranslating(self):
        self.run_regression(r'''
for kind in ('plain', 'code', 'review'):
    i18n.set_language('en')
    show_payload(kind)
    app.processEvents()
    display = win._content_display
    plain = display.toPlainText()
    start = plain.index(sentinel)
    cursor = display.textCursor()
    # Model a real selection using Qt's UTF-16 offsets, including the emoji.
    position = len(plain[:start].encode('utf-16-le')) // 2
    cursor.setPosition(position)
    cursor.setPosition(position + len(sentinel.encode('utf-16-le')) // 2, cursor.MoveMode.KeepAnchor)
    display.setTextCursor(cursor)
    bar = display.verticalScrollBar()
    assert bar.maximum() > 25, (kind, 'fixture must exercise real scrolling')
    bar.setValue(25)
    before_scroll, before_sizes = bar.value(), win._center_split.sizes()
    with patch.object(win.hud, 'glance') as glance, patch.object(win, '_reveal_below_hud', wraps=win._reveal_below_hud) as reveal:
        for language in ('pt-BR', 'en'):
            win._apply_ui_language(language)
            app.processEvents()
            assert not win._content_panel.isHidden()
            assert win._center_split.sizes() == before_sizes
            assert display.textCursor().selectedText() == sentinel, (kind, language, display.textCursor().selectedText())
            assert bar.value() == before_scroll, (kind, language, 'scroll changed')
            if kind == 'code':
                assert ('PEDIDO' if language == 'pt-BR' else 'REQUEST') in display.toPlainText()
            if kind == 'review':
                assert ('O documento não esclarece:' if language == 'pt-BR' else 'The document does not settle:') in display.toPlainText()
        glance.assert_not_called()
        reveal.assert_not_called()
assert not violations, violations
print('VISIBLE_CONTENT_RETRANSLATED_SELECTION_AND_SCROLL_PRESERVED')
''')

    def test_loaded_file_and_folder_paint_localizes_only_own_labels(self):
        self.run_regression(r'''
from types import SimpleNamespace
from gui.widgets import _DropCanvas, FileDropZone
class CapturePainter:
    def __init__(self): self.texts = []
    def setFont(self, *args): pass
    def setPen(self, *args): pass
    def drawText(self, *args): self.texts.append(str(args[-1]))
    def drawLine(self, *args): pass
    def fontMetrics(self): return self
    def elidedText(self, text, *args): return text
folder = root / 'FOLDER'
folder.mkdir()
no_extension, with_extension = root / 'FILE', root / 'CLOSE.CLOSE'
no_extension.write_text('synthetic', encoding='utf-8')
with_extension.write_text('synthetic', encoding='utf-8')
loaded = FileDropZone(win)
loaded.resize(500, 46)
loaded._current_file, loaded._folder_files = str(folder), 5000
loaded.show()
for language in ('en', 'pt-BR', 'en'):
    with patch('gui.widgets._count_files', side_effect=AssertionError('unexpected reload')):
        i18n.set_language(language)
        app.processEvents()
    for count in (0, 1, 2, 5000):
        painter = CapturePainter()
        zone = SimpleNamespace(_current_file=str(folder), _folder_files=count)
        _DropCanvas._paint_file(SimpleNamespace(_z=zone), painter, 500, 60)
        noun = ('file' if count == 1 else 'files') if language == 'en' else ('arquivo' if count == 1 else 'arquivos')
        expected = ('FOLDER' if language == 'en' else 'PASTA') + '  ·  ' + str(count) + ('+' if count >= 5000 else '') + ' ' + noun
        assert painter.texts[1] == 'FOLDER'
        assert painter.texts[2] == expected, (language, count, painter.texts)
    for path, expected_label in ((no_extension, 'FILE' if language == 'en' else 'ARQUIVO'), (with_extension, 'CLOSE')):
        painter = CapturePainter()
        _DropCanvas._paint_file(SimpleNamespace(_z=SimpleNamespace(_current_file=str(path))), painter, 500, 60)
        assert painter.texts[1] == path.name
        assert painter.texts[2].startswith(expected_label + '  ·  '), (language, path.name, painter.texts)
    # Repaint a real loaded widget; the language switch must not enumerate/reload it.
    with patch('gui.widgets._count_files', side_effect=AssertionError('unexpected reload')):
        app.processEvents()
        assert loaded.grab().save(str(root / ('rev2-folder-' + language + '.png')))
        assert loaded.current_file() == str(folder) and loaded._folder_files == 5000
        loaded._current_file = str(no_extension)
        assert loaded.grab().save(str(root / ('rev2-file-' + language + '.png')))
        loaded._current_file = str(folder)
loaded.hide()
assert not violations, violations
print('LOADED_LABELS_COUNTS_AND_OPAQUE_NAMES_OK')
''')

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


REGRESSION_SETUP = r'''
from pathlib import Path
from unittest.mock import Mock, patch
import threading
from providers._tests import install_child_guard
root = Path.cwd()
violations = install_child_guard(root)
with patch.object(threading.Thread, 'start'), patch('platform.system', return_value='Windows'):
    import ui
from memory import config_manager as config
config.update_config(local_only=True, os_system='windows', ui_language='en')
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
from gui import i18n
app = QApplication.instance() or QApplication([])
font = Path(__import__('os').environ['WINDIR']) / 'Fonts' / 'segoeui.ttf'
assert QFontDatabase.addApplicationFont(str(font)) >= 0
patch.object(QTimer, 'start').start()
patch.object(ui.MainWindow, '_update_metrics').start()
patch.object(ui.MainWindow, '_on_clipboard_changed').start()
player = ui.JarvisUI(str(root / 'missing-face.png'))
win = player._win
win.resize(1280, 900)
win.show()
app.processEvents()
sentinel = 'KEEP 📁 CLOSE FOLDER coração'
body = '\n'.join('synthetic line ' + str(i) for i in range(80)) + '\n' + sentinel
def show_payload(kind):
    if kind == 'plain':
        win._show_content('CLOSE', body)
    elif kind == 'code':
        win._show_code_job({'request': body, 'status': 'reading', 'folder': 'CLOSE',
                            'model': 'FOLDER', 'started': 1, 'finished': 2,
                            'steps': [(i, 'synthetic step') for i in range(4)]})
    else:
        win._show_review('CLOSE', '', [], [body])
'''


if __name__ == '__main__':
    unittest.main()
