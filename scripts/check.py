#!/usr/bin/env python3
"""Check public prompt text without printing rejected content."""

import argparse
from pathlib import Path
import re
import sys

PATTERNS = {
    "email": r"[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}",
    "phone": r"(?<!\w)\+\d[\d ()-]{7,}\d",
    "home-path": r"(?:/Users/|/home/|[A-Za-z]:[\\/]Users[\\/])[^\s<>`]+",
    "repository": r"(?:git@[^\s:]+:|(?:github|gitlab|bitbucket)\.\w+/)[\w.-]+/[\w.-]+",
    "url": r"https?://[^\s<>`]+",
    "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "credential": r"(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)",
    "key-shaped": r"\b[0-9a-fA-F]{32,}\b",
}
LINK = re.compile(r"!?\[[^\]]*\]\(([^\s)]+)\)")


def check(root):
    findings = []
    prompts = sorted((root / "prompts").rglob("*.md"))
    files = [root / "README.md", *prompts]

    def report(path, line, rule):
        findings.append(f"{path.relative_to(root)}:{line}: {rule}")

    for path in (root / "prompts").rglob("*"):
        if path.is_symlink() or (path.is_file() and path.suffix != ".md"):
            report(path, 1, "Only regular Markdown prompt files are allowed.")
    if not prompts:
        findings.append("prompts:1: Add at least one Markdown prompt.")
    for path in files:
        if path.is_symlink() or not path.is_file():
            report(path, 1, "Expected a regular Markdown file.")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            report(path, 1, "Use UTF-8 text.")
            continue
        if not re.match(r"# \S", text):
            report(path, 1, "Start with one level-one title.")
        if not text.endswith("\n"):
            report(path, 1, "End the file with a newline.")
        if path != root / "README.md" and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*\.md", path.name):
            report(path, 1, "Use a lowercase, hyphenated filename.")
        fence = None
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line or "\t" in line:
                report(path, number, "Remove trailing spaces and tabs.")
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if marker:
                chars, tail = marker.groups()
                if fence is None:
                    if chars[0] != "`" or "`" not in tail:
                        fence = (chars[0], len(chars))
                elif chars[0] == fence[0] and len(chars) >= fence[1] and not tail.strip():
                    fence = None
            for label, pattern in PATTERNS.items():
                if re.search(pattern, line):
                    report(path, number, f"privacy/{label}: Use a generic placeholder.")
            for target in LINK.findall(line):
                target = target.split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.is_relative_to(root) or not resolved.is_file():
                    report(path, number, "Link must target a file inside the repository.")
        if fence:
            report(path, 1, "Close each fenced code block.")
    readme = root / "README.md"
    if readme.is_file() and not readme.is_symlink():
        indexed = set(LINK.findall(readme.read_text(encoding="utf-8")))
        for path in prompts:
            if path.relative_to(root).as_posix() not in indexed:
                report(path, 1, "Add the prompt to the README index.")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root.resolve()
    findings = check(root)
    for finding in findings:
        print(finding)
    if findings:
        return 1
    print("Prompt, privacy, Markdown, and index checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
