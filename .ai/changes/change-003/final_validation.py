"""Local evidence only: no product imports or personal configuration reads."""
import ast
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import sys
from pip._vendor.packaging.requirements import Requirement

root = Path(__file__).resolve().parents[3]
evidence = Path(__file__).resolve().parent
assert sys.prefix != sys.base_prefix, "Validation requires the local virtual environment"
assert Path(sys.prefix).resolve() == (root / ".venv").resolve()
assert "include-system-site-packages = false" in (root / ".venv" / "pyvenv.cfg").read_text()

versions = {}
for raw in (root / "requirements.txt").read_text(encoding="utf-8").splitlines():
    line = raw.split("#", 1)[0].strip()
    if not line:
        continue
    requirement = Requirement(line)
    if requirement.marker and not requirement.marker.evaluate():
        continue
    try:
        version = metadata.version(requirement.name)
    except metadata.PackageNotFoundError:
        continue  # The validation environment deliberately isn't a full app install.
    assert requirement.specifier.contains(version), (requirement.name, version, str(requirement.specifier))
    versions[requirement.name] = version

previous = json.loads((evidence / "IMPLEMENTATION-EVIDENCE.json").read_text(encoding="utf-8"))
entries = []
for entry in previous["entries"]:
    path = entry["path"]
    if path.startswith(".ai/"):
        continue
    data = (root / path).read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], f"Changed since paused DEVELOP: {path}"
    data.decode("utf-8", errors="strict")
    assert not data.startswith(b"\xef\xbb\xbf"), path
    assert not any(b < 32 and b not in (9, 10, 13) for b in data), path
    if path in ("providers/_tests.py", "README.md"):
        assert b"\n" not in data.replace(b"\r\n", b""), path
    else:
        assert b"\r\n" not in data, path
    if path.endswith(".py"):
        ast.parse(data, filename=path)
    entries.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(),
                    "encoding": "utf-8", "bom": "NONE", "unchanged_since_pause": True})

result = {"change_id": "change-003", "python": sys.version, "executable": sys.executable,
          "virtual_environment": sys.prefix, "system_site_packages": False,
          "installed_project_requirements_checked": versions, "entries": entries,
          "requirements_sha256": hashlib.sha256((root / "requirements.txt").read_bytes()).hexdigest()}
for name in ("providers-resumed.log", "unittest-resumed.log", "venv-packages.json", "RESUMPTION-DEP-001.md"):
    result.setdefault("evidence_hashes", {})[name] = hashlib.sha256((evidence / name).read_bytes()).hexdigest()
(evidence / "FINAL-VALIDATION.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
