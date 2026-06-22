"""Run a shell command, capture the result. Same security caveat as python_runner."""
from __future__ import annotations
import subprocess


def run_shell(cmd: str, *, timeout: int = 30, cwd: str | None = None) -> dict:
    """Execute `cmd` in a subprocess. Returns {ok, stdout, stderr, returncode}."""
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           timeout=timeout, cwd=cwd)
        return {"ok": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr,
                "returncode": p.returncode}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": f"timeout after {timeout}s", "returncode": -9}
