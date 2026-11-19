"""Static inventory and compared discovery; no product imports or writes."""
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
out = root / ".ai"
run = "discovery-2026-11-18-02"
run_dir = out / "discovery-runs" / run
runtime = Path(sys.argv[1])
prior_bytes = (out / "DISCOVERY.md").read_bytes()
match = re.search(r"## finding_registry\s+```json\s*(.*?)\s*```", prior_bytes.decode("utf-8"), re.S)
if not match:
    raise SystemExit("Invalid canonical baseline; refusing publication")
baseline = json.loads(match.group(1))
if not re.fullmatch(r"discovery-[\w-]+", baseline["run_id"]) or baseline["run_id"] == run:
    raise SystemExit("Invalid/reused run id")
if baseline["project_scope"] != "Mark-LVII / whole-project static discovery":
    raise SystemExit("Incomparable scope")
history = out / "discovery-history" / baseline["run_id"]
history.mkdir(parents=True, exist_ok=True)

def preserve(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise SystemExit("Historical snapshot conflict: " + str(path))
    else:
        path.write_bytes(data)

preserve(history / "DISCOVERY.md", prior_bytes)
preserve(history / "DISCOVERY-REGISTRY.json", (json.dumps(baseline, ensure_ascii=False, indent=2) + "\n").encode())
preserve(history / "DISCOVERY-EVIDENCE.json", (out / "DISCOVERY-EVIDENCE.json").read_bytes())
old = json.loads((history / "DISCOVERY-EVIDENCE.json").read_text(encoding="utf-8"))
old_entries = {e["path"]: e for e in old["entries"]}
excluded = {".git", ".ai", ".ai-sdd", ".codex", "__pycache__", "config", "reports", ".venv", "venv", "env", "node_modules", "build", "dist"}
root_names = {"agents.md", "readme.md", "requirements.txt", "ai-sdd.project.yaml", ".gitignore", "project-policy.md", "changelog.md"}
paths = []
for base, dirs, files in os.walk(root):
    folder = Path(base)
    dirs[:] = [d for d in dirs if d.lower() not in excluded and not (folder == root / "memory" and d == "tasks")
               and not (folder / d).is_symlink() and not (folder / d).is_junction()]
    for name in files:
        path = folder / name
        if path.suffix == ".py" or path.parent == root and name.lower() in root_names or path.parent == root / "agents" and path.suffix == ".md":
            if path.is_symlink() or path.is_junction():
                raise SystemExit("Linked inventory target")
            paths.append(path)
entries, errors = [], []
for path in sorted(paths):
    data = path.read_bytes()
    relative = path.relative_to(root).as_posix()
    bom, encoding = "NONE", "utf-8"
    for prefix, marker, codec in ((b"\xff\xfe\x00\x00", "UTF-32-LE", "utf-32"), (b"\x00\x00\xfe\xff", "UTF-32-BE", "utf-32"),
                                  (b"\xef\xbb\xbf", "UTF-8", "utf-8-sig"), (b"\xff\xfe", "UTF-16-LE", "utf-16"), (b"\xfe\xff", "UTF-16-BE", "utf-16")):
        if data.startswith(prefix):
            bom, encoding = marker, codec
            break
    try:
        text = data.decode(encoding, errors="strict")
        controls = [ord(c) for c in text if ord(c) < 32 and c not in "\t\r\n\f"]
        status = "UNKNOWN" if controls else "TEXT"
    except UnicodeError:
        text, controls, status, encoding = "", [], "UNKNOWN", None
    entries.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "status": status,
                    "encoding": encoding if status == "TEXT" else "UNKNOWN", "bom": bom,
                    "method": "BOM signature/strict payload; strict UTF-8 without BOM; conservative control scan",
                    "confidence": "VALID_BYTES_ONLY" if status == "TEXT" else "UNKNOWN",
                    "unexpected_controls": controls,
                    "limitation": "Bytes do not establish historical intent/codepage; not an approved edit baseline."})
    if path.suffix == ".py":
        try:
            ast.parse(data, filename=relative)
        except (SyntaxError, UnicodeError) as exc:
            errors.append({"path": relative, "error": str(exc)})
