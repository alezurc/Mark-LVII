"""Prepare governance artifacts only; product writes require check-close first."""
import hashlib
import json
from pathlib import Path

folder = Path(__file__).resolve().parent
root = folder.parents[2]
context_ref = "Aprovo a pós revisar o CONTEXT.md"

def digest(data):
    return hashlib.sha256(data).hexdigest()

before = (root / "CHANGELOG.md").read_bytes()
assert digest(before) == "fdd512f84650edce0d074b9b4debef932d63ef699d23bd4c0b93391ee6fed768"
assert b"\r\n" not in before and not before.startswith(b"\xef\xbb\xbf")
entry = """## change-003 — encoding e evidência de integração local

- Os controles literais do áudio sintético em providers/_tests.py foram substituídos por escapes Python equivalentes, preservando os bytes de PCM, UTF-8 sem BOM e CRLF.
- A suíte providers executa fontes em projeto temporário, com configuração e vozes sintéticas isoladas, cleanup, timeouts e resultados PASS/FAIL/SKIP separados. Novos testes verificam encoding, isolamento e o harness real com plugins sintéticos; README documenta execução e limites.
- Validação na revisão: 55 testes unittest passaram; providers registrou 98 PASS, zero FAIL e dois SKIPs opcionais por Piper ausente. Ambiente virtual local com dependências declaradas, Python 3.15.2 AMD64; requirements.txt preservado.
- Limitações: revisão não isolada; Python além da faixa historicamente testada até 3.13. Áudio físico, UI interativa, serviços reais, crash e outras plataformas não foram validados; intenção histórica de encoding sem BOM permanece UNKNOWN. O harness e os guards de teste não são sandbox de segurança.
- Identificação mantida: **Mark LVII**, conforme PROJECT-POLICY.md. Sem nova versão, tag ou release.

Evidência técnica: .ai/changes/change-003/REVIEW.md e .ai/changes/change-003/DEVELOP.md.

""".encode("utf-8")
anchor = b"## change-002"
assert before.count(anchor) == 1
proposed = before.replace(anchor, entry + anchor, 1)
(folder / "CHANGELOG-PROPOSED.md").write_bytes(proposed)

evidence = [".ai/changes/change-003/CONTEXT.md", ".ai/changes/change-003/DEVELOP.md",
            ".ai/changes/change-003/REVIEW.md", ".ai/changes/change-003/CLOSE-EVIDENCE.md"]

def target(path, sha, refs):
    return {"path": path, "kind": "UPDATE", "change_id": "change-003", "sha256": sha, "evidence_refs": refs}

records = [
    {"id": "KR-change-003-001", "statement": "providers/_tests.py executa a suíte em cópia temporária de fontes com configuração/cache/vozes sintéticos, separa PASS/FAIL/SKIP e retorna falha quando testes ou subprocessos falham; não é sandbox de segurança.",
     "classification": "CONFIRMED", "evidence_refs": ["providers/_tests.py", "tests/test_provider_test_isolation.py", ".ai/changes/change-003/REVIEW.md"],
     "context_reference": context_ref, "traceability": {"change_id": "change-003", "requirements": ["D011", "AC3", "AC4", "AC5", "AC7"], "review": ".ai/changes/change-003/REVIEW.md"}},
    {"id": "KR-change-003-002", "statement": "Os controles literais 0x01/0x02 do áudio sintético foram substituídos por escapes equivalentes sem alterar o PCM; a política prospectiva aprovada estabelece UTF-8 sem BOM nesse arquivo e preserva CRLF.",
     "classification": "CONFIRMED", "evidence_refs": ["tests/test_source_encoding.py", ".ai/changes/change-003/ENCODING-BASELINE.json", ".ai/changes/change-003/ENCODING-REVIEW.json", ".ai/changes/change-003/REVIEW.md"],
     "context_reference": context_ref, "traceability": {"change_id": "change-003", "requirements": ["D007", "AC1", "AC2"], "review": ".ai/changes/change-003/REVIEW.md"}},
    {"id": "KR-change-003-003", "statement": "Intenção histórica de encoding sem BOM, áudio físico, UI interativa, serviços reais, recuperação de crash e outras plataformas continuam não demonstrados; evidência de change-003 limita-se a testes sintéticos locais e mantém SKIPs opcionais de Piper.",
     "classification": "UNKNOWN", "evidence_refs": [".ai/changes/change-003/CONTEXT.md", ".ai/changes/change-003/REVIEW.md", ".ai/changes/change-003/ENCODING-REVIEW.json"],
     "context_reference": context_ref, "traceability": {"change_id": "change-003", "requirements": ["D007", "D011"], "limitation": "Não promover UNKNOWN por validade UTF-8, mocks, testes locais ou decisão humana."}}
]
plan = {
    "schema_version": 1, "change_id": "change-003", "project_mode": "EXISTING", "context_reference": context_ref,
    "evidence_refs": evidence,
    "unresolved_unknowns": [
        {"description": "Intenção histórica de encoding sem BOM não estabelecida; migração prospectiva e preservação validadas.", "material": False},
        {"description": "Áudio físico, UI interativa, serviços reais, crash, outras plataformas e síntese Piper não demonstrados; fora do perfil sintético aprovado.", "material": False}],
    "unresolved_conflicts": [],
    "risks": ["NON_ISOLATED_REVIEW exposto e submetido a decisão humana explícita.", "Python 3.15.2 além da faixa historicamente testada até 3.13; prova restrita ao ambiente executado.", "Harness/guard não isolam plugins arbitrários como sandbox de segurança."],
    "material_decision_required": False, "proposed_version": None,
    "versioning": {"status": "EXISTING", "strategy": "KEEP_CURRENT_IDENTIFIER", "strategy_target": "PROJECT-POLICY.md", "evidence_refs": ["PROJECT-POLICY.md"]},
    "knowledge": {"impact": "YES", "reason": "Consolidar contratos locais de testes/encoding e preservar limites UNKNOWN no KR canônico.", "targets": [], "evidence_refs": evidence, "records": records},
    "user_docs": {"impact": "YES", "reason": "README já atualizado e revisado com execução isolada e limites; nenhuma nova edição no CLOSE.", "targets": [target("README.md", digest((root / "README.md").read_bytes()), [".ai/changes/change-003/REVIEW.md", "README.md"])], "evidence_refs": ["README.md", ".ai/changes/change-003/REVIEW.md"]},
    "changelog": {"impact": "YES", "reason": "Registrar change-003 conforme estratégia existente e alvo aprovado.", "targets": [target("CHANGELOG.md", digest(proposed), [".ai/changes/change-003/CHANGELOG-PROPOSED.md", ".ai/changes/change-003/REVIEW.md"])], "evidence_refs": ["PROJECT-POLICY.md", ".ai/changes/change-003/CHANGELOG-PROPOSED.md"], "strategy_target": "PROJECT-POLICY.md"},
    "project_spec": {"impact": "NO", "reason": "Sem requisito novo ou alvo de especificação; consolidação de D007/D011 nos limites do CONTEXT e REVIEW aprovados.", "targets": [], "evidence_refs": [".ai/changes/change-003/CONTEXT.md", ".ai/changes/change-003/REVIEW.md"], "material": False}
}
(folder / "CLOSE-PLAN.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Prepared CLOSE plan and proposed changelog; no product writes")
print("CHANGELOG proposed sha256:", digest(proposed))
