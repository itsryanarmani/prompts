#!/usr/bin/env python3
"""Run the same checks locally and in CI."""

from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
for args in [["-m", "unittest", "discover", "-s", "tests", "-v"], ["scripts/check.py"]]:
    result = subprocess.run([sys.executable, *args], cwd=root, check=False)
    if result.returncode:
        sys.exit(result.returncode)
