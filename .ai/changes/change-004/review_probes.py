from pathlib import Path
import ast,os,subprocess,sys,json
sys.path.insert(0, str(Path.cwd()))
from providers._tests import isolated_project
folder=Path('.ai/changes/change-004')
tree=ast.parse(Path('tests/test_ui_language_qt.py').read_text(encoding='utf-8'))
child=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CHILD' for t in n.targets))
probe=r'''
    win._content_panel.hide()
    hidden_before = win._content_panel.isHidden()
    i18n.set_language('pt-BR')
    hidden_after = win._content_panel.isHidden()
    print('DISMISSED_PANEL', hidden_before, hidden_after)
    assert hidden_before is True and hidden_after is False
    win._show_quiz('synthetic quiz', [{'question':'CLOSE','options':['CLOSE'],'answer':'CLOSE'}], None)
    app.processEvents()
    before_sizes = win._center_split.sizes()
    quiz_before = win._content_panel.isHidden()
    i18n.set_language('en')
    app.processEvents()
    after_sizes = win._center_split.sizes()
    quiz_after = win._content_panel.isHidden()
    print('QUIZ_CONTENT_PANEL', quiz_before, quiz_after, 'SPLITTER', before_sizes, after_sizes)
    assert before_sizes[1] == 0 and before_sizes[2] > 0 and after_sizes[1] > 0 and after_sizes[2] == 0
    win._hide_quiz()
    from types import SimpleNamespace
    from gui.widgets import _DropCanvas
    class Painter:
        def __init__(self): self.texts=[]
        def setFont(self,*args): pass
        def setPen(self,*args): pass
        def drawText(self,*args): self.texts.append(str(args[-1]))
        def drawLine(self,*args): pass
        def fontMetrics(self): return self
        def elidedText(self,text,*args): return text
    data = root/'CLOSE'
    data.mkdir(exist_ok=True)
    painter=Painter()
    i18n.set_language('pt-BR')
    _DropCanvas._paint_file(SimpleNamespace(_z=SimpleNamespace(_current_file=str(data),_folder_files=3)), painter, 500, 60)
    print('FOLDER_TEXT_PT_BR',repr(painter.texts))
    assert 'FOLDER  ·  3 files' in painter.texts
    i18n.set_language('en')
'''
child=child.replace('    # Existing native wrappers, new panels and painted states.', probe+'\n    # Existing native wrappers, new panels and painted states.')
with isolated_project() as (root,env):
 env['QT_SCALE_FACTOR']='1'
 result=subprocess.run([sys.executable,'-c',child],cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',timeout=60,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
 (folder/'REVIEW-PROBES.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
 print(result.stdout);print(result.stderr);print('PROBE_EXIT',result.returncode)
 sys.exit(result.returncode)