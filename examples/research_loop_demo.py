"""
The research loop, end to end, offline (no API key — uses StubModel).

    python examples/research_loop_demo.py

A toy but *honest* research task: "find integers below 50 that are prime AND
congruent to 1 (mod 4)". The loop:

  generator (model)  proposes candidate integers, a batch per round
  adversary (model)  cheaply refutes the obviously-wrong ones (even numbers)
  anchor (yours)     VERIFIES survivors with a real, deterministic computation
                     — this is the non-fakeable part; a model never decides it
  -> harvest survivors, iterate until the generator runs dry

Swap StubModel for OpenAIModel/AnthropicModel (bring your own key) and swap the
anchor for your domain's real verifier (a solver, a benchmark, an FCI/SDP check)
and the same loop does real verifiable idea-search.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from looplab import ResearchLoop, Anchor, Tier
from looplab.models import StubModel


# ---- the external anchor: a REAL deterministic check (non-fakeable) ---------
def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))

def prime_and_1mod4(candidate):
    try:
        n = int(str(candidate).strip())
    except ValueError:
        return (False, "verify://parse-fail", "not an integer")
    ok = is_prime(n) and n % 4 == 1
    detail = "" if ok else ("not prime" if not is_prime(n) else "prime but not 1 (mod 4)")
    return (ok, f"verify://prime_and_1mod4/n={n}", detail)


# ---- pluggable models, here stubbed so the demo runs with no API key --------
def make_generator():
    pool = iter([["1", "5", "8", "13", "12"], ["17", "21", "29", "30"], ["37", "41", "49"], []])
    return StubModel(responder=lambda prompt: __import__("json").dumps(next(pool, [])))

def adversary_responder(prompt):
    m = re.search(r"CANDIDATE:\s*(.+)", prompt)
    cand = (m.group(1).strip() if m else "")
    try:
        n = int(cand)
        if n % 2 == 0 and n != 2:            # cheap, fallible filter — kills even numbers
            return '{"refuted": true, "reason": "even number, cannot be an odd prime"}'
    except ValueError:
        return '{"refuted": true, "reason": "not an integer"}'
    return '{"refuted": false, "reason": ""}'


def main():
    engine = ResearchLoop(
        question="find integers below 50 that are prime and congruent to 1 (mod 4)",
        model=make_generator(),                              # generator (pluggable)
        adversary=StubModel(responder=adversary_responder),  # a *different* model in real use
        anchors=[Anchor("prime_and_1mod4", Tier.INVARIANT, prime_and_1mod4)],
        max_rounds=5, per_round=5, ledger="examples/artifacts/research_ledger.jsonl",
    )
    report = engine.run()
    print(report.summary())


if __name__ == "__main__":
    os.makedirs(os.path.join(os.path.dirname(__file__), "artifacts"), exist_ok=True)
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
