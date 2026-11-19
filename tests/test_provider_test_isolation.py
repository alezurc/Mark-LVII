"""Exercise isolation failures without opening personal settings or voice data."""
import asyncio
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("provider_selftests", REPO / "providers" / "_tests.py")
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


class IsolationTests(unittest.TestCase):
    def run_code(self, root, env, code):
        result = subprocess.run([sys.executable, "-c", code], cwd=root, env=env,
                                capture_output=True, text=True, encoding="utf-8", timeout=40,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        self.assertEqual(result.returncode, 0, result.stdout + "\n" + result.stderr)
        return result.stdout

    def test_only_sources_copied_and_cleanup_after_failure(self):
        real_read = Path.read_bytes

        def guarded_read(path):
            self.assertNotEqual(path, REPO / "config" / "api_keys.json")
            return real_read(path)

        root = None
        with patch.object(Path, "read_bytes", guarded_read):
            with self.assertRaisesRegex(RuntimeError, "injected"):
                with suite.isolated_project() as (root, env):
                    self.assertFalse((root / "config").exists())
                    self.assertFalse((root / "providers" / "voices").exists())
                    self.assertFalse((root / "memory" / "long_term.json").exists())
                    self.assertTrue((root / "memory" / "config_manager.py").is_file())
                    self.assertEqual(env["QT_QPA_PLATFORM"], "offscreen")
                    raise RuntimeError("injected")
        self.assertFalse(root.exists())

    def test_failure_skip_and_reentry_counts(self):
        def failure():
            suite.check("synthetic failing assertion", False)

        def skipped():
            suite.skip("optional fixture", "synthetic missing dependency")

        def crashed():
            raise RuntimeError("synthetic exception")

        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(asyncio.run(suite._run_tests([failure, skipped, crashed])), 1)
            self.assertEqual((suite._ok, suite._fail, suite._skip), (0, 2, 1))
            self.assertEqual(asyncio.run(suite._run_tests([skipped])), 0)
            self.assertEqual((suite._ok, suite._fail, suite._skip), (0, 0, 1))
        self.assertIn("0 passed, 2 failed, 1 skipped", output.getvalue())

    def test_runner_propagates_exit_and_cleans_after_timeout(self):
        roots = []

        def child(*args, **kwargs):
            roots.append(Path(kwargs["cwd"]))
            self.assertTrue(roots[-1].exists())
            return subprocess.CompletedProcess(args[0], 7, "synthetic output\n", "synthetic error\n")

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with patch.object(suite.subprocess, "run", side_effect=child):
                self.assertEqual(asyncio.run(suite.main()), 7)
            self.assertFalse(roots[-1].exists())

            def timeout(*args, **kwargs):
                roots.append(Path(kwargs["cwd"]))
                raise subprocess.TimeoutExpired(args[0], 180)

            with patch.object(suite.subprocess, "run", side_effect=timeout):
                self.assertEqual(asyncio.run(suite.main()), 1)
            self.assertFalse(roots[-1].exists())

    def test_voice_patches_restore_after_exception_and_import_is_temporary(self):
        with suite.isolated_project() as (root, env):
            self.run_code(root, env, """from pathlib import Path
from providers import _tests as t
root = Path.cwd()
violations = t.install_child_guard(root)
from providers import tts_piper as p
original = (p._VOICE_DIR, p.download, p.PiperTTS._synth)
assert p._VOICE_DIR.is_relative_to(root)
folder = None
try:
    with t.synthetic_voices():
        folder = p._VOICE_DIR
        assert folder.is_relative_to(root)
        assert set(p.installed()) == {'en_US-lessac-medium', 'tr_TR-dfki-medium'}
        try:
            p.download('forbidden')
        except AssertionError:
            pass
        else:
            raise AssertionError('download was not blocked')
        raise RuntimeError('injected voice failure')
except RuntimeError:
    pass
assert (p._VOICE_DIR, p.download, p.PiperTTS._synth) == original
assert folder is not None and not folder.exists()
assert not violations, violations
""")

    @unittest.skipUnless(importlib.util.find_spec("PyQt6"), "PyQt6 unavailable: panel failure path not demonstrated")
    def test_panel_failure_restores_config_without_accessing_real_path(self):
        with suite.isolated_project() as (root, env):
            self.run_code(root, env, """from pathlib import Path
from unittest.mock import patch
from providers import _tests as t
from memory import config_manager as cm
violations = t.install_child_guard(Path.cwd())
with t.synthetic_voices():
    import ui
    original = (cm.CONFIG_DIR, cm.CONFIG_FILE)
    original_open = Path.open
    def guard(path, *args, **kwargs):
        if path == original[1]:
            raise AssertionError('unredirected config access')
        return original_open(path, *args, **kwargs)
    with patch.object(Path, 'open', guard), patch.object(ui, 'ProvidersOverlay',
            side_effect=RuntimeError('injected panel failure')):
        try:
            t.test_panel_settings_survive()
        except RuntimeError as exc:
            assert str(exc) == 'injected panel failure'
        else:
            raise AssertionError('injection did not run')
    assert (cm.CONFIG_DIR, cm.CONFIG_FILE) == original
    assert not cm.CONFIG_FILE.exists()
assert not violations, violations
""")

    def test_child_guard_rejects_external_connections_and_escaped_writes(self):
        with suite.isolated_project() as (root, env):
            self.run_code(root, env, """from pathlib import Path
import socket
from providers import _tests as t
violations = t.install_child_guard(Path.cwd())
try:
    (Path.cwd().parent / 'must-not-create-jarvis-test.txt').write_text('forbidden')
except RuntimeError:
    pass
else:
    raise AssertionError('escaped write allowed')
with socket.socket() as s:
    try:
        s.connect(('192.0.2.1', 80))
    except RuntimeError:
        pass
    else:
        raise AssertionError('external connection allowed')
assert len(violations) == 2, violations
""")


if __name__ == "__main__":
    unittest.main()
