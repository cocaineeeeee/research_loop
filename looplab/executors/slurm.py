"""Submit a job to Slurm (optional executor for heavy compute anchors).

Heavy verification (e.g. an FCI/SDP anchor) should not run on a login node. This
wraps `sbatch`; it is a thin convenience, not a scheduler. Requires Slurm on PATH.
"""
from __future__ import annotations
import re
import subprocess
import tempfile
import os


def submit_slurm(script_body: str, *, time="01:00:00", cpus=4, mem="8G",
                 partition: str | None = None, job_name="looplab") -> dict:
    """Write an sbatch script and submit it. Returns {ok, job_id, stderr}."""
    hdr = [f"#SBATCH --job-name={job_name}", f"#SBATCH --time={time}",
           f"#SBATCH --cpus-per-task={cpus}", f"#SBATCH --mem={mem}"]
    if partition:
        hdr.append(f"#SBATCH --partition={partition}")
    fd, path = tempfile.mkstemp(suffix=".sh")
    with os.fdopen(fd, "w") as f:
        f.write("#!/bin/bash\n" + "\n".join(hdr) + "\n" + script_body + "\n")
    try:
        p = subprocess.run(["sbatch", path], capture_output=True, text=True, timeout=30)
        m = re.search(r"(\d+)", p.stdout or "")
        return {"ok": p.returncode == 0, "job_id": (m.group(1) if m else None),
                "stderr": p.stderr}
    except FileNotFoundError:
        return {"ok": False, "job_id": None, "stderr": "sbatch not found (Slurm not available)"}
    finally:
        try: os.unlink(path)
        except OSError: pass
