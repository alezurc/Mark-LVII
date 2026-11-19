"""Prepare governance artifacts only; never writes product or runtime state."""
from pathlib import Path
import hashlib
import json

folder = Path('.ai/changes/change-004')
sha = lambda data: hashlib.sha256(data).hexdigest()
write = lambda name, data: (folder / name).write_text(data, encoding='utf-8', newline='\n')
reference = 'Aprovo o CONTEXT revisão 002 da change-004'
review = str(folder / 'REVIEW-REVISION-002.md').replace('\\', '/')
context = str(folder / 'CONTEXT.md').replace('\\', '/')
encoding = str(folder / 'REVIEW-REVISION-002-ENCODING-CHECK.json').replace('\\', '/')
evidence = str(folder / 'CLOSE-EVIDENCE.md').replace('\\', '/')
refs = [context, review, encoding, evidence]

# Verify delivered product and immutable evidence before proposing consolidation.
approved = json.loads((folder / 'APPROVED-SCOPE.json').read_text(encoding='utf-8'))
assert sha((folder / 'ENCODING-BASELINE.json').read_bytes()) == approved['encoding_sha256']
checks = json.loads((folder / 'REVIEW-REVISION-002-ENCODING-CHECK.json').read_text(encoding='utf-8'))['checks']
for item in checks:
    assert sha(Path(item['path']).read_bytes()) == item['sha256'], item['path']
for name in ('DEVELOP-EVIDENCE.json', 'REVIEW-EVIDENCE.json', 'DEVELOP-REVISION-002-EVIDENCE.json', 'REVIEW-REVISION-002-EVIDENCE.json'):
    for item in json.loads((folder / name).read_text(encoding='utf-8')):
        assert sha((folder / item['path']).read_bytes()) == item['sha256'], item['path']

old = Path('CHANGELOG.md').read_bytes()
assert b'\r' not in old and not old.startswith(b'\xef\xbb\xbf')
entry = '''## change-004 — idioma da interface desktop

- Personalização permite escolher English/en ou Português (Brasil)/pt-BR, aplicar imediatamente e persistir a preferência para a próxima inicialização. Inglês é o padrão sem preferência válida; cancelar mantém o idioma e falha de gravação aparece na interface.
- A tradução usa catálogo explícito e preserva texto digitado, conteúdo recebido, nomes, caminhos e configurações de voz/provedores. Retraduzir não reabre conteúdo dispensado nem tira espaço do quiz; seleção, rolagem, pergunta e resposta em andamento são preservadas nos cenários verificados.
- Arquivo/pasta carregados exibem FILE/ARQUIVO, FOLDER/PASTA e contagem singular/plural com marcador de limite, sem traduzir nomes ou recarregar a pasta.
- Validação da revisão 002: 66 testes unittest PASS; providers 98 PASS, zero FAIL e dois SKIPs opcionais por Piper ausente. Testes Qt offscreen com dados sintéticos e inspeção focal de renders nos dois idiomas; UTF-8 sem BOM e finais de linha preservados.
- Limitações: revisão não isolada, aprovada explicitamente pelo responsável. UI interativa em outras plataformas/resoluções, acessibilidade integral, fallback de fontes/ícones, áudio físico e serviços reais permanecem não demonstrados; intenção histórica de encoding sem BOM continua UNKNOWN.
- Identificação mantida: **Mark LVII**, conforme PROJECT-POLICY.md. Sem nova versão, commit, tag, release ou publicação.

Evidência técnica: .ai/changes/change-004/REVIEW-REVISION-002.md e .ai/changes/change-004/DEVELOP-REVISION-002.md. Os achados e relatórios anteriores permanecem preservados como histórico.

'''
marker = '## change-003'
text = old.decode('utf-8')
assert text.count(marker) == 1 and '## change-004' not in text
proposed = text.replace(marker, entry + marker, 1)
write('CHANGELOG-PROPOSED.md', proposed)

