"""
Runnable demo of the looplab discipline.

    python examples/demo.py

It screens four toy "research claims" through a pre-registered ruler of external
anchors and shows the four enforced rules in action:

  * a claim is RETIRED when an anchor refutes it (with the reason on the record);
  * a claim that only passes self-judgement is NOT counted as a survivor;
  * every verdict carries an evidence pointer (no orphan claims);
  * changing the ruler after freezing is caught (try it — see the note at the end).

The anchors here are deterministic toys so the demo is self-contained. In real
use you plug in *your* domain's external checks: a deterministic recompute, a
machine-checkable certificate, an experiment, or a prior-art search.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from looplab import Tier, Anchor, Preregister, Loop


# --------------------------------------------------------------------------- #
# Toy candidates: each is a dict describing a "claim" and the facts about it.
# --------------------------------------------------------------------------- #
CANDIDATES = [
    {"name": "A: invariant-respecting identity",
     "recompute_stable": True, "in_prior_art": False, "model_likes_it": True},
    {"name": "B: rediscovers a known result",
     "recompute_stable": True, "in_prior_art": True,  "model_likes_it": True},
    {"name": "C: fails the deterministic recheck",
     "recompute_stable": False, "in_prior_art": False, "model_likes_it": True},
    {"name": "D: only the model is impressed",
     "recompute_stable": None,  "in_prior_art": False, "model_likes_it": True},
]


# --------------------------------------------------------------------------- #
# Anchors = the external checks. Each returns (passed, evidence, detail).
# Tiers declare how independent each check is of the generator.
# --------------------------------------------------------------------------- #
def invariant_check(c):
    if c["recompute_stable"] is None:
        return (False, "artifacts/recompute_D.log", "no deterministic recheck available")
    return (c["recompute_stable"],
            f"artifacts/recompute_{c['name'][0]}.log",
            "" if c["recompute_stable"] else "result changed under the invariant recompute")

def prior_art_check(c):
    return (not c["in_prior_art"],
            f"artifacts/prior_art_{c['name'][0]}.md",
            "already in the published record" if c["in_prior_art"] else "")

def self_check(c):
    # The generator judging itself. Recorded, but never sufficient alone.
    return (c["model_likes_it"], f"artifacts/self_note_{c['name'][0]}.md",
            "generator is confident" if c["model_likes_it"] else "")


anchors = [
    Anchor("deterministic-invariant", Tier.INVARIANT, invariant_check),
    Anchor("prior-art-search",        Tier.PRIOR_ART, prior_art_check),
    Anchor("self-assessment",         Tier.SELF,      self_check),
]


def main():
    prereg = Preregister(
        question="Which candidate directions survive external screening?",
        anchors=[a.name for a in anchors],
        thresholds={"survive": "no failed anchor AND >=1 independent pass"},
        notes="Toy demo; anchors are deterministic stand-ins.",
    )
    fp = prereg.freeze("artifacts/prereg.json")
    print(f"Ruler frozen: {fp}\n")

    loop = Loop(prereg, anchors, ledger="artifacts/ledger.jsonl")
    for c in CANDIDATES:
        loop.evaluate(c["name"], payload=c)

    print(loop.calibration_report())
    print("\n(audit trail written to artifacts/ledger.jsonl)")

    # Show the goalpost-moving guard: rebuilding the loop with a different
    # anchor set than was pre-registered is refused.
    print("\n--- goalpost-moving guard ---")
    try:
        Loop(prereg, anchors[:2], ledger="artifacts/ledger.jsonl")
    except RuntimeError as e:
        print("refused, as designed:\n " + str(e).splitlines()[0])


if __name__ == "__main__":
    os.makedirs(os.path.join(os.path.dirname(__file__), "artifacts"), exist_ok=True)
    os.chdir(os.path.dirname(__file__))
    main()
