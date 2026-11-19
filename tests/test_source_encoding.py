"""D007: source hygiene and the actual synthetic PCM expression, without imports."""
import ast
from pathlib import Path
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "providers" / "_tests.py"


def pcm_expression(data):
    tree = ast.parse(data)
    test = next(n for n in tree.body if isinstance(n, ast.AsyncFunctionDef)
                and n.name == "test_it_speaks_before_the_tool_runs")
    voice = next(n for n in test.body if isinstance(n, ast.ClassDef) and n.name == "TTS")
    speak = next(n for n in voice.body if isinstance(n, ast.AsyncFunctionDef) and n.name == "speak")
    expression = next(n.value for n in ast.walk(speak) if isinstance(n, ast.Yield))
    if not isinstance(expression, ast.BinOp) or not isinstance(expression.op, ast.Mult):
        raise AssertionError("PCM fixture must remain a repeated bytes literal")
    return ast.literal_eval(expression.left) * ast.literal_eval(expression.right)


def validate(data):
    data.decode("utf-8", errors="strict")
    if data.startswith(b"\xef\xbb\xbf"):
        raise AssertionError("unexpected BOM")
    if any(b < 32 and b not in (9, 10, 13) for b in data):
        raise AssertionError("unexpected literal control")
    if b"\n" in data.replace(b"\r\n", b""):
        raise AssertionError("CRLF must be preserved")
    if pcm_expression(data) != bytes([1, 2]) * 1000:
        raise AssertionError("synthetic PCM changed")


class SourceEncodingTests(unittest.TestCase):
    def test_source_and_pcm(self):
        validate(SOURCE.read_bytes())

    def test_old_literal_and_new_escapes_have_same_semantics(self):
        data = SOURCE.read_bytes()
        old = data.replace(b'\\x01\\x02" * 1000', bytes([1, 2]) + b'" * 1000')
        self.assertNotEqual(data, old)
        self.assertEqual(pcm_expression(old), pcm_expression(data))
        with self.assertRaisesRegex(AssertionError, "literal control"):
            validate(old)

    def test_pcm_regression_is_rejected(self):
        changed = SOURCE.read_bytes().replace(b'\\x01\\x02" * 1000', b'\\x00\\x00" * 1000')
        with self.assertRaisesRegex(AssertionError, "PCM changed"):
            validate(changed)


if __name__ == "__main__":
    unittest.main()
