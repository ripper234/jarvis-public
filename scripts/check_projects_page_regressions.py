#!/usr/bin/env python3
from pathlib import Path
import sys

PROJECTS = Path(__file__).resolve().parent.parent / "projects.html"
text = PROJECTS.read_text(encoding="utf-8")

forbidden = {
    "Investment Focus": "Investment Focus section must never appear on the projects page.",
    "Investment Thesis": "Investment thesis copy must never appear on the projects page.",
}

violations = [message for needle, message in forbidden.items() if needle in text]

if violations:
    print("Projects page regression check failed:", file=sys.stderr)
    for msg in violations:
        print(f"- {msg}", file=sys.stderr)
    sys.exit(1)

print("Projects page regression check passed")
