from pathlib import Path
import ast,pprint

def edit(name,fn):
 p=Path(name);s=p.read_bytes().decode('utf-8').replace('\r\n','\n');s=fn(s);ast.parse(s);p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
edit('gui/widgets.py',lambda s:s.replace('self._kind, self._label, self._colour = kind, str(text or ""), colour','self._kind, self._label, self._colour = kind, text or "", colour').replace('elidedText(render(self._state),','elidedText(render(tr(self._state)),').replace('self.setFixedSize(196, 34)','self.setFixedSize(220, 34)'))
edit('gui/window.py',lambda s:s.replace('RingGauge("MEMORY")','RingGauge(tr("MEMORY"))').replace('RingGauge("TEMP")','RingGauge(tr("TEMP"))').replace('38, "MIC ACTIVE",','38, tr("MIC ACTIVE"),').replace('38, "INTERRUPT",','38, tr("INTERRUPT"),').replace('set_look("mic_off", "MIC MUTED",','set_look("mic_off", tr("MIC MUTED"),').replace('set_look("mic", "MIC ACTIVE",','set_look("mic", tr("MIC ACTIVE"),').replace('self._date_lbl.setText(time.strftime("%a %d %b %Y"))','''from PyQt6.QtCore import QDateTime, QLocale
        from gui.i18n import get_language
        locale = QLocale("pt_BR" if get_language() == "pt-BR" else "en_US")
        self._date_lbl.setText(locale.toString(QDateTime.currentDateTime(), "ddd dd MMM yyyy"))'''))
edit('gui/hud.py',lambda s:s.replace('tr, render, QLabel','tr, render, get_language, QLabel').replace('key = (W, H,','key = (get_language(), W, H,'))
edit('gui/overlays.py',lambda s:s.replace('        self._language_combo.setFont(hud_font(10))','''        self._language_combo.setFont(hud_font(10))
        self._language_combo.setMinimumHeight(32)
        self._language_combo.setStyleSheet(
            f"QComboBox {{ color: {C.TEXT}; background: {C.PANEL2}; "
            f"border: 1px solid {C.BORDER}; padding: 4px 8px; border-radius: 3px; }}"
            f"QComboBox QAbstractItemView {{ color: {C.TEXT}; background: {C.PANEL2}; "
            f"selection-background-color: {C.PRI_DIM}; }}")'''))
p=Path('gui/i18n.py');s=p.read_text(encoding='utf-8');tree=ast.parse(s);n=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PT_BR' for t in n.targets));d=ast.literal_eval(n.value)
d.update({'Try Gemini first  —  faster':'Tentar Gemini primeiro  —  mais rápido','Try the other one first  —  keeps more on your machine':'Tentar o outro primeiro  —  mantém mais dados no computador','MEMORY':'MEMÓRIA','TEMP':'TEMP.','MIC ACTIVE':'MIC ATIVO','MIC MUTED':'MIC SILENCIADO','INTERRUPT':'INTERROMPER'})
lines=s.splitlines(keepends=True);a=sum(map(len,lines[:n.lineno-1]));b=sum(map(len,lines[:n.end_lineno]));s=s[:a]+'PT_BR = '+pprint.pformat(d,sort_dicts=True,width=100)+'\n'+s[b:];p.write_text(s,encoding='utf-8',newline='\n')
print('State, cache, date, selector contrast corrected')