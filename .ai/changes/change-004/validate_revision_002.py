from pathlib import Path
import ast,difflib,hashlib,json
folder=Path('.ai/changes/change-004')
baseline=json.loads((folder/'ENCODING-BASELINE.json').read_text(encoding='utf-8'))
approved=json.loads((folder/'APPROVED-SCOPE.json').read_text(encoding='utf-8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((folder/'ENCODING-BASELINE.json').read_bytes())==approved['encoding_sha256']
checks=[];patch=[];changed=[]
for entry in baseline['entries']:
 path=Path(entry['path']);before=(folder/'develop-revision-002-before'/entry['path'].replace('/','_')).read_bytes();after=path.read_bytes()
 assert sha(before)==entry['sha256'],('bad snapshot',str(path))
 text=after.decode('utf-8',errors='strict');assert not after.startswith(b'\xef\xbb\xbf')
 assert not any(x<32 and x not in (9,10,13) for x in after)
 old_crlf=before.count(b'\r\n');new_crlf=after.count(b'\r\n')
 assert (new_crlf>0)==(old_crlf>0),str(path)
 assert after.count(b'\n')-new_crlf==0 if old_crlf else new_crlf==0
 if path.suffix=='.py':ast.parse(text)
 if before!=after:
  changed.append(entry['path'])
  patch.extend(difflib.unified_diff(before.decode('utf-8').replace('\r\n','\n').splitlines(keepends=True),text.replace('\r\n','\n').splitlines(keepends=True),fromfile='before/'+entry['path'],tofile='after/'+entry['path']))
 checks.append({'path':entry['path'],'before_sha256':entry['sha256'],'after_sha256':sha(after),'changed':before!=after,'status':'TEXT','encoding':'utf-8','bom':'NONE','newline':'CRLF' if new_crlf else 'LF','historical_intent':'UNKNOWN'})
assert set(changed)=={'gui/window.py','gui/widgets.py','gui/i18n.py','tests/test_ui_language_qt.py'},changed
for name in ('DEVELOP-EVIDENCE.json','REVIEW-EVIDENCE.json'):
 for item in json.loads((folder/name).read_text(encoding='utf-8')):
  assert sha((folder/item['path']).read_bytes())==item['sha256'],('historical evidence changed',item['path'])
(folder/'DEVELOP-REVISION-002-ENCODING.json').write_text(json.dumps({'change_id':'change-004','revision':'002','approved_baseline_sha256':approved['encoding_sha256'],'status':'PASS','changed_paths':changed,'checks':checks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
(folder/'DEVELOP-REVISION-002.patch').write_text(''.join(patch),encoding='utf-8',newline='\n')
print('ENCODING_PASS 12 approved paths; 4 changed; historical evidence intact')