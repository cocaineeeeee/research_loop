"""Executors: run the code/compute a research loop proposes. Use with care — they
run model-written code (see the security note in each module)."""
from .python_runner import run_python
from .shell import run_shell
from .slurm import submit_slurm

__all__ = ["run_python", "run_shell", "submit_slurm"]
