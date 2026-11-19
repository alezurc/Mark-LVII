from pathlib import Path
import ast
root=Path('.')
def edit(name,fn):
 p=root/name;raw=p.read_bytes();s=raw.decode('utf-8').replace('\r\n','\n')
 updated=fn(s);assert updated!=s,('no edit',name);ast.parse(updated)
 p.write_bytes(updated.replace('\n','\r\n').encode('utf-8') if b'\r\n' in raw else updated.encode('utf-8'))

def window(s):
 s=s.replace('        anchor, position = cursor.anchor(), cursor.position()\n        mode, args = payload', '        anchor, position = cursor.anchor(), cursor.position()\n        old_text = display.toPlainText()\n        mode, args = payload')
 s=s.replace('            self._show_content(*args)','            self._show_content(*args, present=False)')
 s=s.replace('            self._show_review(*args)','            self._show_review(*args, present=False)')
 s=s.replace('            self._show_code_job(*args)','            self._show_code_job(*args, present=False)')
 old='''        cursor = display.textCursor()
        cursor.setPosition(min(anchor, display.document().characterCount() - 1))
        cursor.setPosition(min(position, display.document().characterCount() - 1), cursor.MoveMode.KeepAnchor)'''
 new='''        new_text = display.toPlainText()
        # Cursor offsets use UTF-16 units in Qt. Map unchanged text across the
        # translated labels instead of selecting the old numeric offsets.
        from difflib import SequenceMatcher
        changes = SequenceMatcher(None, old_text, new_text).get_opcodes()

        def relocated(qt_position):
            before = old_text.encode("utf-16-le")[:qt_position * 2]
            old_position = len(before.decode("utf-16-le", errors="ignore"))
            new_position = len(new_text)
            for kind, a, b, c, d in changes:
                if a <= old_position < b:
                    new_position = c + min(old_position - a, d - c)
                    break
            return len(new_text[:new_position].encode("utf-16-le")) // 2

        cursor = display.textCursor()
        cursor.setPosition(relocated(anchor))
        cursor.setPosition(relocated(position), cursor.MoveMode.KeepAnchor)'''
 assert old in s;s=s.replace(old,new)
 bounds=[('    def _show_content(', '    # ── the coding agent'),('    def _show_code_job(', '    # ── document review'),('    def _show_review(', '    # ── quiz panel')]
 for start_marker,end_marker in bounds:
  a=s.index(start_marker);b=s.index(end_marker,a);segment=s[a:b]
  if start_marker.endswith('_show_content('):segment=segment.replace('def _show_content(self, title: str, text: str):','def _show_content(self, title: str, text: str, *, present: bool = True):')
  elif start_marker.endswith('_show_code_job('):segment=segment.replace('def _show_code_job(self, job: dict):','def _show_code_job(self, job: dict, *, present: bool = True):')
  else:segment=segment.replace('def _show_review(self, title: str, summary: str, findings, unclear):','def _show_review(self, title: str, summary: str, findings, unclear, *, present: bool = True):')
  segment=segment.replace('        self._content_ts_lbl.setText(_time.strftime("%H:%M:%S"))','        if present:\n            self._content_ts_lbl.setText(_time.strftime("%H:%M:%S"))')
  segment=segment.replace('        self._reveal_below_hud(self._content_panel, 220)','        if present:\n            self._reveal_below_hud(self._content_panel, 220)')
  segment=segment.replace('        self._reveal_below_hud(self._content_panel, 260)','        if present:\n            self._reveal_below_hud(self._content_panel, 260)')
  if start_marker.endswith('_show_code_job('):
   segment=segment.replace('keep = 0 if first else bar.value()','keep = 0 if first and present else bar.value()')
   segment=segment.replace('        if first:\n            self.hud.glance','        if first and present:\n            self.hud.glance')
  else:
   segment=segment.replace('        self.hud.glance(0.0, -0.85, hold=1.3)','        if present:\n            self.hud.glance(0.0, -0.85, hold=1.3)')
   segment=segment.replace('''        self._content_display.moveCursor(
            self._content_display.textCursor().MoveOperation.Start
        )''','''        if present:
            self._content_display.moveCursor(
                self._content_display.textCursor().MoveOperation.Start)''')
   segment=segment.replace('''        self._content_display.moveCursor(
            self._content_display.textCursor().MoveOperation.Start)''','''        if present:
            self._content_display.moveCursor(
                self._content_display.textCursor().MoveOperation.Start)''')
  s=s[:a]+segment+s[b:]
 return s
edit('gui/window.py',window)
def widgets(s):
 s=s.replace('ext_str = path.suffix.upper().lstrip(".") or "FILE"','ext_str = path.suffix.upper().lstrip(".") or tr("FILE")')
 s=s.replace('            ext_str, size_str = "FOLDER", f"{n}{\'+\' if n >= 5000 else \'\'} files"','''            ext_str = tr("FOLDER")
            size_str = tr("{count}{limit} file" if n == 1 else "{count}{limit} files",
                          count=n, limit="+" if n >= 5000 else "")''')
 s=s.replace('render(f"{ext_str}  ·  {size_str}")','render(tr("{label}  ·  {size}", label=ext_str, size=size_str))')
 return s
edit('gui/widgets.py',widgets)
edit('gui/i18n.py',lambda s:s.replace('PT_BR = {', '''PT_BR = {'FILE': 'ARQUIVO', 'FOLDER': 'PASTA',
 '{count}{limit} file': '{count}{limit} arquivo',
 '{count}{limit} files': '{count}{limit} arquivos',
 '''))
print('Applied R004-001 and R004-002 corrections in 3 approved sources')