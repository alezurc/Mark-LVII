"""Isolated VS Code launch contract; no editor, models, keys or GUI required."""
import ast
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import Mock, patch


SOURCE = Path(__file__).resolve().parents[1] / 'actions' / 'dev_agent.py'
TREE = ast.parse(SOURCE.read_bytes())
NAMES = {'_vscode_launchers', '_vscode_output', '_vscode_observe', '_open_vscode',
         '_vscode_read_ready', '_vscode_capture'}


class Clock:
    def __init__(self):
        self.now = 0.0

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class VscodeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name) / 'project & special % ! spaces'
        self.folder.mkdir()
        self.clock = Clock()
        self.logs = []
        self.proc = types.SimpleNamespace(
            run=Mock(return_value=types.SimpleNamespace(returncode=0, stdout=b'', stderr=b'')),
            TimeoutExpired=subprocess.TimeoutExpired, CREATE_NO_WINDOW=0)
        self.ns = dict(Path=Path, subprocess=self.proc, sys=sys, shutil=shutil,
                       time=self.clock, BASE_DIR=SOURCE.parents[1])
        code = ast.Module(body=[n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name in NAMES], type_ignores=[])
        exec(compile(code, str(SOURCE), 'exec'), self.ns)
        self.real_launchers = self.ns['_vscode_launchers']
        self.real_observe = self.ns['_vscode_observe']
        self.real_capture = self.ns['_vscode_capture']
        self.ns['_vscode_capture'] = self.proc.run
        self.ns['_vscode_launchers'] = Mock(return_value=iter([['code']]))
        self.ns['_vscode_observe'] = Mock(return_value=False)

    def open(self):
        return self.ns['_open_vscode'](self.folder, self.logs.append)

    def assert_unverified(self):
        self.assertFalse(self.open())
        self.assertNotIn('VS Code opened:', '\n'.join(self.logs))

    def test_new_window_appears_after_poll(self):
        self.ns['_vscode_observe'].side_effect = [False, True]
        self.assertTrue(self.open())
        self.assertIn('matching project window verified', '\n'.join(self.logs))

    def test_existing_matching_window_is_accepted_after_launch(self):
        self.ns['_vscode_observe'].side_effect = lambda *a: self.proc.run.called
        self.assertTrue(self.open())
        self.proc.run.assert_called_once()

    def test_zero_exit_without_window_is_not_success(self):
        self.assert_unverified()
        self.assertLessEqual(self.clock.now, 8.0)
        self.assertIn('deadline', '\n'.join(self.logs))

    def test_path_is_a_single_uri_argument_without_shell(self):
        self.open()
        args, kwargs = self.proc.run.call_args
        self.assertEqual(args[0], ['code', '--folder-uri', self.folder.resolve().as_uri()])
        self.assertIs(kwargs['shell'], False)
        self.assertLessEqual(kwargs['timeout'], 3.0)

    def test_no_launcher(self):
        self.ns['_vscode_launchers'].return_value = iter([])
        self.assert_unverified()
        self.proc.run.assert_not_called()
        self.assertIn('not found', '\n'.join(self.logs))

    def test_start_failure(self):
        self.proc.run.side_effect = FileNotFoundError('do not publish raw exception')
        self.assert_unverified()
        self.assertIn('could not start', '\n'.join(self.logs))
        self.assertNotIn('raw exception', '\n'.join(self.logs))

    def test_exit_error_records_status_and_output_receipt(self):
        self.proc.run.return_value = types.SimpleNamespace(returncode=7, stdout=b'private project text', stderr=b'token=secret')
        self.assert_unverified()
        log = '\n'.join(self.logs)
        self.assertIn('exit code 7', log)
        self.assertIn('stdout: captured', log)
        self.assertIn('stderr: captured', log)
        self.assertNotIn('secret', log)
        self.assertNotIn('private project text', log)

    def test_launcher_timeout_records_partial_output(self):
        self.proc.run.side_effect = subprocess.TimeoutExpired('code', 3, output=b'partial', stderr=b'error')
        self.assert_unverified()
        self.assertIn('launcher timeout', '\n'.join(self.logs))
        self.assertIn('stderr: captured', '\n'.join(self.logs))

    def test_fallback_is_bounded_to_three_candidates(self):
        self.ns['_vscode_launchers'].return_value = iter([[str(i)] for i in range(8)])
        self.proc.run.side_effect = FileNotFoundError()
        self.assert_unverified()
        self.assertEqual(self.proc.run.call_count, 3)

    def test_second_candidate_can_succeed(self):
        self.ns['_vscode_launchers'].return_value = iter([['missing'], ['working']])
        self.proc.run.side_effect = [FileNotFoundError(), types.SimpleNamespace(returncode=0, stdout=b'', stderr=b'')]
        self.ns['_vscode_observe'].return_value = True
        self.assertTrue(self.open())
        self.assertIn('candidate 1 failed', '\n'.join(self.logs))

    def test_total_deadline_includes_launch_and_observation(self):
        def launch(*args, **kwargs):
            self.clock.now += kwargs['timeout']
            return types.SimpleNamespace(returncode=0, stdout=b'', stderr=b'')
        def observe(folder, timeout):
            self.clock.now += timeout
            raise subprocess.TimeoutExpired('probe', timeout)
        self.proc.run.side_effect = launch
        self.ns['_vscode_observe'].side_effect = observe
        self.assert_unverified()
        self.assertLessEqual(self.clock.now, 8.000001)

    def test_observation_permission_denied(self):
        self.ns['_vscode_observe'].side_effect = PermissionError()
        self.assert_unverified()
        self.assertIn('observation unavailable', '\n'.join(self.logs))

    def test_invalid_directory_never_launches(self):
        self.folder.rmdir()
        self.assert_unverified()
        self.proc.run.assert_not_called()

    def test_launcher_overflow_stops_without_fallback_or_window_claim(self):
        self.ns['_vscode_launchers'].return_value = iter([['first'], ['second']])
        error = OverflowError('stderr')
        error.stdout, error.stderr = b'project contents', b'token=secret'
        self.proc.run.side_effect = error
        self.assert_unverified()
        self.proc.run.assert_called_once()
        self.ns['_vscode_observe'].assert_not_called()
        logs = '\n'.join(self.logs)
        self.assertIn('stderr exceeded 65536 bytes', logs)
        self.assertIn('truncated', logs)
        self.assertNotIn('secret', logs)
        self.assertNotIn('project contents', logs)

    def test_observer_overflow_cannot_confirm_opening(self):
        error = OverflowError('stdout')
        error.stdout, error.stderr = b'x', b''
        self.ns['_vscode_observe'].side_effect = error
        self.assert_unverified()
        self.assertIn('stdout exceeded 65536 bytes', '\n'.join(self.logs))

    def test_frozen_app_does_not_spawn_itself_as_python(self):
        with patch.object(sys, 'frozen', True, create=True):
            self.assertFalse(self.real_observe(self.folder, 0.5))
        self.proc.run.assert_not_called()

    def probe(self, matches):
        # Execute the actual child payload against a fake process/window source.
        self.real_observe(self.folder, 0.5)
        argv = self.proc.run.call_args.args[0]
        fake_core = types.ModuleType('core')
        fake_core.appidentity = types.SimpleNamespace(running=Mock(return_value=matches))
        with patch.dict(sys.modules, {'core': fake_core}), patch.object(sys, 'argv', ['probe', str(self.folder)]):
            with self.assertRaises(SystemExit) as exited:
                exec(argv[2], {})
        self.assertEqual(self.proc.run.call_args.kwargs['timeout'], 0.5)
        return exited.exception.code

    def test_probe_matches_full_path_window(self):
        match = types.SimpleNamespace(name='Code.exe', titles=[f'{self.folder} — Visual Studio Code'])
        self.assertEqual(self.probe([match]), 0)

    def test_probe_rejects_other_project_and_homonymous_folder(self):
        for title in [f'{self.folder.parent / "elsewhere" / self.folder.name} — Visual Studio Code',
                      f'{self.folder.name} — Visual Studio Code', f'{self.folder}-extra — Visual Studio Code']:
            with self.subTest(title=title):
                self.assertEqual(self.probe([types.SimpleNamespace(name='Code.exe', titles=[title])]), 1)

    def test_probe_rejects_process_without_window_or_wrong_app(self):
        for match in [types.SimpleNamespace(name='Code.exe', titles=[]),
                      types.SimpleNamespace(name='other.exe', titles=[str(self.folder)])]:
            self.assertEqual(self.probe([match]), 1)

    def test_windows_cmd_wrapper_is_never_executed(self):
        home = Path(self.tmp.name) / 'VS Code'
        (home / 'bin').mkdir(parents=True)
        (home / 'resources/app/out').mkdir(parents=True)
        (home / 'Code.exe').touch()
        (home / 'resources/app/out/cli.js').touch()
        wrapper = home / 'bin/code.cmd'
        with patch.object(sys, 'platform', 'win32'), patch.object(shutil, 'which', return_value=str(wrapper)), patch.dict(os.environ, {}, clear=True):
            launchers = list(self.real_launchers())
        self.assertEqual(launchers, [[str(home / 'Code.exe'), str(home / 'resources/app/out/cli.js')]])

    def test_both_callers_report_false_result_without_open_claim(self):
        calls = []
        for fn in [n for n in TREE.body if isinstance(n, ast.FunctionDef)]:
            # Exercise the real caller statements without running unrelated code work.
            for i, node in enumerate(fn.body[:-1]):
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == '_open_vscode':
                    calls.append((node, fn.body[i + 1]))
        self.assertEqual(len(calls), 2)
        for statements in calls:
            for result in (False, True):
                logs = []
                ns = dict(_open_vscode=Mock(return_value=result), folder=self.folder, project_dir=self.folder,
                          player=None, log=logs.append, _log=lambda player, text: logs.append(text))
                exec(compile(ast.Module(body=list(statements), type_ignores=[]), str(SOURCE), 'exec'), ns)
                self.assertEqual(len(logs), 1)
                self.assertIn('verified open' if result else 'not confirmed', logs[0])
                if not result:
                    self.assertNotIn('verified open', logs[0])


