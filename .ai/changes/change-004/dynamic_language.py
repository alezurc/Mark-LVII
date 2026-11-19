from pathlib import Path
import ast,pprint
p=Path('gui/i18n.py');s=p.read_text(encoding='utf-8');tree=ast.parse(s);n=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PT_BR' for t in n.targets));d=ast.literal_eval(n.value)
d.update({'MICROPHONE — what JARVIS hears you with':'MICROFONE — como JARVIS ouve você','SPEAKERS — what JARVIS talks through':'ALTO-FALANTES — por onde JARVIS fala','System default':'Padrão do sistema','TRANSLATE':'TRADUZIR','SUMMARISE':'RESUMIR','EXPLAIN':'EXPLICAR','FIX':'CORRIGIR','F4 MUTE   ·   F11 FULLSCREEN   ·   ESC INTERRUPT   ·   BY FATIHMAKES':'F4 SILENCIAR   ·   F11 TELA CHEIA   ·   ESC INTERROMPER   ·   POR FATIHMAKES','Same as background requests':'Igual às solicitações em segundo plano','Same as conversation':'Igual à conversa','None':'Nenhum','REQUEST':'PEDIDO','FILES':'ARQUIVOS','STEPS — newest first':'ETAPAS — mais recentes primeiro','CODE AGENT':'AGENTE DE CÓDIGO','The document does not settle:':'O documento não esclarece:','READING':'LENDO','PLANNING':'PLANEJANDO','WRITING':'ESCREVENDO','CHECKING':'VERIFICANDO','TESTING':'TESTANDO','FIXING':'CORRIGINDO','WAITING':'AGUARDANDO','SKIPPED':'IGNORADO','BROKEN':'COM ERRO','new ':'novo ','enabled':'ativada','disabled':'desativada','When: {when}':'Quando: {when}','Next: {next}':'Próxima: {next}','Last: {last} — {result}':'Última: {last} — {result}','Says':'Diz','Carries out':'Executa','Background task':'Tarefa em segundo plano','on':'ligada','off':'desligada',' · held back in quiet hours':' · suspensa no horário silencioso','State: {state}{quiet} · ran {runs} times':'Estado: {state}{quiet} · executada {runs} vezes','Change it by voice — "move the briefing to 08:30", "turn the check-in off", "remind me every Friday at 17:00".':'Altere por voz — "mude o resumo para 08:30", "desative o check-in", "lembre-me toda sexta às 17:00".','ROUTINE':'ROTINA','next {time} · {description}':'próxima {time} · {description}','✓  {count} found.':'✓  {count} encontrados.','✓  {count} available: {items}':'✓  {count} disponíveis: {items}','✓  {count} available — pick one above.':'✓  {count} disponíveis — escolha acima.','installing {package} — this can take a minute…':'instalando {package} — pode levar um minuto…','✓  installed — close and reopen this panel':'✓  instalado — feche e reabra este painel','pip failed':'falha no pip','{name}  (not connected)':'{name}  (desconectado)'})
lines=s.splitlines(keepends=True);a=sum(map(len,lines[:n.lineno-1]));b=sum(map(len,lines[:n.end_lineno]));s=s[:a]+'PT_BR = '+pprint.pformat(d,sort_dicts=True,width=100)+'\n'+s[b:];p.write_text(s,encoding='utf-8',newline='\n')

def edit(name,fn):
 p=Path(name);s=p.read_bytes().decode('utf-8').replace('\r\n','\n');s=fn(s);ast.parse(s);p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))

