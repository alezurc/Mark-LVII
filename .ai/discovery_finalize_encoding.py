"""Reconcile the refined encoding evidence before completing this run."""
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
directory = root / '.ai/discovery-runs/discovery-2026-11-18-01'
path = directory / 'CURRENT.json'
current = json.loads(path.read_text(encoding='utf-8'))
row = next(r for r in current['findings'] if r['subject']=='encoding.intent-not-established')
row['description'] = ('Evidência ampliada pelo detector conservador: além da intenção histórica sem BOM continuar desconhecida, providers/_tests.py contém os controles preexistentes U+0001 e U+0002. Seus bytes são UTF-8 válidos, mas o perfil conservador registra status UNKNOWN; não houve mudança desses bytes desde a baseline.')
row['implication'] = ('Não inferir codepage nem converter esses bytes automaticamente. Uma futura edição desse alvo exige SCOPE exato e decisão/política apropriada antes da aprovação de CONTEXT. A classificação refinada não reescreve a evidência histórica anterior.')
row['material'] = row['description']+' '+row['implication']
row['evidence'] = ['.ai/discovery-runs/discovery-2026-11-18-01/EVIDENCE.json','providers/_tests.py']
path.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
runtime = Path(sys.argv[1])
baseline = root / '.ai/discovery-history/discovery-2026-11-17-01/DISCOVERY-REGISTRY.json'
result = subprocess.run([sys.executable,'-B',str(runtime/'scripts/discovery_findings.py'),str(path),str(baseline)],capture_output=True,text=True,check=True,timeout=20)
registry = json.loads(result.stdout)
sys.path.insert(0,str(runtime/'scripts'))
import discovery_findings as helper
helper.validate(registry['findings'],historical=True)
report_path = root / '.ai/DISCOVERY.md'
text = report_path.read_text(encoding='utf-8')
snapshot = directory / 'REPORT-BEFORE-ENCODING-RECONCILIATION.md'
if not snapshot.exists():
    snapshot.write_bytes(report_path.read_bytes())
text = re.sub(r'\| ID \| Subject \| Classification.*?(?=\n## Encoding,)',helper.render(registry)+'\n',text,flags=re.S)
text = text.replace('D011 conserva UNKNOWN, com evidência focal ampliada;', 'D007 conserva UNKNOWN, com detecção conservadora dos controles preexistentes U+0001/U+0002 em providers/_tests.py; D011 conserva UNKNOWN, com evidência focal ampliada;')
text = text.split('## finding_registry')[0] + '## finding_registry\n\n```json\n'+json.dumps(registry,ensure_ascii=False,indent=2)+'\n```\n'
(root/'.ai/DISCOVERY-REGISTRY.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report_path.write_text(text,encoding='utf-8')
print(json.dumps({status:sum(f['comparison_status']==status for f in registry['findings']) for status in ('SAME_FINDING','CHANGED','NEW','AMBIGUOUS')},ensure_ascii=True))