write('CLOSE-EVIDENCE.md', '''# CLOSE — change-004

Consolidação autorizada pelo pedido ai-sdd close após REVIEW_APPROVED, referência humana “Considero como aprovado após analisar o REVIEW-REVISION-002.md”. CONTEXT revisão 002 aprovado por “Aprovo o CONTEXT revisão 002 da change-004”. Papel ORCHESTRATOR, codex, Core v0.2.0; ALLOW em todos os termos; sem expansão/fallback. Lease próprio: 5548e039-f019-4ff8-bbb1-24c6b344c5ed.

Plano: manter o README já revisado com instruções nos dois idiomas; acrescentar ao CHANGELOG somente a entrada change-004 proposta, preservando LF/UTF-8 sem BOM; consolidar no KR os contratos de localização/preservação e os limites UNKNOWN. Não há PROJECT-SPEC existente ou proposta material nesta mudança, nem novo requisito além do CONTEXT aprovado. PROJECT-POLICY.md estabelece KEEP_CURRENT_IDENTIFIER; manter Mark LVII sem nova versão/publicação. Não é necessário bootstrap de política ou nova decisão material.

Proveniência: 12 arquivos entregues conferidos contra a evidência da revisão; baseline aprovado e manifests DEVELOP/REVIEW das duas revisões íntegros. A publicação do changelog fica condicionada a check-close e check-stage bem-sucedidos; o runtime revalida encoding e hashes na conclusão. CLOSE-ENCODING-CHECK.json e CLOSE-TARGETS.json registrarão o estado final. Não reexecutar testes de produto sem alteração funcional: evidência aprovada é 66 unittest PASS e providers 98 PASS/0 FAIL/2 SKIP, preservada por hash.

Limites preservados: NON_ISOLATED_REVIEW submetida à aprovação explícita; validação Windows/Python 3.15.2/PyQt6 6.12.1/Qt 6.12.0 sintética/offscreen; Piper opcional ausente; serviços reais, áudio físico, UI interativa em todas as plataformas/resoluções, acessibilidade integral e fallback de fontes/ícones UNKNOWN. Validade UTF-8 não prova intenção histórica. Sem nova Boundary Stop material; registros DEP-004-001 permanecem históricos, sem reabertura externa. Sem edição de código funcional, settings pessoais, política, versão, commit, tag ou release no CLOSE.

Conclusão efetiva de lifecycle e consolidação KR são responsabilidade exclusiva de complete CLOSE após validações; este documento não antecipa CLOSED.
''')

def section(impact, reason, targets=None):
    return dict(impact=impact, reason=reason, targets=targets or [], evidence_refs=refs)

def target(path, digest, sources):
    return dict(path=path, kind='UPDATE', change_id='change-004', sha256=digest, evidence_refs=sources)

records = []
for number, statement, classification, requirements, sources in [
    (1, 'A interface desktop oferece en padrão e pt-BR persistido por config_manager antes da criação dos widgets. Catálogo e bindings explícitos preservam conteúdo opaco e independência de voz/provedores no perfil testado.', 'CONFIRMED', ['AC1','AC2','AC3','AC4','AC5'], ['gui/i18n.py','ui.py','memory/config_manager.py',review]),
    (2, 'Retradução plain/code/review usa present=False para preservar apresentação e quiz. Pintura de arquivo/pasta traduz somente rótulos próprios e singular/plural, mantendo nome/extensão e evitando reload; regressões Qt cobrem os dois sentidos.', 'CONFIRMED', ['AC10','AC11','AC12','AC13'], ['gui/window.py','gui/widgets.py','tests/test_ui_language_qt.py',review]),
    (3, 'Os 12 alvos de change-004 preservam UTF-8 sem BOM e finais de linha aprovados; bytes válidos não estabelecem intenção histórica de encoding. A evidência de revisão registra baseline aprovado e hashes por caminho.', 'CONFIRMED', ['AC9'], [str(folder/'ENCODING-BASELINE.json').replace('\\','/'),encoding,review]),
    (4, 'Intenção histórica de encoding, UI interativa em todas as plataformas/resoluções, acessibilidade integral, fallback de fontes/ícones, áudio físico e serviços reais permanecem não demonstrados. A evidência de change-004 é sintética/offscreen e preserva skips opcionais de Piper.', 'UNKNOWN', ['AC6','AC8','AC9'], [context,review,encoding]),
]:
    records.append(dict(id=f'KR-change-004-{number:03}', statement=statement, classification=classification, evidence_refs=sources, context_reference=reference, traceability=dict(change_id='change-004', requirements=requirements, review=review)))

plan = dict(schema_version=1, change_id='change-004', project_mode='EXISTING', context_reference=reference, evidence_refs=refs,
    unresolved_unknowns=[dict(description=records[-1]['statement'],material=False)], unresolved_conflicts=[],
    risks=['NON_ISOLATED_REVIEW aprovada explicitamente pelo humano; sem alegar revisão independente.', 'Cobertura offscreen local não demonstra todos os perfis interativos.'],
    material_decision_required=False, proposed_version=None,
    versioning=dict(status='EXISTING',strategy='KEEP_CURRENT_IDENTIFIER',strategy_target='PROJECT-POLICY.md',evidence_refs=['PROJECT-POLICY.md']),
    knowledge=section('YES','Consolidar contratos locais de localização e preservação, evidência de encoding e limites UNKNOWN.'),
    user_docs=section('YES','README já atualizado e revisado; instruções permanecem corretas, nenhuma nova edição no CLOSE.',[target('readme.md',sha(Path('readme.md').read_bytes()),[review,'readme.md'])]),
    changelog=section('YES','Registrar alteração observável, validação e limites conforme política existente e alvo aprovado.',[target('CHANGELOG.md',sha(proposed.encode('utf-8')),[str(folder/'CHANGELOG-PROPOSED.md').replace('\\','/'),review])]),
    project_spec=section('NO','Sem novo requisito ou proposta de especificação material; consolidar somente o CONTEXT aprovado.'))
plan['knowledge']['records'] = records
plan['changelog']['strategy_target'] = 'PROJECT-POLICY.md'
plan['project_spec']['material'] = False
write('CLOSE-PLAN.json', json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print('CLOSE_PLAN_PREPARED; product unchanged; prior evidence hashes verified')
