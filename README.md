<!-- Author withheld (anonymous) during review. -->

# looplab

> **An LLM will fabricate a result, score itself 95% confident, and move the goalpost when you push back. `looplab` runs the research loop where an external anchor — not the model — decides what survives.**

[![CI](https://github.com/cocaineeeeee/research_loop/actions/workflows/ci.yml/badge.svg)](https://github.com/cocaineeeeee/research_loop/actions/workflows/ci.yml) ![status](https://img.shields.io/badge/status-v0.2-orange) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![deps](https://img.shields.io/badge/core-zero%20deps-success) ![license](https://img.shields.io/badge/license-Apache--2.0-green)

An **anchor-first research loop**: generate candidates with *your* model, let an adversary refute them, verify the survivors against an **external, non-fakeable anchor** (a real computation, a solver, a certificate), keep an append-only audit trail, and iterate until the ideas run dry. The discipline you *meant* to follow — freeze the ruler before you look, anchor every claim, never let the model judge itself — enforced in code.

Bring your own model (OpenAI / Anthropic / local — your key, never committed). The verification core has zero dependencies. The point of the whole thing: it makes it hard to fool yourself.

---

## 30-second demo (no install, standard library only)

```bash
git clone https://github.com/<withheld>/research_loop && cd research_loop
python examples/agent_claims.py
```

Three confident "discoveries" from an agent, screened through a frozen ruler:

```text
ruler frozen: 0da6e59585667225

CLAIM: new closed-form for the partition sum        [model: 95% confident]
  => SURVIVED   (independent anchor: INVARIANT)

CLAIM: novel O(n log n) bound on the cut            [model: 93% confident]
  => REJECTED   prior-art: already published — arXiv:1109.4205

CLAIM: the variational energy beats FCI             [model: 98% confident]
  => REJECTED   recompute disagrees (energy below FCI is impossible)

Ruler 0da6e59585667225 | screened: 3 | survived: 1 | retired: 2
```

The claim the model was **most** confident about (98%) is the one killed hardest. Self-confidence is logged; it never decides. Only an independent external check can certify `SURVIVED`.

---

## The full loop, end to end (bring your own model)

`examples/research_loop_demo.py` runs the whole cycle offline (no key — a stub model
stands in for the generator) on a toy task with a *real* deterministic anchor:

```text
Question: find integers below 50 that are prime and congruent to 1 (mod 4)
Rounds: 4 | survivors: 6 | killed: 6

Survivors (cleared an independent external anchor):
  + 5   + 13   + 17   + 29   + 37   + 41
Killed (with reason):
  - 1   [anchor]     not prime
  - 8   [adversary]  even number, cannot be an odd prime
  - 21  [anchor]     not prime
  ...
```

The generator proposes, the adversary cheaply filters, and a **real computation**
decides — and the loop returns the correct answer with an audit trail, not because a
model said so. Swap the stub for your model and the anchor for your domain's verifier:

```python
from looplab import ResearchLoop, Anchor, Tier
from looplab.models import AnthropicModel, OpenAIModel   # bring your own key (env var)

def verify(candidate):                       # YOUR non-fakeable check — the moat
    score, ok = run_real_computation(candidate)
    return ok, f"runs/{candidate}.log", "" if ok else "failed the external check"

engine = ResearchLoop(
    question="propose <X> with property <Y>",
    model=AnthropicModel(model="claude-sonnet-4-6"),   # generator
    adversary=OpenAIModel(model="gpt-5.5"),            # a *different* model = independent
    anchors=[Anchor("verify", Tier.INVARIANT, verify)],
    max_rounds=4,
)
print(engine.run().summary())
```

The keys are read from `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` (or passed in), held only
in memory, and **never written to the ledger or anywhere on disk**.

---

## The four rules, enforced in code

| Rule | What it means | Why you can't skip it |
|---|---|---|
| **Freeze the ruler** | Your anchors and thresholds are hashed and locked *before* results are seen. | Editing them afterwards is detected and refused (goalpost-moving guard). |
| **Anchor every claim** | A verdict must point to a raw artifact — a recompute log, a certificate, a prior-art hit. | A verdict with no evidence pointer raises an error. No orphan claims. |
| **Self-judgement never decides** | The model is a generator, not the judge. | A claim that passes only on `SELF` is auto-rejected; it must clear an *independent* anchor. |
| **Append-only audit trail** | Every verdict, with evidence and the ruler fingerprint, is written once. | The trail is tamper-evident; you can reconstruct exactly what was decided and why. |

Anchors are ranked by independence from the generator:

`INVARIANT` (deterministic ground truth) · `CERTIFICATE` (machine-checkable proof) · `EXPERIMENT` · `PRIOR_ART` · `CROSS_MODEL` (a *different* model) · `SELF` — *never sufficient alone.*

---

## Use it on your own loop

You supply the candidates and the anchors for *your* field; the harness enforces the discipline. This is the real API (it's what `examples/agent_claims.py` runs):

```python
from looplab import Tier, Anchor, Preregister, Loop

# An anchor returns (passed, evidence_pointer, detail). The evidence pointer is
# mandatory — a path / URL / hash a skeptic could re-inspect.
def recompute(claim):
    ok = deterministic_recheck(claim)              # your domain's ground truth
    return ok, f"runs/{claim.id}.log", "" if ok else "recompute disagrees"

anchors = [
    Anchor("recompute",  Tier.INVARIANT,   recompute),
    Anchor("prior-art",  Tier.PRIOR_ART,   prior_art_search),
    Anchor("self",       Tier.SELF,        model_confidence),  # logged, never decisive
]

prereg = Preregister(question="which claims survive?", anchors=[a.name for a in anchors])
prereg.freeze("prereg.json")                       # ruler hashed + locked

loop = Loop(prereg, anchors, ledger="ledger.jsonl")
for claim in claims:
    loop.evaluate(claim)

print(loop.calibration_report())                   # survivors + a kill-map
```

---

## How it compares

|  | **looplab** | "be careful" prompt | OSF preregistration | nothing |
|---|:--:|:--:|:--:|:--:|
| ruler frozen *in code*, edits blocked | ✅ | ❌ | ⚠️ paperwork | ❌ |
| claim auto-rejected without an external anchor | ✅ | ❌ | ❌ | ❌ |
| model can't grade its own homework | ✅ | ❌ | ❌ | ❌ |
| goalpost-moving detected | ✅ | ❌ | ⚠️ months later | ❌ |
| tamper-evident audit trail | ✅ | ❌ | ⚠️ a dated doc | ❌ |
| runs inside your loop, today, zero deps | ✅ | ✅ | ❌ | ✅ |

---

## Where it comes from

`looplab` is the distilled discipline from a real research pilot in strongly correlated quantum chemistry: ~14 candidate directions were broadcast in parallel, each judged for life or death against an external anchor; **11 were retired, 3 advanced, and the survivors became submission-ready manuscripts.** The harness is what made that screening reproducible and auditable instead of a matter of opinion — including the moment it killed the direction the pilot was *most* excited about, because an independent prior-art check found it had been published 25 years earlier.

- The operating discipline and its measured limits: [`method/`](method/)
- The pilot, its three results, and the full kill-map: [`pilot/`](pilot/)

---

## Install

```bash
pip install -e .          # zero dependencies, Python 3.9+
```

---

## Status (honest)

- **v0.1.** The four guards (freeze, anchor-or-reject, self-can't-decide, append-only log) work and are exercised by `examples/`. The API may still move. Not yet on PyPI.
- Distilled from a real quantum-chemistry pilot whose three manuscripts are **submission-ready, not yet peer-reviewed**. `looplab` is the *process* that produced them, not a claim that the results are blessed.
- Not a model, not an agent framework, not an API wrapper. A small set of rules in plain Python you wrap around any model.

## License

Apache-2.0. Author withheld during review.
