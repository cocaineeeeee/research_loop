"""Tests for the four guards looplab promises. Run: pytest -q  (or: python tests/test_looplab.py)."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from looplab import Tier, Anchor, Preregister, Loop, Verdict


def _prereg(anchors, tmp):
    pr = Preregister(question="t", anchors=[a.name for a in anchors])
    pr.freeze(os.path.join(tmp, "prereg.json"))
    return pr


def test_verdict_requires_evidence():
    """Guard 2: a verdict with no evidence pointer is refused."""
    try:
        Verdict("a", Tier.INVARIANT, True, evidence="")
    except ValueError:
        return
    raise AssertionError("a verdict with no evidence must raise")


def test_self_alone_cannot_survive():
    """Guard 3: passing only on SELF is not 'survived'."""
    with tempfile.TemporaryDirectory() as tmp:
        anchors = [Anchor("self", Tier.SELF, lambda c: (True, "note.md", "confident"))]
        loop = Loop(_prereg(anchors, tmp), anchors, ledger=os.path.join(tmp, "l.jsonl"))
        res = loop.evaluate("c1")
        assert not res.survived, "SELF-only must not survive"


def test_independent_anchor_survives():
    with tempfile.TemporaryDirectory() as tmp:
        anchors = [Anchor("inv", Tier.INVARIANT, lambda c: (True, "run.log", ""))]
        loop = Loop(_prereg(anchors, tmp), anchors, ledger=os.path.join(tmp, "l.jsonl"))
        res = loop.evaluate("c1")
        assert res.survived and res.top_independent_tier == Tier.INVARIANT


def test_failed_anchor_retires():
    with tempfile.TemporaryDirectory() as tmp:
        anchors = [Anchor("inv", Tier.INVARIANT, lambda c: (True, "r.log", "")),
                   Anchor("prior", Tier.PRIOR_ART, lambda c: (False, "p.md", "already published"))]
        loop = Loop(_prereg(anchors, tmp), anchors, ledger=os.path.join(tmp, "l.jsonl"))
        res = loop.evaluate("c1")
        assert not res.survived and "already published" in res.retired_because


def test_goalpost_moving_guard():
    """Guard 1: running with a different anchor set than was frozen is refused."""
    with tempfile.TemporaryDirectory() as tmp:
        anchors = [Anchor("inv", Tier.INVARIANT, lambda c: (True, "r.log", "")),
                   Anchor("prior", Tier.PRIOR_ART, lambda c: (True, "p.md", ""))]
        pr = _prereg(anchors, tmp)
        try:
            Loop(pr, anchors[:1], ledger=os.path.join(tmp, "l.jsonl"))
        except RuntimeError:
            return
        raise AssertionError("changing the ruler after freeze must be refused")


def test_append_only_ledger_grows():
    """Guard 4: every verdict is appended to the audit trail."""
    with tempfile.TemporaryDirectory() as tmp:
        ledger = os.path.join(tmp, "l.jsonl")
        anchors = [Anchor("inv", Tier.INVARIANT, lambda c: (True, "r.log", ""))]
        loop = Loop(_prereg(anchors, tmp), anchors, ledger=ledger)
        loop.evaluate("c1"); loop.evaluate("c2")
        assert sum(1 for _ in open(ledger)) == 2


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