current_entries = {e["path"]: e for e in entries}
changed = [p for p, e in old_entries.items() if p not in current_entries or e["sha256"] != current_entries[p]["sha256"]]
added = sorted(set(current_entries) - set(old_entries))
revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
tracked = subprocess.check_output(["git", "ls-files", "memory/tasks", "reports"], cwd=root, text=True).splitlines()
run_dir.mkdir(parents=True, exist_ok=True)
evidence = {"run_id": run, "revision": revision, "entries": entries, "syntax_errors": errors,
            "changed_since_baseline": changed, "added_to_inventory": added,
            "tracked_runtime_artifact_count": len(tracked),
            "limits": "Static only. No personal data, dependencies/venv contents, product imports, test execution, models/services or GUI in this DISCOVERY."}
(run_dir / "EVIDENCE.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if "--publish" not in sys.argv:
    print(json.dumps({"run": run, "files": len(entries), "python_files": sum(p.suffix == '.py' for p in paths),
                      "changed": changed, "added": added, "syntax_errors": errors,
                      "unknown_encoding": [e['path'] for e in entries if e['status'] == 'UNKNOWN']}, ensure_ascii=False))
    raise SystemExit(0)

findings = []
for previous in baseline["findings"]:
    row = {key: copy.deepcopy(previous[key]) for key in
           ("subject", "classification", "evidence", "description", "implication", "material")}
    if "treatment_status" in previous:
        row["treatment_status"] = previous["treatment_status"]
    refs = []
    for reference in row["evidence"]:
        location = reference.split(" @ ")[0]
        path = re.sub(r":\d+$", "", location)
        if path in current_entries:
            refs.append(location + " @ working-tree sha256:" + current_entries[path]["sha256"])
        elif "tracked_runtime_artifact_count=" in reference:
            refs.append(f".ai/discovery-runs/{run}/EVIDENCE.json / tracked_runtime_artifact_count={len(tracked)}")
        else:
            refs.append(reference)
    row["evidence"] = refs
    if previous["id"] == "D007":
        row.update(
            description="Mudança material de evidência após change-003 CLOSED: os controles literais U+0001/U+0002 de providers/_tests.py foram substituídos por escapes equivalentes, com PCM preservado e política prospectiva UTF-8 sem BOM. O inventário atual não contém arquivo com status de bytes UNKNOWN; intenção histórica sem BOM continua UNKNOWN.",
            implication="O problema localizado dos controles foi tratado; não inferir intenção histórica/codepage a partir de UTF-8 válido. Futuras edições continuam exigindo SCOPE e política de encoding quando necessária. Não converter UNKNOWN histórico em CONFIRMED.",
            evidence=["providers/_tests.py", "tests/test_source_encoding.py", ".ai/changes/change-003/ENCODING-REVIEW.json", ".ai/changes/change-003/REVIEW.md", ".ai/knowledge/KNOWLEDGE-REGISTER.json", f".ai/discovery-runs/{run}/EVIDENCE.json"],
            treatment_status="PARTIALLY_RESOLVED")
    elif previous["id"] == "D008":
        row.update(
            classification="CONFIRMED",
            description="Mudança material após change-002 CLOSED: memória e sessões publicam JSON completo por temporário exclusivo e os.replace após fechamento; RLock cobre mutadores internos read-modify-write. A revisão documenta 13 testes focais; change-003 reexecutou essas regressões entre os 55 unittest PASS.",
            implication="Risco original de truncamento por escrita direta tratado no escopo local; durabilidade física, processos concorrentes e recuperação de corrupção anterior continuam fora da garantia. Não inferir proteção universal de filesystem/crash.",
            evidence=["memory/memory_manager.py:120", "memory/memory_manager.py:178", "memory/memory_manager.py:433", "memory/memory_manager.py:453", "memory/memory_manager.py:475", "tests/test_memory_persistence.py", ".ai/changes/change-002/REVIEW.md", ".ai/changes/change-002/AI-SDD-CLOSE.json", ".ai/changes/change-003/REVIEW.md"],
            treatment_status="RESOLVED_FOR_APPROVED_SCOPE")
    elif previous["id"] == "D011":
        row.update(
            description="Mudança material após changes 002/003: evidência revisada de 55 unittest PASS e providers com 98 PASS, zero FAIL, dois SKIPs opcionais de Piper. Há integração sintética local com types.Blob/TaskGroup, streaming HTTP loopback, resampling, painel Qt offscreen e harness com plugins sintéticos. Esses resultados foram documentados nas revisões fechadas, não reexecutados neste DISCOVERY.",
            implication="Cobertura local ampliada e testes isolados; áudio físico, UI interativa, serviços reais, crash e outras plataformas permanecem UNKNOWN. NON_ISOLATED_REVIEW e Python 3.15.2 além da faixa historicamente testada até 3.13 foram explicitados. Não afirmar validação integrada universal nem contar SKIP como PASS.",
            evidence=["providers/_tests.py", "core/_smoke_harness.py", "tests/test_provider_test_isolation.py", "tests/test_smoke_harness.py", "tests/test_memory_persistence.py", ".ai/changes/change-003/REVIEW.md", ".ai/changes/change-003/REVIEW-EVIDENCE.json", ".ai/changes/change-003/AI-SDD-CLOSE.json"],
            treatment_status="PARTIALLY_RESOLVED")
    elif previous["id"] == "D013":
        row.update(
            description="Mudança material de governança: changes 001, 002 e 003 encerradas pelo runtime, com auditorias e sete registros no Knowledge Register canônico, mantendo CONFIRMED e UNKNOWN separados. A preparação de ambiente da change-003 teve parada e retomada humana delimitada preservadas.",
            implication="Reutilizar evidência duradoura de VS Code, persistência e testes/encoding sem promover UNKNOWN ou apagar histórico. O projeto está sem change ativa e sem autorização de desenvolvimento; DISCOVERY não aprova novo contexto.",
            evidence=[".ai/changes/change-001/AI-SDD-CLOSE.json", ".ai/changes/change-002/AI-SDD-CLOSE.json", ".ai/changes/change-003/AI-SDD-CLOSE.json", ".ai/changes/change-003/BOUNDARY-STOP-DEP-001.md", ".ai/changes/change-003/RESUMPTION-DEP-001.md", ".ai/knowledge/KNOWLEDGE-REGISTER.json", ".ai/AI-SDD.yaml"])
    if previous["id"] in {"D007", "D008", "D011", "D013"}:
        row["material"] = row["description"] + " " + row["implication"]
    findings.append(row)

# Preserve hashes/provenance for every explicitly cited local artifact.
governance_paths = sorted({ref for row in findings for ref in row["evidence"]
                           if ref.startswith(".ai/") and " / " not in ref and ref != f".ai/discovery-runs/{run}/EVIDENCE.json"})
evidence["governance_evidence"] = [{"path": path, "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest()}
                                   for path in governance_paths]
(run_dir / "EVIDENCE.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
current = {"run_id": run, "project_scope": baseline["project_scope"],
           "baseline": {"source": (history / "DISCOVERY.md").relative_to(root).as_posix(),
                        "sha256": hashlib.sha256(prior_bytes).hexdigest(), "run_id": baseline["run_id"],
                        "revision": old["revision"], "project_scope": baseline["project_scope"]},
           "findings": findings}
input_path = run_dir / "CURRENT.json"
input_path.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
result = subprocess.run([sys.executable, "-B", str(runtime / "scripts/discovery_findings.py"), str(input_path),
                         str(history / "DISCOVERY-REGISTRY.json")], capture_output=True, text=True, encoding="utf-8",
                        env=dict(os.environ, PYTHONIOENCODING="utf-8"), timeout=20, check=True)
registry = json.loads(result.stdout)
if any(f["comparison_status"] == "AMBIGUOUS" for f in registry["findings"]):
    raise SystemExit("Unresolved ambiguity; refusing publication")
sys.path.insert(0, str(runtime / "scripts"))
import discovery_findings as helper
helper.validate(registry["findings"], historical=True)
table = helper.render(registry)
report = f'''# Discovery — Mark-LVII — comparação após change-003

Execução: {run}. Escopo: {registry['project_scope']}. Revisão Git: `{revision}`; modificações locais identificadas por SHA-256, sem atribuí-las ao commit. Modo COMPARED. Baseline canônica anterior preservada integralmente em `{current['baseline']['source']}`, SHA-256 `{current['baseline']['sha256']}`. IDs e subjects mantidos por equivalência semântica, sem renumeração ou reciclagem.

## Método e arquitetura

Inspeção estática de {len(entries)} arquivos e parsing AST de {sum(p.suffix == '.py' for p in paths)} fontes Python: {len(errors)} erros. Arquivos alterados desde a baseline: {', '.join(changed)}. Adicionados ao inventário: {', '.join(added)}. Demais bytes reconfirmam as observações estáticas anteriores; módulos alterados, novos testes, políticas, auditorias de CLOSE e KR foram consultados nesta execução. O cotejo profundo usa evidência preservada e leitura focal de mudanças, sem repetir execução do produto. Inventário, hashes e proveniência em `.ai/discovery-runs/{run}/EVIDENCE.json`.

Mantidos os contratos: asyncio da voz em thread dedicado, QApplication/GUI no principal, ferramentas em workers e sinais de JarvisUI; TaskEngine para trabalho longo; loaders com contratos TOOL/PLUGIN; core.gemini para deadlines/fallback; settings por config_manager. Memória agora publica snapshots completos por temporário/replace e serializa mutadores internos com RLock. Providers self-test executa fontes e dados sintéticos em projeto temporário. Não se deduz eficácia universal de controles estáticos.

Caches, .venv/dependências, segredos/configuração pessoal, conteúdo de memória, checkpoints, relatórios pessoais e mídia foram excluídos. Metadados do índice Git confirmam {len(tracked)} artefatos runtime versionados, sem ler seu conteúdo. Não houve imports do produto, execução de testes/aplicação, instalação, modelos/serviços ou pesquisa externa neste DISCOVERY. Resultados de testes citados abaixo são evidência documental das revisões fechadas, com hashes, e não execuções novas. AST não demonstra comportamento.

## Findings e reconciliação

D007, D008, D011 e D013 mudam de material/evidência, com antes/depois preservado pelo auxiliar oficial. D008 passa de risco INFERRED para controles observados CONFIRMED, tratado somente no escopo aprovado. D007 e D011 permanecem UNKNOWN quanto à intenção histórica e integração real; seus tratamentos localizados não apagam essas lacunas. D006 conserva o tratamento anterior. Não foram alocados novos IDs; não há identidade ambígua pendente.

{table}

## Encoding e conhecimento duradouro

Todos os arquivos inventariados decodificam estritamente no perfil textual detectado; nenhum tem status de bytes UNKNOWN nesta execução. A remoção focal dos controles em providers/_tests.py foi aprovada na change-003, com PCM equivalente e UTF-8 sem BOM prospectivo. Ausência de BOM continua sem provar intenção histórica/codepage: D007 e KR UNKNOWN permanecem. Inventário de DISCOVERY não é baseline de edição aprovada; CONTEXT futuro exige caminhos exatos e política apropriada antes da aprovação.

Sete registros KR preservam fatos e limites das três changes; não foi criado segundo registro nem alterado o KR. Testes documentados: change-003 REVIEW com 55 unittest PASS e providers 98 PASS/0 FAIL/2 SKIP opcionais de Piper; NON_ISOLATED_REVIEW, Python 3.15.2 e limites reais foram explicitados e submetidos a decisão humana. Não transformar decisão/validade dos bytes em prova ausente.

## Lacunas e continuidade

D005 (requisito de transporte/TLS e exposição real do dashboard), D010 (política para artefatos runtime versionados) e D012 (limitação documentada de DNS rebinding) permanecem observações para eventual contexto específico. D007 mantém intenção histórica UNKNOWN; D011 mantém áudio físico, UI interativa, serviços reais, crash e outras plataformas UNKNOWN. D008 não promete durabilidade física, locks entre processos, merge de snapshots ou recuperação anterior. Nenhuma dessas lacunas autoriza testes externos ou implementação automática.

DEP-001 da change-003 foi parado, reaberto por autorização humana delimitada e validado no ambiente preparado; o original e a retomada foram preservados. Esta inspeção não reabre esse ramo nem encontra dependência externa material para seu objetivo estático; nenhuma nova Boundary Stop foi acionada. Estado observado no início: CLOSED, última change change-003, sem change ativa e develop_authorized=false. Não executar CONTEXT automaticamente.

## finding_registry

```json
{json.dumps(registry, ensure_ascii=False, indent=2)}
```
'''
if (out / "DISCOVERY.md").read_bytes() != prior_bytes:
    raise SystemExit("Concurrent canonical report change")
for entry in entries + evidence["governance_evidence"]:
    if hashlib.sha256((root / entry["path"]).read_bytes()).hexdigest() != entry["sha256"]:
        raise SystemExit("Evidence changed before publication: " + entry["path"])
for name, data in (("DISCOVERY-CURRENT.json", current), ("DISCOVERY-REGISTRY.json", registry), ("DISCOVERY-EVIDENCE.json", evidence)):
    (out / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "DISCOVERY.md").write_text(report, encoding="utf-8")
print(json.dumps({"run": run, "files": len(entries), "findings": len(registry["findings"]),
                  "comparisons": {s: sum(f['comparison_status'] == s for f in registry['findings'])
                                  for s in ("SAME_FINDING", "CHANGED", "NEW", "NOT_RECONFIRMED", "AMBIGUOUS")}}, ensure_ascii=False))
