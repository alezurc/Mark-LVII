"""Behavior of desktop localization and isolated configuration persistence."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from gui import i18n
from memory import config_manager as config


class LanguageTests(unittest.TestCase):
    def tearDown(self):
        i18n.set_language("en")

    def test_locale_validation_and_english_default(self):
        for value in (None, "", "pt", "fr", [], 12, "PT-BR"):
            self.assertEqual(i18n.normalize_language(value), "en")
        self.assertEqual(i18n.normalize_language("pt-BR"), "pt-BR")
        i18n.set_language("invalid")
        self.assertEqual(i18n.get_language(), "en")

    def test_translation_fallback_and_opaque_values(self):
        message = i18n.tr("Could not save interface language: {error}", error="CLOSE")
        i18n.set_language("pt-BR")
        self.assertEqual(i18n.render(i18n.tr("CLOSE")), "FECHAR")
        self.assertEqual(i18n.render("CLOSE"), "CLOSE")
        self.assertEqual(i18n.render(i18n.tr("unknown key")), "unknown key")
        self.assertEqual(i18n.render(message), "Não foi possível salvar o idioma da interface: CLOSE")
        self.assertEqual(i18n.render(i18n.tr("missing {value}")), "missing {value}")

    def test_nested_messages_retranslate_without_touching_values(self):
        composed = i18n.tr("{left}{right}", left=i18n.tr("CLOSE"), right=" CLOSE")
        i18n.set_language("pt-BR")
        self.assertEqual(i18n.render(composed), "FECHAR CLOSE")
        i18n.set_language("en")
        self.assertEqual(i18n.render(composed), "CLOSE CLOSE")

    def test_catalog_placeholders_and_coverage(self):
        self.assertEqual(i18n.catalog_errors(), [])
        self.assertGreater(len(i18n.PT_BR), 200)
        self.assertTrue(all(isinstance(v, str) and v for v in i18n.PT_BR.values()))
        for path in (Path(__file__).resolve().parents[1] / "gui").glob("*.py"):
            if path.name == "i18n.py":
                continue
            import ast
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id == "tr" and node.args
                        and isinstance(node.args[0], ast.Constant)):
                    source = node.args[0].value
                    # Pure composition/formatting has no translatable literal.
                    import re
                    literal = re.sub(r"\{[^}]*\}", "", source)
                    if any(c.isalpha() for c in literal):
                        self.assertIn(source, i18n.PT_BR, (path.name, node.lineno, source))

    def test_persistence_preserves_settings_and_defaults(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "api_keys.json"
            with patch.object(config, "CONFIG_DIR", Path(folder)), patch.object(config, "CONFIG_FILE", target):
                self.assertEqual(config.get_ui_language(), "en")
                config.update_config(assistant_name="SENTINEL", unrelated={"value": 42})
                config.save_ui_language("pt-BR")
                self.assertEqual(config.get_ui_language(), "pt-BR")
                data = json.loads(target.read_text(encoding="utf-8"))
                self.assertEqual(data["unrelated"], {"value": 42})
                self.assertEqual(data["assistant_name"], "SENTINEL")
                config.save_ui_language("invalid")
                self.assertEqual(config.get_ui_language(), "en")

    def test_failed_write_does_not_claim_persistence(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "api_keys.json"
            with patch.object(config, "CONFIG_DIR", Path(folder)), patch.object(config, "CONFIG_FILE", target):
                config.save_ui_language("en")
                before = target.read_bytes()
                with patch.object(config, "_write_config", side_effect=OSError("synthetic failure")):
                    with self.assertRaisesRegex(OSError, "synthetic failure"):
                        config.save_ui_language("pt-BR")
                self.assertEqual(target.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
