"""Discovery evidence generation: stdlib, no product imports or mutations."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '.ai'
RUN = 'discovery-2026-11-17-01'
REV = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
paths = sorted(p for p in ROOT.rglob('*') if p.is_file() and
               not any(x in {'.git', '.ai', '.ai-sdd', '.codex', '__pycache__', 'config', 'reports'} for x in p.relative_to(ROOT).parts)
               and (p.suffix == '.py' or p.name in {'requirements.txt', 'AGENTS.md', 'readme.md', 'ai-sdd.project.yaml', '.gitignore'}
                    or p.parent == ROOT / 'agents'))
entries, syntax = [], []
for p in paths:
    rel = p.relative_to(ROOT).as_posix()
    b = p.read_bytes()
    bom, enc = 'NONE', 'utf-8'
    for prefix, name, codec in [(b'\xff\xfe\x00\x00','UTF-32-LE','utf-32'), (b'\x00\x00\xfe\xff','UTF-32-BE','utf-32'), (b'\xef\xbb\xbf','UTF-8','utf-8-sig'), (b'\xff\xfe','UTF-16-LE','utf-16'), (b'\xfe\xff','UTF-16-BE','utf-16')]:
        if b.startswith(prefix):
            bom, enc = name, codec
            break
    try:
        decoded = b.decode(enc, errors='strict')
        status = 'TEXT' if '\x00' not in decoded else 'UNKNOWN'
    except UnicodeError:
        decoded, status, enc = None, 'UNKNOWN', None
    entries.append(dict(path=rel, sha256=hashlib.sha256(b).hexdigest(), status=status,
                        encoding=enc, bom=bom, method='BOM signature and strict decode; UTF-8 strict when no BOM',
                        confidence='byte-validity only', limitation='No BOM does not prove intended encoding; ASCII remains ambiguous. Not an approved edit baseline.'))
    if p.suffix == '.py':
        try:
            ast.parse(b, filename=rel)
        except (SyntaxError, UnicodeError) as exc:
            syntax.append({'path': rel, 'error': str(exc)})
(OUT / 'DISCOVERY-EVIDENCE.json').write_text(json.dumps(dict(run_id=RUN, revision=REV, method='Static inspection and AST parse only; no imports, execution, provider calls or personal-data reads.', entries=entries, syntax_errors=syntax), ensure_ascii=False, indent=2), encoding='utf-8')

findings = []
def add(subject, classification, evidence, description, implication):
    findings.append(dict(subject=subject, classification=classification,
                         evidence=[f'{x} @ {REV}' for x in evidence], description=description,
                         implication=implication, material=description + ' ' + implication))

add('architecture.qt-worker-boundary','CONFIRMED',['main.py:1727','main.py:3052','ui.py:103','ui.py:265','gui/window.py:398'],
    'Qt fica no thread principal; a sessão asyncio roda em thread dedicado; ações/plugins são despachados ao executor. JarvisUI emite sinais para a janela.',
    'Mudanças de UI devem preservar os sinais e a única QApplication; ferramentas não podem construir widgets.')
add('automation.background-policy','CONFIRMED',['core/tasks/tools.py:87','core/tasks/tools.py:96','core/tasks/engine.py:268'],
    'TaskEngine agenda workers e TaskTools filtra ferramentas, separa web de recall_memory e restringe caminhos à pasta da tarefa.',
    'Trabalho longo pertence ao motor de tarefas; isto confirma controles estáticos, não isolamento completo demonstrado.')
add('automation.routines-and-research','CONFIRMED',['core/routines/engine.py:114','core/tasks/research.py:111','core/tasks/research.py:342','main.py:726'],
    'Rotinas usam armazenamento compartilhado de JSON; pesquisa registra fontes e verifica trechos contra páginas salvas.',
    'A verificação textual de citações não demonstra verdade factual nem qualidade global do relatório.')
add('configuration.atomic-settings','CONFIRMED',['memory/config_manager.py:38','memory/config_manager.py:52','memory/config_manager.py:69'],
    'Configuração usa RLock, arquivo temporário e os.replace, com tratamento de arquivo corrompido.',
    'Usar config_manager; serialização dentro do processo não prova coordenação entre processos ou durabilidade após perda de energia.')
add('dashboard.transport-fallback','CONFIRMED',['dashboard/server.py:1248','dashboard/server.py:1276','dashboard/server.py:750'],
    'Dashboard usa pareamento/tokens e pode servir HTTP em 0.0.0.0 quando TLS não está disponível, com aviso explícito.',
    'Exposição real depende da configuração/rede; não foi verificada. Requisito de TLS obrigatório exigiria contexto específico.')
add('developer.vscode-success-claim','CONFLICT',['AGENTS.md','actions/dev_agent.py:299'],
    '_open_vscode descarta stdout/stderr com DEVNULL, espera 1,5 s e anuncia VSCode opened sem verificar janela/processo; conflita com a regra geral do AGENTS.md.',
    'Uma tentativa pode ser anunciada como sucesso. Corrigir apenas em change com contexto e aprovação próprios.')
add('encoding.intent-not-established','UNKNOWN',['.ai/DISCOVERY-EVIDENCE.json'],
    'O inventário registra hash, BOM e decodificação estrita por arquivo; a intenção de encoding sem BOM permanece desconhecida.',
    'Antes de aprovação de CONTEXT, preparar SCOPE.json com arquivos exatos e política de encoding quando necessária; preservar bytes no DEVELOP.')
add('memory.persistence-risk','INFERRED',['memory/memory_manager.py:118','core/tasks/store.py:31'],
    'save_memory grava o arquivo diretamente; o store de tarefas usa temporário e replace. Interrupção durante gravação pode afetar a memória de forma diferente.',
    'Risco de truncamento inferido da estratégia de escrita; nenhum crash ou perda de dados foi reproduzido.')
add('models.shared-ladder-coupling','CONFIRMED',['core/gemini.py:714','core/gemini.py:814','core/tasks/brain.py:142'],
    'core.gemini concentra deadlines/fallback; o motor de tarefas usa a ladder e helpers privados para chamadas com ferramentas.',
    'Mudanças na ladder afetam voz, chamadas avulsas e tarefas; preservar compatibilidade dos caminhos com tool-calling.')
add('repository.runtime-artifacts-tracked','CONFIRMED',['.gitignore','git ls-files memory/tasks reports'],
    'O índice Git contém checkpoints, páginas de pesquisa e um relatório gerado; .gitignore não exclui memory/tasks nem reports.',
    'Revisar política de dados antes de futuras publicações. O conteúdo desses artefatos não foi lido nem classificado como segredo.')
add('tests.end-to-end-evidence','UNKNOWN',['providers/_tests.py:1','core/_smoke_harness.py:1'],
    'Existem autotestes de providers e harness de smoke, mas esta execução não validou UI, áudio real, serviços externos, recuperação após crash ou plataformas alternativas.',
    'Evidência mínima depende da futura change: testes focais e observação do fluxo afetado. Não declarar funcionamento integrado com base em parsing.')
add('web.dns-rebinding-limitation','CONFIRMED',['core/tasks/web.py:21','core/tasks/web.py:52','core/tasks/web.py:128'],
    'Fetch valida IPs públicos e redirects, mas documenta limitação quando o hostname resolve de modo diferente entre validação e conexão.',
    'Não apresentar o filtro como sandbox completo; exploração e eficácia em execução não foram testadas.')

current = dict(run_id=RUN, project_scope='Mark-LVII / whole-project static discovery', baseline=None,
               baseline_reason='Primeiro relatório canônico: .ai/DISCOVERY.md ausente antes desta execução.', findings=findings)
current_path = OUT / 'DISCOVERY-CURRENT.json'
current_path.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(files=len(entries), python_files=sum(p.suffix=='.py' for p in paths), syntax_errors=syntax, unknown_encoding=[e['path'] for e in entries if e['status']=='UNKNOWN']), ensure_ascii=True))

if len(sys.argv) > 1:
    import importlib.util
    helper = Path(sys.argv[1])
    spec = importlib.util.spec_from_file_location('discovery_findings', helper)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    registry = mod.compare(current)
    (OUT / 'DISCOVERY-REGISTRY.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    report = f'''# Discovery — Mark-LVII

Execução: {RUN}. Revisão Git: `{REV}`. FIRST_BASELINE; baseline null porque não havia relatório anterior comparável. Nenhum histórico foi sobrescrito.

## Escopo e método

Inspeção estática aprofundada dos pontos de entrada, loaders, UI, configuração, memória, tarefas, rotinas, pesquisa, providers, dashboard e agente de código. Manifests: requirements.txt e setup.py; Python mínimo 3.11, PyQt6, sounddevice/numpy, google-genai/httpx, Playwright e FastAPI/Uvicorn. Origin: https://github.com/alezurc/Mark-LVII.git; upstream: https://github.com/FatihMakes/Mark-LVII.git.

O inventário em DISCOVERY-EVIDENCE.json captura hashes dos fontes e documentos selecionados, encoding/BOM, método, confiança e limitações. Foram analisados {len(entries)} arquivos, incluindo {sum(p.suffix=='.py' for p in paths)} arquivos Python por AST, sem importar o produto. Erros de sintaxe encontrados: {len(syntax)}. Isso não substitui testes comportamentais. Fontes locais/untracked são identificadas pelo hash; o SHA Git identifica o checkout, não os documentos de governança novos.

Segredos/configuração pessoal, conteúdo de memória, checkpoints, relatórios pessoais, mídia, dependências, caches e internals Git foram excluídos da leitura de conteúdo. Apenas metadados do índice demonstram artefatos runtime versionados. A busca de testes encontrou providers/_tests.py e o harness core/_smoke_harness.py; não estabelece ausência absoluta de outros testes.

## Arquitetura e contratos

main.py coordena voz e ferramentas; ui.py adapta chamadas thread-safe para gui/window.py. gui/theme.py e gui/style.py são os pontos de paleta/fontes. core/action_loader.py descobre TOOL e core/plugin_loader.py descobre PLUGIN; helpers iniciados por underscore são ignorados. Plugins são opt-out via config_manager. core/tasks contém scheduler, checkpoints, ferramentas limitadas e pesquisa; core/routines agenda ações recorrentes. agents/*.md descreve perfis, sem conceder ferramentas fora da allowlist. providers oferece pipeline STT/LLM/TTS opcional. dashboard/server.py fornece pareamento e controle remoto. core/confirm.py guarda ações irreversíveis atrás da UI; core/outcome.py distingue resultado verificado, não verificado e falha. core/code_checks.py e actions/dev_agent.py implementam verificações e proteção de projetos editados.

## Findings

{mod.render(registry)}

## Limites e próximos levantamentos

Não houve chamada de fornecedor, instalação, teste de áudio, abertura da aplicação, simulação de crash, alteração do produto ou teste de exploração. As alegações do README são contexto declarativo; não foram tratadas como medições atuais. Sem change/requisito concreto que dependa de evidência externa, nenhuma condição material de Boundary Stop foi acionada nesta inspeção. UNKNOWNs permanecem abertos, sem promover readiness ou autorização. Se um contexto futuro depender de evidência externa, aplicar o registro e a parada do contrato de boundary, sem expandir automaticamente a investigação.

Prioridades sugeridas para escolha humana: verificação do launcher VS Code; política de artefatos runtime no Git; persistência de memória; requisitos de transporte do dashboard. Nenhuma prioridade autoriza correção. CONTEXT exige change-id explícito, escopo exato e critérios de aceitação. SCOPE/ENCODING-POLICY devem estar preparados antes de aprovação; este inventário não substitui o baseline capturado pelo runtime. Sem criar Knowledge Register paralelo: eventual impacto duradouro de encoding deve usar o KR Day1 no lifecycle apropriado.

## finding_registry

```json
{json.dumps(registry, ensure_ascii=False, indent=2)}
```
'''
    if (OUT / 'DISCOVERY.md').exists():
        raise SystemExit('Refusing to overwrite existing canonical report without baseline reconciliation')
    (OUT / 'DISCOVERY.md').write_text(report, encoding='utf-8')
    print('DISCOVERY_REPORT_WRITTEN; registry validated by official helper')
