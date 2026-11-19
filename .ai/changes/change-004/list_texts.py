import ast, json, pathlib
root=pathlib.Path('.')
names=['window','overlays','providers_panel','widgets','hud']
sinks={'QLabel':[0],'QPushButton':[0],'setText':[0],'setToolTip':[0],'setPlaceholderText':[0],'_lbl':[0],'_label':[0],'_btn':[0],'HoloPanel':[0,1],'DataRow':[0],'addItem':[0],'append_log':[0],'_quiz_btn':[0],'_mode_card':[0,1],'drawText':[-1],'elidedText':[0],'set_title':[0],'set_code':[0],'addAction':[0]}
rows=[]
for name in names:
 src=(root/'gui'/f'{name}.py').read_text(encoding='utf-8')
 tree=ast.parse(src)
 found=[]
 def visit(expr):
  if isinstance(expr,ast.Constant) and isinstance(expr.value,str) and any(c.isalpha() for c in expr.value):
   found.append((expr.lineno,expr.value))
  elif isinstance(expr,ast.JoinedStr):
   found.append((expr.lineno,ast.unparse(expr)))
  elif isinstance(expr,ast.IfExp):visit(expr.body);visit(expr.orelse)
  elif isinstance(expr,ast.BinOp) and isinstance(expr.op,ast.Add):visit(expr.left);visit(expr.right)
 for node in ast.walk(tree):
  if isinstance(node,ast.Call):
   key=getattr(node.func,'id',None) or getattr(node.func,'attr',None)
   for ix in sinks.get(key,[]):
    if node.args and -len(node.args)<=ix<len(node.args):visit(node.args[ix])
 rows.extend((name,line,val) for line,val in sorted(set(found)))
print(json.dumps(rows,ensure_ascii=False,indent=1))