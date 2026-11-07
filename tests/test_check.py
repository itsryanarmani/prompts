"""Exercise the checker through its public command before publishing text."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECK = Path(__file__).resolve().parents[1] / "scripts" / "check.py"


class CheckCommand(unittest.TestCase):
    def run_check(self, text=None, name="sample.md", readme=None, extra=None):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "prompts").mkdir()
            (root / "README.md").write_text(
                readme if readme is not None else "# Collection\n\n[Sample](prompts/" + name + ")\n",
                encoding="utf-8",
            )
            if text is not False:
                (root / "prompts" / name).write_text(
                    text if text is not None else "# Sample\n\nUse <PROJECT> and <PATH>.\n",
                    encoding="utf-8",
                )
            if extra is not None:
                (root / "prompts" / "extra.txt").write_text(extra, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(CHECK), "--root", folder],
                capture_output=True, text=True, check=False,
            )

    def test_generic_prompt_and_placeholders_pass(self):
        self.assertEqual(self.run_check().returncode, 0)

    def test_private_content_fails_without_echoing_it(self):
        cases = {
            "email": "person@example.invalid",
            "phone": "+1 202 555 0100",
            "home-path": "/Users/example/private-project/file",
            "linux-path": "/home/example/private-project/file",
            "windows-path": "C:\\Users\\example\\private-project\\file",
            "repository-url": "https://github.com/example/private-project",
            "ssh-repository": "git@github.com:example/private-project.git",
            "web-url": "https://service.example.invalid/path",
            "address": "192.0.2.10",
            "github-secret": "gh" + "p_" + "a" * 36,
            "private-key": "-----BEGIN " + "PRIVATE KEY-----",
        }
        for label, value in cases.items():
            with self.subTest(label=label):
                result = self.run_check("# Sample\n\n" + value + "\n")
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn(value, result.stdout + result.stderr)

    def test_readme_is_also_checked(self):
        result = self.run_check(readme="# Collection\n\nperson@example.invalid\n")
        self.assertNotEqual(result.returncode, 0)

    def test_non_markdown_prompt_cannot_bypass_checks(self):
        result = self.run_check(extra="person@example.invalid")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("person@example.invalid", result.stdout + result.stderr)

    def test_markdown_structure_failures(self):
        for text in ["No heading\n", "# Sample\n\nText  \n", "# Sample", "# Sample\n\n```text\nunclosed\n", "# Sample\n\n~~~text\nunclosed\n"]:
            with self.subTest(text=text):
                self.assertNotEqual(self.run_check(text).returncode, 0)

    def test_valid_long_and_tilde_fences_pass(self):
        for text in ["# Sample\n\n````text\nLiteral marker:\n```\n````\n", "# Sample\n\n~~~text\nExample\n~~~\n"]:
            self.assertEqual(self.run_check(text).returncode, 0)

    def test_missing_or_unindexed_prompt_fails(self):
        self.assertNotEqual(self.run_check(text=False).returncode, 0)
        self.assertNotEqual(self.run_check(readme="# Collection\n").returncode, 0)

    def test_bad_filename_and_missing_link_fail(self):
        self.assertNotEqual(self.run_check(name="Bad Name.md").returncode, 0)
        self.assertNotEqual(self.run_check(text="# Sample\n\n[Missing](absent.md)\n").returncode, 0)

    def test_link_cannot_leave_the_repository(self):
        self.assertNotEqual(self.run_check(text="# Sample\n\n[Outside](../../outside.md)\n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
