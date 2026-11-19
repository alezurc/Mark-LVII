"""Prepare governance proposals and plan only; never publish root files."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[3]
directory = root / '.ai/changes/change-001'
plan_path = directory / 'CLOSE-PLAN.json'
history = directory / 'close-plan-history/pre-bootstrap.json'
if not history.exists():
    history.parent.mkdir(parents=True, exist_ok=True)
    history.write_bytes(plan_path.read_bytes())
plan = json.loads(plan_path.read_text(encoding='utf-8'))
drafts = directory / 'proposals'
policy_path = drafts / 'PROJECT-POLICY.md'
policy = policy_path.read_text(encoding='utf-8')
policy = policy.replace('Proposta para publicação em `PROJECT-POLICY.md`. Preparada para a change-001; sua publicação depende do escopo autorizado pelo AI-SDD.\n\n', '')
policy_path.write_bytes(policy.encode('utf-8'))
changelog_path = drafts / 'CHANGELOG.md'
changelog = changelog_path.read_text(encoding='utf-8')
changelog = changelog.replace('Proposta para publicação em `CHANGELOG.md`. As entradas registram mudanças revisadas, sem representar release ou publicação automática.', 'As entradas registram mudanças revisadas, sem representar release ou publicação automática.')
changelog_path.write_bytes(changelog.encode('utf-8'))

targets = []
for name, role in [('PROJECT-POLICY.md', 'PROJECT_POLICY'), ('CHANGELOG.md', 'CHANGELOG')]:
    destination = root / name
    proposal = drafts / name
    targets.append(dict(path=name, role=role, proposal=proposal.relative_to(root).as_posix(),
                        sha256=hashlib.sha256(proposal.read_bytes()).hexdigest(),
                        before_sha256=hashlib.sha256(destination.read_bytes()).hexdigest() if destination.is_file() else None))

evidence = '.ai/changes/change-001/CLOSE-BOOTSTRAP-PROPOSAL.md'
plan['evidence_refs'] = list(dict.fromkeys(plan['evidence_refs'] + [evidence]))
plan['unresolved_unknowns'] = [dict(description='Intenção histórica de encoding sem BOM não comprovada; preservação verificada.', material=False)]
plan['unresolved_conflicts'] = []
plan['material_decision_required'] = True
plan['proposed_version'] = None
plan['versioning'] = dict(status='PROPOSED', strategy='KEEP_CURRENT_IDENTIFIER', strategy_target='PROJECT-POLICY.md',
                          evidence_refs=[evidence, targets[0]['proposal']])
plan['changelog'] = dict(impact='YES', reason='Registrar change-001 por identificador, segundo a política proposta aceita em abordagem pelo usuário.',
                         targets=[dict(path='CHANGELOG.md', kind='UPDATE', change_id='change-001', sha256=targets[1]['sha256'],
                                       evidence_refs=[evidence, targets[1]['proposal']])],
                         evidence_refs=[evidence, targets[1]['proposal']], strategy_target='PROJECT-POLICY.md')
plan['close_policy_bootstrap'] = dict(change_id='change-001',
    versioning_decision=dict(strategy='KEEP_CURRENT_IDENTIFIER', current_identifier='Mark LVII', proposed_version=None),
    targets=targets)
for field in ('blockers', 'human_decision_required', 'close_ready'):
    plan.pop(field, None)

# Official digest implementation from the explicitly declared installation.
sys.path.insert(0, str(Path(sys.argv[1]) / 'runtime'))
from close_lifecycle import plan_digest
digest = plan_digest(plan)
plan_path.write_bytes((json.dumps(plan, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
lines = ['# Publicação proposta — CLOSE_POLICY_BOOTSTRAP — change-001', '',
         'Substitui a limitação operacional de POLICY-PROPOSAL.md pelo adendo agora presente na instalação declarada.',
         'A abordagem foi aceita pelo usuário com “pode seguir com essa abordagem”; a publicação exata abaixo ainda exige autorização específica.', '',
         'Decisão proposta: KEEP_CURRENT_IDENTIFIER; identificação atual Mark LVII; proposed_version=null. Sem nova versão, commit, tag, release ou publicação externa.', '',
         '| Destino exato | SHA-256 dos bytes propostos | Preimagem |', '|---|---|---|']
for target in targets:
    lines.append(f"| {target['path']} | `{target['sha256']}` | {target['before_sha256'] or 'ausente (null)'} |")
lines += ['', f'Hash oficial do plano: `{digest}`.', '',
          'Conteúdos exatos estão em proposals/PROJECT-POLICY.md e proposals/CHANGELOG.md. Os avisos de rascunho foram removidos desses bytes antes do hash; nenhuma alteração de conteúdo será feita após autorização.',
          'Nenhum arquivo-raiz foi publicado. APPROVED-SCOPE.json, DEVELOP/REVIEW e autorização histórica permanecem intactos. O runtime registrará CLOSE_GOVERNANCE_SCOPE somente após instrução humana explícita sobre plano, conteúdos, destinos, hashes e decisão de versão.',
          'A confirmação de ausência prévia será repetida antes de publicar. Divergência de preimagem ou mudança do plano exige nova autorização.',
          'Os impactos UNKNOWN anteriores relativos à política são substituídos por proposta concreta; isso não constitui aprovação da proposta. Os registros antigos permanecem no histórico.']
(directory / 'CLOSE-BOOTSTRAP-PROPOSAL.md').write_bytes(('\n'.join(lines) + '\n').encode('utf-8'))
print(json.dumps(dict(plan_sha256=digest, targets=targets, versioning=plan['close_policy_bootstrap']['versioning_decision']), ensure_ascii=True, indent=2))
