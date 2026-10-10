#!/usr/bin/env python3
"""Prepare the pinned python-for-android source used by local and CI builds."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
P4A_DIR = ROOT / ".p4a"
P4A_REPOSITORY = "https://github.com/kivy/python-for-android.git"
P4A_COMMIT = "58d21141f17c889bf8585f5665921d72028f8831"
OLD_PIP_COMMAND = "source venv/bin/activate && pip install -U pip"
PINNED_PIP_COMMAND = (
    "source venv/bin/activate && pip install --force-reinstall pip==25.3"
)


def run(*args: str) -> str:
    result = subprocess.run(
        args, cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE
    )
    return result.stdout.strip()


if not P4A_DIR.exists():
    run("git", "clone", P4A_REPOSITORY, str(P4A_DIR))

actual_remote = run("git", "-C", str(P4A_DIR), "remote", "get-url", "origin")
if actual_remote != P4A_REPOSITORY:
    raise SystemExit(f"Unexpected python-for-android remote: {actual_remote}")

run("git", "-C", str(P4A_DIR), "fetch", "--depth=1", "origin", P4A_COMMIT)
run("git", "-C", str(P4A_DIR), "checkout", "--detach", P4A_COMMIT)

build_file = P4A_DIR / "pythonforandroid" / "build.py"
source = build_file.read_text()
if PINNED_PIP_COMMAND not in source:
    if OLD_PIP_COMMAND not in source:
        raise SystemExit("Expected python-for-android pip bootstrap command not found")
    build_file.write_text(source.replace(OLD_PIP_COMMAND, PINNED_PIP_COMMAND, 1))

print(f"python-for-android ready at {P4A_COMMIT}")
