#!/usr/bin/env bash
# One command to verify every guard looplab promises, then run the demo.
set -e
pip install -e . -q
echo "== tests =="
python tests/test_looplab.py
echo
echo "== demo =="
python examples/agent_claims.py