def window(s):
 s=s.replace('tr, render, QLabel','tr, render, watch_language, join_messages, QLabel')
 s=s.replace('        self._face_path = face_path','        self._face_path = face_path\n        self._localized_content = None\n        watch_language(self._refresh_language_content)')
 s=s.replace('    def _show_content(self, title: str, text: str):', '''    def _refresh_language_content(self):
        self._tick_clock()
        payload = self._localized_content
        if not payload:
            return
        display = self._content_display
        bar = display.verticalScrollBar()
        scroll = bar.value()
        cursor = display.textCursor()
        anchor, position = cursor.anchor(), cursor.position()
        mode, args = payload
        if mode == "plain":
            self._show_content(*args)
        elif mode == "review":
            self._show_review(*args)
        else:
            self._show_code_job(*args)
        cursor = display.textCursor()
        cursor.setPosition(min(anchor, display.document().characterCount() - 1))
        cursor.setPosition(min(position, display.document().characterCount() - 1), cursor.MoveMode.KeepAnchor)
        display.setTextCursor(cursor)
        bar.setValue(scroll)

    def _show_content(self, title: str, text: str):''')
 s=s.replace('        # The panel opens below the head,', '        self._localized_content = ("plain", (title, text))\n        # The panel opens below the head,')
 s=s.replace('label, dash, rest = str(title or "").partition','label, dash, rest = str(render(title) or "").partition')
 s=s.replace('self._content_display.setPlainText(text)','self._content_display.setPlainText(render(text))')
 s=s.replace('        e = self._esc\n        col = lambda', '        self._localized_content = ("code", (job,))\n        e = self._esc\n        col = lambda')
 s=s.replace('    def _show_review(self, title: str, summary: str, findings, unclear):\n', '    def _show_review(self, title: str, summary: str, findings, unclear):\n        self._localized_content = ("review", (title, summary, findings, unclear))\n')
 s=s.replace('{ph.upper()}', '{e(render(tr(ph.upper())))}').replace('{e(status.upper())}', '{e(render(tr(status.upper())))}')
 s=s.replace('f\'REQUEST&nbsp;</span>', 'f\'{e(render(tr("REQUEST")))}&nbsp;</span>')
 s=s.replace('>FILES</div>\')','>{e(render(tr("FILES")))}</div>\')')
 s=s.replace('f\'STEPS — newest first</div>\'', 'f\'{e(render(tr("STEPS — newest first")))}</div>\'')
 s=s.replace('verb = "new " if','verb = render(tr("new ")) if')
 s=s.replace('f"CODE AGENT — {job.get', 'f"{render(tr(\'CODE AGENT\'))} — {job.get')
 s=s.replace("'The document does not settle:</div>'", "f'{e(render(tr(\"The document does not settle:\")))}</div>'")
 s=s.replace('            "F4 MUTE   ·   F11 FULLSCREEN   ·   ESC INTERRUPT   ·   BY FATIHMAKES")', '            tr("F4 MUTE   ·   F11 FULLSCREEN   ·   ESC INTERRUPT   ·   BY FATIHMAKES"))')
 s=s.replace("'enabled' if enabled else 'disabled'", "tr('enabled') if enabled else tr('disabled')")
 s=s.replace('text = f"next {_time.strftime(\'%a %H:%M\', _time.localtime(r[\'next_ts\']))} · {text}"', 'text = tr("next {time} · {description}", time=_time.strftime("%a %H:%M", _time.localtime(r["next_ts"])), description=text)')
 s=s.replace('lines = [r["name"], "", f"When: {eng.describe(r)}"]','lines = [r["name"], "", tr("When: {when}", when=eng.describe(r))]')
 s=s.replace('lines.append(f"Next: {stamp(r[\'next_ts\'])}")','lines.append(tr("Next: {next}", next=stamp(r["next_ts"])))')
 s=s.replace('lines.append(f"{what}: {r[\'text\']}")','lines.append(tr("{what}: {text}", what=tr(what), text=r["text"]))')
 s=s.replace('lines.append(f"State: {state}{\' · held back in quiet hours\' if r.get(\'quiet\') else \'\'}"\n                     f" · ran {int(r.get(\'runs\') or 0)} times")', 'lines.append(tr("State: {state}{quiet} · ran {runs} times", state=tr(state), quiet=tr(" · held back in quiet hours") if r.get("quiet") else "", runs=int(r.get("runs") or 0)))')
 s=s.replace('lines.append(f"Last: {stamp(r[\'last_run\'])} — {r.get(\'last_result\') or \'\'}")','lines.append(tr("Last: {last} — {result}", last=stamp(r["last_run"]), result=r.get("last_result") or ""))')
 s=s.replace('lines += ["", "Change it by voice — \\"move the briefing to 08:30\\", "\n                      "\\"turn the check-in off\\", \\"remind me every Friday at 17:00\\"."]','lines += ["", tr(\'Change it by voice — "move the briefing to 08:30", "turn the check-in off", "remind me every Friday at 17:00".\')]')
 s=s.replace('self._show_content("ROUTINE", "\\n".join(lines)[:4000])','self._show_content(tr("ROUTINE"), join_messages("\\n", lines))')
 return s
edit('gui/window.py',window)
edit('gui/overlays.py',lambda s:s.replace('_row("MICROPHONE — what JARVIS hears you with",','_row(tr("MICROPHONE — what JARVIS hears you with"),').replace('_row("SPEAKERS — what JARVIS talks through",','_row(tr("SPEAKERS — what JARVIS talks through"),').replace('box.addItem(DEFAULT_LABEL,','box.addItem(tr(DEFAULT_LABEL),').replace('btn = QPushButton(label)\n            btn.setFont(hud_font(8))','btn = QPushButton(tr(label))\n            btn.setFont(hud_font(8))'))
edit('gui/providers_panel.py',lambda s:s.replace('("Same as background requests", "")','(tr("Same as background requests"), "")').replace('f"✓  {len(items)} found."','tr("✓  {count} found.", count=len(items))').replace('f"✓  {len(items)} available — pick one above."','tr("✓  {count} available — pick one above.", count=len(items))').replace('f"installing {pkg} — this can take a minute…"','tr("installing {package} — this can take a minute…", package=pkg)').replace('"✓  installed — close and reopen this panel"','tr("✓  installed — close and reopen this panel")').replace('else "pip failed"','else tr("pip failed")'))
print('Dynamic surfaces updated')