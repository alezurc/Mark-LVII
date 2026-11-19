"""Compared static discovery, with immutable baseline and official comparator."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
out = root / '.ai'
runtime = Path(sys.argv[1])
run = 'discovery-2026-11-18-01'
report_path = out / 'DISCOVERY.md'
prior_bytes = report_path.read_bytes()
prior_text = prior_bytes.decode('utf-8')
block = re.search(r'## finding_registry\s+```json\s*(.*?)\s*```', prior_text, re.S)
if not block:
    raise SystemExit('Invalid/inaccessible canonical baseline; refusing refresh')
baseline = json.loads(block.group(1))
if baseline['run_id'] == run:
    raise SystemExit('This run already exists; refusing historical overwrite')
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
history = out / 'discovery-history' / baseline['run_id']
history.mkdir(parents=True, exist_ok=True)
def preserve(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise SystemExit('Historical snapshot conflict: ' + str(path))
    else:
        path.write_bytes(data)
preserve(history / 'DISCOVERY.md', prior_bytes)
preserve(history / 'DISCOVERY-REGISTRY.json', (json.dumps(baseline, ensure_ascii=False, indent=2) + '\n').encode())
preserve(history / 'DISCOVERY-EVIDENCE.json', (out / 'DISCOVERY-EVIDENCE.json').read_bytes())
old_evidence = json.loads((history / 'DISCOVERY-EVIDENCE.json').read_text(encoding='utf-8'))
old_by_path = {e['path']: e for e in old_evidence['entries']}

excluded = {'.git', '.ai', '.ai-sdd', '.codex', '__pycache__', 'config', 'reports',
            '.venv', 'venv', 'env', 'node_modules', 'build', 'dist'}
root_names = {'AGENTS.md', 'readme.md', 'requirements.txt', 'ai-sdd.project.yaml',
              '.gitignore', 'PROJECT-POLICY.md', 'CHANGELOG.md'}
paths = []
for base, dirs, files in os.walk(root):
    folder = Path(base)
    dirs[:] = [d for d in dirs if d not in excluded and not (folder == root / 'memory' and d == 'tasks')]
    for name in files:
        p = folder / name
        if p.suffix == '.py' or p.parent == root and name in root_names or p.parent == root / 'agents' and p.suffix == '.md':
            if p.is_symlink():
                raise SystemExit('Unexpected symlink in inventory: ' + str(p))
            paths.append(p)
entries, errors = [], []
for p in sorted(paths):
    data = p.read_bytes()
    rel = p.relative_to(root).as_posix()
    bom, codec = 'NONE', 'utf-8'
    for prefix, marker, encoding in [(b'\xff\xfe\x00\x00','UTF-32-LE','utf-32'), (b'\x00\x00\xfe\xff','UTF-32-BE','utf-32'), (b'\xef\xbb\xbf','UTF-8','utf-8-sig'), (b'\xff\xfe','UTF-16-LE','utf-16'), (b'\xfe\xff','UTF-16-BE','utf-16')]:
        if data.startswith(prefix):
            bom, codec = marker, encoding
            break
    try:
        decoded = data.decode(codec, errors='strict')
        status = 'UNKNOWN' if '\x00' in decoded or any(ord(c)<32 and c not in '\t\r\n\f' for c in decoded) else 'TEXT'
    except UnicodeError:
        codec, status = None, 'UNKNOWN'
    entries.append(dict(path=rel, sha256=hashlib.sha256(data).hexdigest(), status=status,
                        encoding=codec, bom=bom, method='BOM signature/strict payload decoding; strict UTF-8 when no BOM',
                        confidence='VALID_BYTES_ONLY' if status=='TEXT' else 'UNKNOWN',
                        limitation='No BOM does not establish author intent or a legacy codepage; not an approved editing baseline.'))
    if p.suffix == '.py':
        try:
            ast.parse(data, filename=rel)
        except (SyntaxError, UnicodeError) as exc:
            errors.append(dict(path=rel, error=str(exc)))
current_by_path = {e['path']: e for e in entries}
changed = [path for path in old_by_path if path not in current_by_path or old_by_path[path]['sha256'] != current_by_path[path]['sha256']]
tracked = subprocess.check_output(['git', 'ls-files', 'memory/tasks', 'reports'], cwd=root, text=True).splitlines()
evidence = dict(run_id=run, revision=revision, entries=entries, syntax_errors=errors,
                changed_since_baseline=changed, added_to_inventory=sorted(set(current_by_path)-set(old_by_path)),
                tracked_runtime_artifact_count=len(tracked),
                limits='No personal-data content, imports of product, model/service calls, GUI or tests executed in this refresh; AST is syntax only.')
run_dir = out / 'discovery-runs' / run
run_dir.mkdir(parents=True, exist_ok=True)
evidence_path = run_dir / 'EVIDENCE.json'
evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

findings = []
for previous in baseline['findings']:
    row = {k: copy.deepcopy(previous[k]) for k in ('subject','classification','evidence','description','implication','material')}
    # Unchanged source bytes reconfirm prior static observations; changed subjects are re-read.
    for ref in row['evidence']:
        path = ref.split(' @ ')[0].rsplit(':',1)[0] if re.search(r':\d+ @ ',ref) else ref.split(' @ ')[0]
        if path in old_by_path and path in changed and previous['id'] != 'D006':
            raise SystemExit('Finding needs material reconciliation: '+previous['id'])
    refs = []
    for ref in row['evidence']:
        location = ref.split(' @ ')[0]
        path = re.sub(r':\d+$','',location)
        if path in current_by_path:
            refs.append(location + ' @ working-tree sha256:' + current_by_path[path]['sha256'])
        elif location.startswith('git ls-files'):
            refs.append(evidence_path.relative_to(root).as_posix() + f' / tracked_runtime_artifact_count={len(tracked)}')
        elif location.startswith('.ai/DISCOVERY-EVIDENCE'):
            refs.append(evidence_path.relative_to(root).as_posix())
        else:
            refs.append(ref)
    row['evidence'] = refs
    if previous['id'] == 'D006':
        row.update(classification='CONFIRMED',
                   evidence=['actions/dev_agent.py:333','actions/dev_agent.py:364','actions/dev_agent.py:456','tests/test_dev_agent_vscode.py', '.ai/changes/change-001/REVIEW-REVISION-002.md', '.ai/changes/change-001/AI-SDD-CLOSE.json'],
                   description='Mudança material desde a baseline: change-001 substituiu o sucesso presumido por observação de janela com caminho completo, captura limitada a 64 KiB por stream e resultado conservador. A revisão registrou 29 testes PASS; a mudança está CLOSED.',
                   implication='D006 tratado (RESOLVED), preservando o conflito histórico em previous. Títulos sem caminho completo continuam não verificados; não há teste manual do editor nem prova integrada.')
        row['material'] = row['description'] + ' ' + row['implication']
        row['treatment_status'] = 'RESOLVED'
    elif previous['id'] == 'D011':
        row.update(description='Mudança de evidência: além dos autotestes de providers e do harness, há 29 testes focais documentados e aprovados para VS Code, incluindo fixtures locais. UI, áudio real, serviços externos, recuperação após crash e outras plataformas continuam sem validação integrada nesta inspeção.',
                   evidence=['providers/_tests.py:1','core/_smoke_harness.py:1','tests/test_dev_agent_vscode.py','.ai/changes/change-001/REVIEW-REVISION-002.md'])
        row['material'] = row['description'] + ' ' + row['implication']
    findings.append(row)

def add(subject, description, implication, refs):
    findings.append(dict(subject=subject, classification='CONFIRMED', evidence=refs,
                         description=description, implication=implication, material=description+' '+implication))
add('governance.documentation-policy',
    'Política publicada em PROJECT-POLICY.md: changelog por change-id, documentação atualizada quando instruções forem afetadas, identificação Mark LVII preservada e versão futura por decisão humana.',
    'Novas mudanças devem avaliar documentação e registrar histórico; a política não cria automaticamente versão, commit, tag ou release.',
    ['PROJECT-POLICY.md','CHANGELOG.md','.ai/changes/change-001/CLOSE-POLICY-BOOTSTRAP-EVIDENCE.json'])
add('governance.closed-change-knowledge',
    'change-001 foi encerrada pelo runtime, com auditoria, bootstrap documental autorizado e dois registros no Knowledge Register canônico (CONFIRMED e UNKNOWN).',
    'Reutilizar a evidência duradoura, sem promover UNKNOWN ou reclassificar retrospectivamente o finding aberto original; não há autorização ativa de desenvolvimento.',
    ['.ai/changes/change-001/AI-SDD-CLOSE.json','.ai/knowledge/KNOWLEDGE-REGISTER.json','.ai/AI-SDD.yaml'])
current = dict(run_id=run, project_scope=baseline['project_scope'],
               baseline=dict(source=(history/'DISCOVERY.md').relative_to(root).as_posix(), sha256=hashlib.sha256(prior_bytes).hexdigest(),
                             run_id=baseline['run_id'], revision=old_evidence['revision'], project_scope=baseline['project_scope']), findings=findings)
input_path = run_dir / 'CURRENT.json'
input_path.write_text(json.dumps(current, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
result = subprocess.run([sys.executable, '-B', str(runtime/'scripts/discovery_findings.py'), str(input_path), str(history/'DISCOVERY-REGISTRY.json')], capture_output=True, text=True, check=True, timeout=20)
registry = json.loads(result.stdout)
if any(f['comparison_status']=='AMBIGUOUS' for f in registry['findings']):
    raise SystemExit('Unresolved ambiguity; refusing publication')
sys.path.insert(0,str(runtime/'scripts'))
import discovery_findings as helper
helper.validate(registry['findings'], historical=True)
table = helper.render(registry)
report = f'''# Discovery — Mark-LVII — comparação após change-001

Execução: {run}. Escopo: {registry['project_scope']}. Revisão Git: `{revision}`; alterações locais são identificadas por SHA-256 no inventário, não atribuídas indevidamente ao commit. Modo COMPARED. Fonte anterior preservada em `{current['baseline']['source']}`, SHA-256 `{current['baseline']['sha256']}`.

## Método e arquitetura revalidada

Inspeção estática de {len(entries)} arquivos, com parsing AST de {sum(p.suffix=='.py' for p in paths)} arquivos Python: {len(errors)} erros. Dos {len(old_by_path)} arquivos da baseline, somente {', '.join(changed) or 'nenhum'} mudou; os outros contratos estáticos foram reconfirmados por igualdade dos bytes e pelas evidências originais. Fontes alteradas, novos testes, políticas, auditoria de CLOSE e KR foram inspecionados nesta execução. Evidência completa em `{evidence_path.relative_to(root).as_posix()}`.

Python mínimo 3.11; PyQt6, sounddevice/numpy, google-genai/httpx, Playwright e FastAPI/Uvicorn continuam declarados nos manifests sem mudança. main.py mantém sessão asyncio em thread e dispatch ao executor; ui.py mantém QApplication/sinais para gui/window.py. Loaders descobrem TOOL/PLUGIN, ignorando helpers com underscore. TaskEngine/rotinas, isolamento de ferramentas de background, pesquisa com verificação textual de citações, memória, settings e providers mantêm os contratos da inspeção anterior. Não se infere eficácia integrada a partir da existência desses controles.

Caches, segredos/configuração pessoal, conteúdo de memória, checkpoints, mídia e relatórios pessoais foram excluídos da leitura. Somente metadados do índice confirmam {len(tracked)} artefatos runtime versionados. Não houve instalação, imports do produto, chamadas de modelos/serviços, exploração de rede ou execução da aplicação. Os 29 testes são evidência documental da revisão fechada; não foram executados novamente neste DISCOVERY. AST não é teste comportamental.

## Findings e reconciliação

IDs/subjects anteriores preservados. D006 muda de CONFLICT para CONFIRMED com treatment_status=RESOLVED; o original fica em previous. D011 conserva UNKNOWN, com evidência focal ampliada; não equivale a validação integrada. Os novos subjects de governança recebem IDs acima do máximo anterior, por ordenação lexical do auxiliar oficial. Nenhum finding foi apagado ou renumerado por posição.

{table}

## Encoding, limites e próximos contextos

O inventário registra bytes, hash, BOM, método e confiança por arquivo. UTF-8 sem BOM prova validade dos bytes, não intenção histórica; D007 permanece UNKNOWN. CONTEXT futuro deve listar caminhos exatos em SCOPE.json e preparar ENCODING-POLICY quando necessária antes de aprovação. Preservar encoding/BOM no DEVELOP e reutilizar o KR canônico para conhecimento duradouro, sem criar registro paralelo.

O conflito de D006 foi tratado; candidatos remanescentes para escolha humana incluem D008 (persistência de memória, risco INFERRED), D010 (artefatos runtime no Git), D005 (requisitos de transporte do dashboard) e D011 (evidência integrada UNKNOWN). Isso não autoriza correção, teste externo ou implementação. D012 continua limitação documentada de DNS rebinding; não se afirma sandbox completo. Nenhum requisito material desta inspeção dependeu de evidência externa, portanto nenhuma Boundary Stop foi acionada. UNKNOWNs e riscos foram preservados; não foi aberto novo ciclo CONTEXT.

## finding_registry

```json
{json.dumps(registry, ensure_ascii=False, indent=2)}
```
'''
if report_path.read_bytes() != prior_bytes:
    raise SystemExit('Canonical report changed concurrently')
# Verify observed files did not change before publishing governance artifacts.
for entry in entries:
    if hashlib.sha256((root/entry['path']).read_bytes()).hexdigest() != entry['sha256']:
        raise SystemExit('Evidence changed during discovery: '+entry['path'])
(out/'DISCOVERY-REGISTRY.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(out/'DISCOVERY-EVIDENCE.json').write_bytes(evidence_path.read_bytes())
report_path.write_text(report, encoding='utf-8')
print(json.dumps(dict(run_id=run, files=len(entries), python_files=sum(p.suffix=='.py' for p in paths), syntax_errors=errors,
                     changed=changed, findings=len(registry['findings']),
                     comparisons={status:sum(f['comparison_status']==status for f in registry['findings']) for status in ('SAME_FINDING','CHANGED','NEW','NOT_RECONFIRMED')},
                     unknown_encoding=[e['path'] for e in entries if e['status']=='UNKNOWN']), ensure_ascii=True))
