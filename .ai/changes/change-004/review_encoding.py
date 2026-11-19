from pathlib import Path
import json,hashlib,ast
folder=Path('.ai/changes/change-004');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
approved=json.loads((folder/'APPROVED-SCOPE.json').read_text(encoding='utf-8'))
baseline=json.loads((folder/'ENCODING-BASELINE.json').read_text(encoding='utf-8'))
assert sha(folder/'ENCODING-BASELINE.json')==approved['encoding_sha256']
expected=json.loads((folder/'DEVELOP-ENCODING.json').read_text(encoding='utf-8'))
checks=[]
for entry in expected['entries']:
 p=Path(entry['path']);b=p.read_bytes();b.decode('utf-8',errors='strict')
 assert sha(p)==entry['sha256'],('Changed since DEVELOP',str(p))
 assert not b.startswith(b'\xef\xbb\xbf'),str(p)
 assert b.count(b'\r\n')==entry['crlf'] and b.count(b'\n')-b.count(b'\r\n')==entry['lf'],str(p)
 if p.suffix=='.py':ast.parse(b.decode('utf-8'))
 checks.append({'path':str(p).replace('\\','/'),'sha256':sha(p),'status':'PASS','encoding':'utf-8','bom':'NONE','historical_intent':'UNKNOWN'})
for entry in json.loads((folder/'DEVELOP-EVIDENCE.json').read_text(encoding='utf-8')):
 assert sha(folder/entry['path'])==entry['sha256'],('Development evidence changed',entry['path'])
(folder/'REVIEW-ENCODING-CHECK.json').write_text(json.dumps({'change_id':'change-004','status':'PASS','approved_baseline_sha256':approved['encoding_sha256'],'checks':checks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('REVIEW_ENCODING_PASS; 12 paths unchanged since DEVELOP; development evidence hashes intact')