class CaptureTests(unittest.TestCase):
    """Real, bounded local Python producers; never run VS Code or a model."""
    def setUp(self):
        self.ns = dict(Path=Path, subprocess=subprocess, sys=sys, shutil=shutil,
                       time=time, BASE_DIR=SOURCE.parents[1])
        code = ast.Module(body=[n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name in NAMES], type_ignores=[])
        exec(compile(code, str(SOURCE), 'exec'), self.ns)
        self.children = []
        self.requests = []
        self.read = self.ns['_vscode_read_ready']

        def read(stream, size):
            self.assertGreater(size, 0)
            self.assertLessEqual(size, 8192)
            chunk = self.read(stream, size)
            if chunk:
                self.assertLessEqual(len(chunk), size)
            self.requests.append(size)
            return chunk
        self.ns['_vscode_read_ready'] = read

    def run_capture(self, script, timeout=3):
        original = subprocess.Popen
        def launch(*args, **kwargs):
            self.assertIs(kwargs['stdout'], subprocess.PIPE)
            self.assertIs(kwargs['stderr'], subprocess.PIPE)
            self.assertFalse(kwargs.get('shell'))
            proc = original(*args, **kwargs)
            self.children.append(proc)
            return proc
        with patch.object(subprocess, 'Popen', side_effect=launch):
            try:
                return self.ns['_vscode_capture'](
                    [sys.executable, '-B', '-c', script], timeout,
                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            finally:
                for proc in self.children:
                    # Cleanup is asserted, not silently repaired by the test.
                    self.assertIsNotNone(proc.poll())
                    self.assertTrue(proc.stdout.closed)
                    self.assertTrue(proc.stderr.closed)

    def test_each_stream_below_and_exact_limit(self):
        for fd in (1, 2):
            for size in (0, 65535, 65536):
                with self.subTest(fd=fd, size=size):
                    result = self.run_capture(f'import os; os.write({fd}, b"x" * {size})')
                    self.assertEqual(result.returncode, 0)
                    data = result.stdout if fd == 1 else result.stderr
                    other = result.stderr if fd == 1 else result.stdout
                    self.assertEqual(len(data), size)
                    self.assertEqual(len(other), 0)
                    self.assertIsInstance(data, memoryview)
                    self.assertEqual(len(data.obj), 65536)  # actual backing storage
        self.assertLessEqual(max(self.requests), 8192)

    def test_first_excess_byte_is_detected_on_each_stream(self):
        for fd, name in ((1, 'stdout'), (2, 'stderr')):
            with self.subTest(fd=fd):
                with self.assertRaises(OverflowError) as caught:
                    self.run_capture(f'import os; os.write({fd}, b"x" * 65537)')
                self.assertEqual(str(caught.exception), name)
                self.assertEqual(len(getattr(caught.exception, name)), 65536)
                for value in (caught.exception.stdout, caught.exception.stderr):
                    self.assertLessEqual(len(value), 65536)
                    self.assertEqual(len(value.obj), 65536)
        self.assertIn(1, self.requests)  # read one extra byte, not an unbounded read

    def test_both_streams_at_limit_without_deadlock(self):
        script = ('import os\n'
                  'for i in range(8):\n'
                  ' os.write(1, b"a"*8192)\n'
                  ' os.write(2, b"b"*8192)\n')
        result = self.run_capture(script)
        self.assertEqual(len(result.stdout), 65536)
        self.assertEqual(len(result.stderr), 65536)
        self.assertEqual(result.returncode, 0)

    def test_continuous_excess_is_stopped_and_reaped(self):
        script = ('import os\nwhile True:\n'
                  ' os.write(1, b"a"*8192)\n'
                  ' os.write(2, b"b"*8192)\n')
        started = time.monotonic()
        with self.assertRaises(OverflowError):
            self.run_capture(script)
        self.assertLess(time.monotonic() - started, 3.5)

    def test_silence_timeout_has_no_reader_threads(self):
        import threading
        before = set(threading.enumerate())
        started = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            self.run_capture('import time; time.sleep(10)', timeout=0.6)
        self.assertLess(time.monotonic() - started, 1.5)
        self.assertEqual(set(threading.enumerate()), before)

    def test_one_stream_closes_while_other_continues(self):
        result = self.run_capture('import os; os.close(1); os.write(2, b"ok")')
        self.assertEqual(result.stdout, b'')
        self.assertEqual(result.stderr, b'ok')

    def test_missing_executable_does_not_create_a_reader(self):
        with patch.object(subprocess, 'Popen', side_effect=FileNotFoundError()):
            with self.assertRaises(FileNotFoundError):
                self.ns['_vscode_capture'](['missing'], 1)

    def test_no_communicate_or_full_output_capture(self):
        capture = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == '_vscode_capture')
        for node in ast.walk(capture):
            if isinstance(node, ast.Call):
                self.assertFalse(isinstance(node.func, ast.Attribute) and node.func.attr in ('communicate', 'run'))
                self.assertNotIn('capture_output', [kw.arg for kw in node.keywords])


if __name__ == '__main__':
    unittest.main(verbosity=2)
