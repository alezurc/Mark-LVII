from pathlib import Path
import ast,hashlib,json
root=Path('.');folder=root/'.ai/changes/change-004'
baseline=json.loads((folder/'ENCODING-BASELINE.json').read_text(encoding='utf-8'))
approved=json.loads((folder/'APPROVED-SCOPE.json').read_text(encoding='utf-8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((folder/'ENCODING-BASELINE.json').read_bytes())==approved['encoding_sha256']
results=[]
for entry in baseline['entries']:
 path=root/entry['path'];raw=path.read_bytes();raw.decode('utf-8',errors='strict')
 assert not raw.startswith(b'\xef\xbb\xbf'),str(path)
 assert not any(x<32 and x not in (9,10,13) for x in raw),str(path)
 if path.suffix=='.py':ast.parse(raw.decode('utf-8'))
 row={'path':entry['path'],'sha256':sha(raw),'status':'TEXT','encoding':'utf-8','bom':'NONE','crlf':raw.count(b'\r\n'),'lf':raw.count(b'\n')-raw.count(b'\r\n'),'historical_intent':'UNKNOWN'}
 if entry['status']=='MISSING':
  assert row['crlf']==0,str(path)
  row['preservation']='NEW_UTF8_NO_BOM_LF'
 else:
  snap=folder/'develop-before'/path.name
  if not snap.exists():snap=folder/'develop-before'/entry['path'].replace('/','_')
  if snap.exists():before=snap.read_bytes()
  elif entry['path']=='readme.md':before=raw.split(b'\r\n## Interface language / Idioma da interface',1)[0]
  else:before=raw
  assert sha(before)==entry['sha256'],('before bytes differ',str(path))
  assert row['lf']==before.count(b'\n')-before.count(b'\r\n'),str(path)
  row['preservation']='ORIGINAL_UTF8_NO_BOM_NEWLINE_STYLE_PRESERVED'
  row['approved_before_sha256']=entry['sha256']
 results.append(row)
(folder/'DEVELOP-ENCODING.json').write_text(json.dumps({'change_id':'change-004','approved_baseline_sha256':approved['encoding_sha256'],'entries':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('ENCODING_OK',len(results),'approved paths; baseline intact; original byte intent UNKNOWN')