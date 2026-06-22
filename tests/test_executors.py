"""Executors really run code, and the execution result (not the model) decides."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from looplab.executors import run_python, run_shell


def test_python_runs_and_captures():
    r = run_python("print(6*7)")
    assert r["ok"] and r["stdout"].strip() == "42", r

def test_python_reports_failure_honestly():
    r = run_python("raise ValueError('boom')")
    assert not r["ok"] and "ValueError" in r["stderr"], r

def test_python_timeout():
    r = run_python("while True: pass", timeout=2)
    assert not r["ok"] and "timeout" in r["stderr"], r

def test_shell_runs():
    r = run_shell("echo hello")
    assert r["ok"] and "hello" in r["stdout"], r

if __name__ == "__main__":
    for k, v in sorted(globals().items()):
        if k.startswith("test_"):
            v(); print(f"ok  {k}")
    print("executor tests passed")
