import ast,json,pathlib,re
ROOT=pathlib.Path('.')
FILES=['window','overlays','providers_panel','widgets','hud']
SINKS={'QLabel':[0],'QPushButton':[0],'setText':[0],'setToolTip':[0],'setPlaceholderText':[0],'_lbl':[0],'_label':[0],'_btn':[0],'HoloPanel':[0,1],'DataRow':[0],'append_log':[0],'_quiz_btn':[0],'_mode_card':[0,1],'drawText':[-1],'elidedText':[0],'set_title':[0],'set_code':[0],'addAction':[0]}
EXEMPT={'AIza…','pip install\nqrcode[pil]','☁  GEMINI LIVE'}
def message(node):
 if isinstance(node,ast.Constant) and isinstance(node.value,str):return node.value,[]
 if isinstance(node,ast.JoinedStr):
  template='';values=[]
  for x in node.values:
   if isinstance(x,ast.Constant):template+=x.value.replace('{','{{').replace('}','}}')
   else:
    key='v'+str(len(values)); spec=''
    if x.format_spec:
     if not all(isinstance(z,ast.Constant) for z in x.format_spec.values):return None
     spec=':'+''.join(z.value for z in x.format_spec.values)
    conv='!'+chr(x.conversion) if x.conversion!=-1 else ''
    template+='{'+key+conv+spec+'}';values.append((key,ast.unparse(x.value)))
  return template,values
 return None

def gather(node,out):
 msg=message(node)
 if msg:
  text,values=msg
  static=re.sub(r'\{[^}]*\}','',text)
  if text not in EXEMPT and re.search('[A-Za-z]',static) and not text.startswith(('You:', '<b>')):
   out.append((node,text,values))
 elif isinstance(node,ast.IfExp):gather(node.body,out);gather(node.orelse,out)
 elif isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):gather(node.left,out);gather(node.right,out)

all_messages=[]
for name in FILES:
 src=(ROOT/'gui'/f'{name}.py').read_text(encoding='utf-8');tree=ast.parse(src);out=[]
 for node in ast.walk(tree):
  if isinstance(node,ast.Call):
   key=getattr(node.func,'id',None) or getattr(node.func,'attr',None)
   for ix in SINKS.get(key,[]):
    if node.args and -len(node.args)<=ix<len(node.args):gather(node.args[ix],out)
 all_messages.extend(text for _,text,_ in out)
path=ROOT/'.ai/changes/change-004/messages.json'
path.write_text(json.dumps(sorted(set(all_messages)),ensure_ascii=False,indent=1),encoding='utf-8')
print(path.read_text(encoding='utf-8'))# Apply only explicit display expressions. Preserve original CRLF bytes elsewhere.
pairs={}
for line in (ROOT/'.ai/changes/change-004/translations.txt').read_text(encoding='utf-8').splitlines():
 if not line:continue
 key,value=line.split('|',1);pairs[key.replace('\\n','\n')]=value.replace('\\n','\n')
missing=set(all_messages)-pairs.keys()
assert not missing,missing
p=ROOT/'gui/i18n.py'
s=p.read_text(encoding='utf-8').replace('PT_BR = {}  # Populated below; English source messages are the stable keys.', 'PT_BR = '+repr(pairs))
p.write_text(s,encoding='utf-8',newline='\n')
snap=ROOT/'.ai/changes/change-004/develop-before';snap.mkdir(exist_ok=True)
for name in FILES:
 path=ROOT/'gui'/f'{name}.py';raw=path.read_bytes();src=raw.decode('utf-8').replace('\r\n','\n')
 (snap/f'{name}.py').write_bytes(raw)
 tree=ast.parse(src);out=[]
 for node in ast.walk(tree):
  if isinstance(node,ast.Call):
   key=getattr(node.func,'id',None) or getattr(node.func,'attr',None)
   for ix in SINKS.get(key,[]):
    if node.args and -len(node.args)<=ix<len(node.args):gather(node.args[ix],out)
   # Preserve tagged arguments through formatted composition (e.g. mode cards).
   if key=='setText' and node.args and isinstance(node.args[0],ast.JoinedStr):
    x=node.args[0];msg=message(x)
    if msg and not any(a is x for a,_,_ in out) and not msg[0].startswith(('You:', '<b>')):out.append((x,*msg))
 lines=src.splitlines(keepends=True);starts=[0]
 for line in lines:starts.append(starts[-1]+len(line))
 def offset(line,col):return starts[line-1]+len(lines[line-1].encode('utf-8')[:col].decode('utf-8'))
 replacements={}
 for node,text,values in out:
  args=''.join(', '+k+'='+v for k,v in values)
  replacement='tr('+repr(text)+args+')'
  replacements[(offset(node.lineno,node.col_offset),offset(node.end_lineno,node.end_col_offset))]=replacement
 # drawText/elidedText render only tagged values; raw user data passes through.
 for node in ast.walk(tree):
  if not isinstance(node,ast.Call):continue
  key=getattr(node.func,'attr',None)
  if key in ('drawText','elidedText') and node.args:
   x=node.args[-1] if key=='drawText' else node.args[0]
   a,b=offset(x.lineno,x.col_offset),offset(x.end_lineno,x.end_col_offset)
   if (a,b) in replacements:replacements[(a,b)]='render('+replacements[(a,b)]+')'
   elif not isinstance(x, ast.Call) and not any(a<=i and j<=b for i,j in replacements):replacements[(a,b)]='render('+src[a:b]+')'
 for (a,b),rep in sorted(replacements.items(),reverse=True):src=src[:a]+rep+src[b:]
 marker='from __future__ import annotations\n'
 # Qt aliases are imported after QtWidgets so they are not overwritten.
 marker2='from gui.style import '
 pos=src.index(marker2)
 src=src[:pos]+'from gui.i18n import tr, render, QLabel, QPushButton, QLineEdit, QComboBox\n\n'+src[pos:]
 path.write_bytes(src.replace('\n','\r\n').encode('utf-8'))
print('Localized',len(pairs),'messages in',len(FILES),'GUI modules')