"""
An LLM agent makes three confident "discoveries". looplab screens them through
a frozen ruler of external anchors — and kills the ones that only the model
believes, or that the published record already owns.

    python examples/agent_claims.py

The agent's self-confidence is recorded, but never sufficient. What decides is
the highest *independent* anchor a claim clears: a deterministic recompute and a
prior-art search. This is the moment every AI researcher knows — the model says
"95% sure, this is novel" and something outside the model has to check.

Anchors here are deterministic stand-ins so the demo is self-contained and
zero-dependency. In real use you plug in your domain's checks (a real recompute,
a certificate, an arXiv search). looplab does not make those checks for you — it
just refuses to let a claim be called SURVIVED without one.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from looplab import Tier, Anchor, Preregister, Loop

# What the agent generated. `confidence` is the model judging itself. The other
# fields are facts an *external* check would discover — not the model's opinion.
CLAIMS = [
    {"id": "new closed-form for the partition sum", "confidence": 0.95,
     "recompute_matches": True,  "prior_art": None},
    {"id": "novel O(n log n) bound on the cut",     "confidence": 0.93,
     "recompute_matches": True,  "prior_art": "arXiv:1109.4205"},
    {"id": "the variational energy beats FCI",      "confidence": 0.98,
     "recompute_matches": False, "prior_art": None},
]

def recompute(c):  # deterministic ground truth — fixed by maths, unfakeable
    ok = c["recompute_matches"]
    return (ok, f"artifacts/recompute_{c['id'][:6]}.log",
            "" if ok else "deterministic recompute disagrees (energy below FCI is impossible)")

def prior_art(c):  # has the published record already done this?
    pub = c["prior_art"]
    return (pub is None, pub or "artifacts/search_clean.md",
            "" if pub is None else f"already published — {pub}")

def self_review(c):  # the generator grading its own homework
    return (c["confidence"] >= 0.9, "artifacts/self_note.md",
            f"model {int(c['confidence']*100)}% confident")

anchors = [
    Anchor("deterministic-recompute", Tier.INVARIANT, recompute),
    Anchor("prior-art-search",        Tier.PRIOR_ART, prior_art),
    Anchor("self-assessment",         Tier.SELF,      self_review),
]

def main():
    os.makedirs("artifacts", exist_ok=True)
    prereg = Preregister(
        question="Which of the agent's claimed discoveries survive external screening?",
        anchors=[a.name for a in anchors],
        thresholds={"survive": "no failed anchor AND >=1 independent pass"},
    )
    print(f"ruler frozen: {prereg.freeze('artifacts/prereg.json')}\n")
    loop = Loop(prereg, anchors, ledger="artifacts/ledger.jsonl")

    for c in CLAIMS:
        r = loop.evaluate(c["id"], payload=c)
        conf = int(c["confidence"] * 100)
        print(f"CLAIM: {c['id']}  [model: {conf}% confident]")
        if r.survived:
            print(f"  \033[32m=> SURVIVED\033[0m  (independent anchor: {r.top_independent_tier.name})\n")
        else:
            print(f"  \033[31m=> REJECTED\033[0m  {r.retired_because}\n")

    print(loop.calibration_report())

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
