"""Persistence contracts using synthetic memory only; no app or service imports."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch


SOURCE = Path(__file__).resolve().parents[1] / 'memory' / 'memory_manager.py'
spec = importlib.util.spec_from_file_location('isolated_memory', SOURCE)
mm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mm)  # Module defines functions; it performs no memory I/O.


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'nested' / 'memory.json'
        self.redirect = patch.object(mm, 'MEMORY_PATH', self.path)
        self.redirect.start()
        self.addCleanup(self.redirect.stop)
        self.output = patch('sys.stdout', new_callable=io.StringIO)
        self.output.start()
        self.addCleanup(self.output.stop)

    def seed(self):
        mm.save_memory({'notes': {'legacy': 'ação 東京'}, 'extra': [1],
                        'sessions': [{'summary': 'first'}, {'summary': 'last'}]})
        return self.path.read_bytes()

    def assert_clean(self):
        self.assertEqual(list(self.path.parent.glob('*.tmp')), [])

    def test_roundtrip_and_missing(self):
        self.assertEqual(mm.load_memory(), mm._empty_memory())
        self.assertIsNone(mm.pop_last_session())
        self.seed()
        result = mm.load_memory()
        self.assertEqual(result['notes']['legacy'], 'ação 東京')
        self.assertEqual(result['extra'], [1])
        self.assertIn('identity', result)
        self.assertFalse(self.path.read_bytes().startswith(b'\xef\xbb\xbf'))
        self.assertIn('ação 東京', self.path.read_text(encoding='utf-8'))
        self.assert_clean()

    def test_serialization_failure_preserves_bytes(self):
        before = self.seed()
        with self.assertRaises(TypeError):
            mm.save_memory({'unserializable': object()})
        self.assertEqual(self.path.read_bytes(), before)
        self.assert_clean()

    def test_creation_failure_preserves_bytes(self):
        before = self.seed()
        with patch.object(mm.tempfile, 'NamedTemporaryFile', side_effect=OSError('create')):
            with self.assertRaises(OSError):
                mm.save_memory({'new': 1})
        self.assertEqual(self.path.read_bytes(), before)
        self.assert_clean()

    def test_partial_write_and_close_failure(self):
        before = self.seed()
        real_factory = mm.tempfile.NamedTemporaryFile
        for failure in ('write', 'close'):
            with self.subTest(failure=failure):
                @contextlib.contextmanager
                def faulty(**kwargs):
                    with real_factory(**kwargs) as stream:
                        if failure == 'write':
                            def partial(payload):
                                stream.write(payload[:4])
                                raise OSError('partial')
                            yield type('Stream', (), {'name': stream.name,
                                                     'write': staticmethod(partial)})()
                        else:
                            yield stream
                    if failure == 'close':
                        raise OSError('close')
                with patch.object(mm.tempfile, 'NamedTemporaryFile', faulty):
                    with self.assertRaises(OSError):
                        mm.save_memory({'new': 'payload'})
                self.assertEqual(self.path.read_bytes(), before)
                self.assert_clean()

    def test_replace_failure_existing_and_missing(self):
        before = self.seed()
        for exists in (True, False):
            if not exists:
                self.path.unlink()
            with patch.object(mm.os, 'replace', side_effect=PermissionError('denied')) as replace:
                with self.assertRaises(PermissionError):
                    mm.save_memory({'new': 1})
                self.assertEqual(replace.call_count, 1)
            if exists:
                self.assertEqual(self.path.read_bytes(), before)
            else:
                self.assertFalse(self.path.exists())
            self.assert_clean()

    def test_cleanup_failure_does_not_mask_original(self):
        self.seed()
        with patch.object(mm.os, 'replace', side_effect=PermissionError('original')):
            with patch.object(Path, 'unlink', side_effect=OSError('cleanup')):
                with self.assertRaisesRegex(PermissionError, 'original'):
                    mm.save_memory({'new': 1})
        # Only this operation's uniquely named temporary remains; destination is valid.
        self.assertEqual(len(list(self.path.parent.glob('*.tmp'))), 1)
        self.assertEqual(mm.load_memory()['extra'], [1])

    def test_all_mutators_fail_without_false_success(self):
        before = self.seed()
        operations = [lambda: mm.update_memory({'notes': {'new': 'value'}}),
                      lambda: mm.remember('new', 'value'),
                      lambda: mm.forget('legacy'),
                      lambda: mm.save_session_summary('new')]
        with patch.object(mm.os, 'replace', side_effect=PermissionError('denied')):
            for operation in operations:
                with self.assertRaises(PermissionError):
                    operation()
                self.assertEqual(self.path.read_bytes(), before)
            self.assertIsNone(mm.pop_last_session())
            self.assertEqual(self.path.read_bytes(), before)
        self.assert_clean()

    def test_mutators_compatibility_and_lifo(self):
        self.seed()
        mm.remember('long', 'x' * 500)
        self.assertEqual(len(mm.load_memory()['notes']['long']['value']), 381)
        self.assertTrue(mm.forget('legacy').startswith('Forgotten:'))
        self.assertTrue(mm.forget('absent').startswith('Not found:'))
        for i in range(4):
            mm.save_session_summary(str(i), 'pt')
        self.assertEqual(len(mm.load_memory()['sessions']), 3)
        self.assertEqual([mm.pop_last_session()['summary'] for _ in range(3)], ['3', '2', '1'])
        self.assertIsNone(mm.pop_last_session())
        self.assertEqual(mm.load_memory()['extra'], [1])

    def test_invalid_json_and_invalid_arguments(self):
        self.path.parent.mkdir()
        self.path.write_bytes(b'{invalid')
        self.assertEqual(mm.load_memory(), mm._empty_memory())
        self.assertIsNone(mm.pop_last_session())
        mm.save_memory(None)
        mm.save_session_summary('  ')
        self.assertEqual(self.path.read_bytes(), b'{invalid')

    def test_trim_notification(self):
        data = mm._empty_memory()
        data['notes'] = {'old': {'value': 'x' * 100, 'updated': '2000-01-01'},
                         'new': {'value': 'y' * 100, 'updated': '2026-01-01'}}
        notifier = Mock()
        limit = len(json.dumps(data, ensure_ascii=False)) - 1
        with patch.object(mm, 'MEMORY_MAX_CHARS', limit), patch.object(mm, '_trim_notifier', notifier):
            mm.save_memory(data)
        self.assertNotIn('old', mm.load_memory()['notes'])
        self.assertIn('new', mm.load_memory()['notes'])
        notifier.assert_called_once()

    def test_publish_only_after_complete_close(self):
        before = self.seed()
        real_replace = mm.os.replace
        def observe(source, destination):
            self.assertEqual(Path(source).parent, self.path.parent)
            self.assertEqual(self.path.read_bytes(), before)
            self.assertEqual(json.loads(Path(source).read_text(encoding='utf-8')), {'new': 'é'})
            # On Windows replace also verifies the temporary is no longer open.
            return real_replace(source, destination)
        with patch.object(mm.os, 'replace', side_effect=observe):
            mm.save_memory({'new': 'é'})
        self.assertEqual(mm.load_memory()['new'], 'é')

    def test_concurrent_internal_mutators_serialize_transactions(self):
        self.seed()
        # Instrument acquisition to prove the second thread attempts the lock
        # while the first transaction is paused after its read.
        real_lock = threading.RLock()
        attempted = threading.Event()
        read_paused = threading.Event()
        release = threading.Event()
        errors = []
        class ObservedLock:
            def __enter__(self):
                if threading.current_thread().name == 'second':
                    attempted.set()
                real_lock.acquire()
            def __exit__(self, *args):
                real_lock.release()
        real_load = mm.load_memory
        def paused_load():
            result = real_load()
            if threading.current_thread().name == 'first':
                read_paused.set()
                if not release.wait(3):
                    raise TimeoutError('test release')
            return result
        def run(fn):
            try:
                fn()
            except BaseException as exc:
                errors.append(exc)
        operations = [lambda: mm.update_memory({'notes': {'added': 'value'}}),
                      lambda: mm.forget('legacy'),
                      lambda: mm.save_session_summary('concurrent'),
                      mm.pop_last_session]
        for operation in operations:
            with self.subTest(operation=operation):
                self.seed()
                attempted.clear(); read_paused.clear(); release.clear()
                with patch.object(mm, '_lock', ObservedLock()), patch.object(mm, 'load_memory', paused_load):
                    first = threading.Thread(name='first', target=run,
                                             args=(lambda: mm.update_memory({'notes': {'first': 'kept'}}),))
                    second = threading.Thread(name='second', target=run, args=(operation,))
                    first.start()
                    try:
                        self.assertTrue(read_paused.wait(3))
                        second.start()
                        self.assertTrue(attempted.wait(3))
                    finally:
                        release.set()
                        first.join(4)
                        if second.ident is not None:
                            second.join(4)
                    self.assertFalse(first.is_alive())
                    self.assertFalse(second.is_alive())
                self.assertEqual(errors, [])
                self.assertEqual(mm.load_memory()['notes']['first']['value'], 'kept')

    def test_external_reader_never_sees_partial_json(self):
        self.seed()
        barrier = threading.Barrier(2, timeout=4)
        errors = []
        def reader():
            try:
                for _ in range(30):
                    barrier.wait()
                    value = json.loads(self.path.read_text(encoding='utf-8'))
                    self.assertIsInstance(value, dict)
                    barrier.wait()
            except BaseException as exc:
                errors.append(exc)
        worker = threading.Thread(target=reader)
        worker.start()
        try:
            for i in range(30):
                barrier.wait()
                mm.save_memory({'notes': {'n': 'é' * (1000 + i)}})
                barrier.wait()
        finally:
            worker.join(5)
        self.assertFalse(worker.is_alive())
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
