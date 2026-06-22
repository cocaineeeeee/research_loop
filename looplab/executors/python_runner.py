"""
Run model-written Python and capture the result. This is what turns the loop
from "screen claims" into "do research": the model's hypothesis is tested by
*executing code*, and the execution output — not the model's say-so — decides.

SECURITY: this executes code an LLM wrote. That is dangerous (it can delete files,
exfiltrate secrets, hit the network). It runs in a subprocess with a timeout, but
that is NOT a sandbox. For anything beyond toy use, run inside a container / VM /
seccomp jail and drop network. The autonomous example requires an explicit
--allow-exec flag for exactly this reason.
"""
from __future__ import annotations
import os
import subprocess
import sys
import tempfile


def run_python(code: str, *, timeout: int = 30, cwd: str | None = None) -> dict:
    """Execute `code` in a fresh subprocess. Returns {ok, stdout, stderr, returncode}."""
    fd, path = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(code)
        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=timeout, cwd=cwd,
        )
        return {"ok": proc.returncode == 0, "stdout": proc.stdout,
                "stderr": proc.stderr, "returncode": proc.returncode}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": f"timeout after {timeout}s", "returncode": -9}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "stdout": "", "stderr": f"{type(e).__name__}: {e}", "returncode": -1}
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
