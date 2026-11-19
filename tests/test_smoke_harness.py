"""Real harness, real loader, synthetic plugins only; no application session."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "core" / "_smoke_harness.py"


def run_report(root, spec, timeout=20):
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", PYTHONUTF8="1",
               PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(root))
    result = subprocess.run([sys.executable, str(HARNESS), str(root), json.dumps(spec)],
                            cwd=root, env=env, capture_output=True, text=True,
                            encoding="utf-8", timeout=timeout,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    if result.returncode:
        raise AssertionError(f"Harness exited {result.returncode}: {result.stdout}\n{result.stderr}")
    lines = [line[len("@@REPORT@@"):] for line in result.stdout.splitlines()
             if line.startswith("@@REPORT@@")]
    if len(lines) != 1:
        raise AssertionError(f"Expected one report: {result.stdout}\n{result.stderr}")
    try:
        report = json.loads(lines[0])
    except ValueError as exc:
        raise AssertionError(f"Malformed report: {result.stdout}") from exc
    if not isinstance(report, dict) or not isinstance(report.get("imports"), dict) or not isinstance(report.get("plugins"), dict):
        raise AssertionError("Malformed report structure")
    return report


class SmokeHarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="jarvis-smoke-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for package in ("core", "memory", "plugins"):
            (self.root / package).mkdir()
            (self.root / package / "__init__.py").write_text("", encoding="utf-8")
        for relative in ("core/plugin_loader.py", "core/gemini.py", "memory/config_manager.py"):
            shutil.copyfile(REPO / relative, self.root / relative)

    def write(self, relative, text):
        (self.root / relative).write_text(text, encoding="utf-8")

    def plugin(self, name, body):
        self.write(f"plugins/{name}.py",
                   f"PLUGIN = {{'name': '{name}', 'description': 'synthetic fixture', "
                   "'parameters': {'type': 'OBJECT', 'properties': {}}}\n" + body)

    def test_import_and_plugin_results(self):
        self.write("good.py", "VALUE = 1\n")
        self.write("bad.py", "raise RuntimeError('synthetic import failure')\n")
        self.plugin("worker", """import json, threading
def run(parameters, player=None, session_memory=None):
    if player is not None:
        player.write_log('synthetic call')
    return json.dumps({'worker': threading.current_thread() is not threading.main_thread(),
                       'none': player is None})
""")
        self.plugin("raises", "def run(parameters, player=None):\n    raise ValueError('synthetic run failure')\n")
        self.write("plugins/invalid.py", "PLUGIN = {}\n")
        report = run_report(self.root, {"imports": ["good", "bad"],
                            "plugins": ["plugins/worker.py", "plugins/raises.py", "plugins/invalid.py"]})
        self.assertEqual(report["imports"]["good"], "")
        self.assertIn("synthetic import failure", report["imports"]["bad"])
        worker = report["plugins"]["plugins/worker.py"]
        self.assertEqual(worker["error"], "")
        self.assertEqual(json.loads(worker["returned"]), {"worker": True, "none": False})
        self.assertIn("write_log", worker["calls"])
        self.assertIn("synthetic run failure", report["plugins"]["plugins/raises.py"]["error"])
        self.assertIn("rejects", report["plugins"]["plugins/invalid.py"]["error"])

        # The same real loader with player=None; no discovery or real plugins.
        self.write("none_check.py", """import importlib.util, json
from core.plugin_loader import _call_run
spec = importlib.util.spec_from_file_location('synthetic', 'plugins/worker.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
assert json.loads(_call_run(mod.run, {}, None, None))['none'] is True
""")
        self.assertEqual(run_report(self.root, {"imports": ["none_check"]})["imports"]["none_check"], "")

    @unittest.skipUnless(importlib.util.find_spec("PyQt6"), "PyQt6 unavailable: Qt profile not demonstrated")
    def test_jarvis_profile_qt_and_stubbed_model(self):
        self.write("qt_check.py", """import threading
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication
from core import gemini
app = QApplication.instance()
assert app is not None
assert app.thread() == QThread.currentThread()
assert threading.current_thread() is threading.main_thread()
assert gemini.as_json('synthetic') is None
assert gemini.text('synthetic') == ''
""")
        report = run_report(self.root, {"profile": "jarvis", "imports": ["qt_check"]})
        self.assertEqual(report["imports"]["qt_check"], "")

    def test_missing_malformed_and_nonzero_reports_fail(self):
        for code, stdout in ((0, ""), (0, "@@REPORT@@not-json"), (0, "@@REPORT@@[]"), (2, "@@REPORT@@{}")):
            with self.subTest(code=code, stdout=stdout), patch.object(subprocess, "run", return_value=
                    subprocess.CompletedProcess([], code, stdout, "synthetic stderr")):
                with self.assertRaises(AssertionError):
                    run_report(self.root, {})

    def test_timeout_is_not_success(self):
        self.write("slow.py", "import time\ntime.sleep(30)\n")
        with self.assertRaises(subprocess.TimeoutExpired):
            run_report(self.root, {"imports": ["slow"]}, timeout=0.5)


if __name__ == "__main__":
    unittest.main()
