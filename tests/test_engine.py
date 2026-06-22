"""The research loop runs end to end (offline, StubModel) and the anchor decides."""
import os, sys, json, re, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from looplab import ResearchLoop, Anchor, Tier
from looplab.models import StubModel


def _is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))

def _anchor(c):
    try:
        n = int(str(c).strip())
    except ValueError:
        return (False, "verify://parse", "not int")
    ok = _is_prime(n) and n % 4 == 1
    return (ok, f"verify://{n}", "" if ok else "fails property")


def test_loop_finds_the_right_answers_and_goes_dry():
    pool = iter([["5", "8", "13"], ["7", "17", "20", "29"], []])  # 7 = prime but ≡3 (mod4)
    gen = StubModel(responder=lambda p: json.dumps(next(pool, [])))

    def adv(p):
        m = re.search(r"CANDIDATE:\s*(.+)", p)
        try:
            if int(m.group(1).strip()) % 2 == 0:
                return '{"refuted": true, "reason": "even"}'
        except Exception:
            pass
        return '{"refuted": false, "reason": ""}'

    with tempfile.TemporaryDirectory() as tmp:
        engine = ResearchLoop(
            question="primes ≡ 1 (mod 4)",
            model=gen, adversary=StubModel(responder=adv),
            anchors=[Anchor("prop", Tier.INVARIANT, _anchor)],
            max_rounds=5, per_round=4, ledger=os.path.join(tmp, "l.jsonl"),
        )
        r = engine.run()
        assert set(r.survivors) == {"5", "13", "17", "29"}, r.survivors   # the verified ones
        assert any(k["by"] == "adversary" for k in r.killed)              # adversary fired
        assert any(k["by"] == "anchor" for k in r.killed)                 # anchor fired
        assert r.rounds <= 5                                              # terminates


def test_engine_requires_an_anchor():
    try:
        ResearchLoop(question="q", model=StubModel(), anchors=[])
    except ValueError:
        return
    raise AssertionError("an engine with no external anchor must be refused")


if __name__ == "__main__":
    for k, v in sorted(globals().items()):
        if k.startswith("test_"):
            v(); print(f"ok  {k}")
    print("\nengine tests passed")
