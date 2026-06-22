<!-- Author withheld (anonymous) during review. -->

# looplab

> **An LLM will fabricate a result, score itself 95% confident, and move the goalpost when you push back. `looplab` is the brake.**

[![CI](https://github.com/cocaineeeeee/research_loop/actions/workflows/ci.yml/badge.svg)](https://github.com/cocaineeeeee/research_loop/actions/workflows/ci.yml) ![status](https://img.shields.io/badge/status-v0.1-orange) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-success) ![license](https://img.shields.io/badge/license-Apache--2.0-green)

A zero-dependency Python harness that enforces the discipline you *meant* to follow when you let an AI agent loose on research: **freeze your ruler before you look at the data, anchor every claim to something the model can't fake, and never let the model's own confidence decide what is true.**

It does not call a model, spawn agents, or need an API key. It does the one thing those tools leave out — it makes it hard to fool yourself.

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
