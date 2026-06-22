# looplab

**An anti-self-deception harness for AI-accelerated research.**

When you can generate and screen hundreds of research directions with agents, the
bottleneck stops being generation and becomes *not fooling yourself*. `looplab`
is a small, dependency-free Python harness that enforces — in code — the
discipline that keeps a high-throughput research loop honest.

It does four things, and refuses to let you skip them:

1. **Pre-register the ruler.** You declare your anchors and thresholds and *freeze*
   them (hashed, timestamped) before you look at results. Changing the ruler
   afterwards is caught and refused — no moving the goalposts.
2. **Anchor every verdict to evidence.** A verdict with no artifact pointer is a
   `ValueError`. No orphan claims.
3. **Rank anchors by independence.** A candidate can only be marked *survived* if
   an anchor *independent of the generator* passes it. Passing on self-judgement
   alone never counts.
4. **Keep an append-only audit trail.** Every verdict, with its evidence and the
   ruler fingerprint, is written to a ledger you can hand to a skeptic.

## 30-second demo (no install, stdlib only)

```bash
python examples/demo.py
```

```text
Ruler frozen: 3b1953a36b8533a9

Ruler 3b1953a36b8533a9 | candidates screened: 4
  survived (independently anchored): 1
  retired: 3

Survivors (with highest independent anchor cleared):
  + A: invariant-respecting identity  [INVARIANT]

Kill-map (boundary of the explored region):
  - B: rediscovers a known result        ->  prior-art-search: already in the published record
  - C: fails the deterministic recheck   ->  deterministic-invariant: result changed under the invariant recompute
  - D: only the model is impressed       ->  deterministic-invariant: no deterministic recheck available
```

`B` is the case that matters most: a confident, internally-consistent claim that
the prior-art anchor retires because *it already exists*. In real use this is what
catches the directions an enthusiastic generator would otherwise keep alive.

## Use it on your own problem

You supply the candidates and the anchors for *your* field; the harness enforces
the discipline.

```python
from looplab import Tier, Anchor, Preregister, Loop

# An anchor returns (passed, evidence_pointer, detail). The evidence pointer is
# mandatory — a path/URL/hash a skeptic could re-inspect.
def recompute(candidate):
    ok = run_deterministic_check(candidate)          # your domain's ground truth
    return ok, f"runs/{candidate.id}.log", "" if ok else "failed invariance"

anchors = [
    Anchor("recompute",  Tier.INVARIANT,   recompute),
    Anchor("prior-art",  Tier.PRIOR_ART,   prior_art_search),
    Anchor("adversary",  Tier.CROSS_MODEL, refute_with_a_different_model),
]

prereg = Preregister(question="...", anchors=[a.name for a in anchors])
prereg.freeze("prereg.json")                          # freeze before you look

loop = Loop(prereg, anchors, ledger="ledger.jsonl")
for c in candidates:
    loop.evaluate(c.name, payload=c)

print(loop.calibration_report())                      # survivors + kill-map
```

### The anchor-independence hierarchy

`looplab` will not let a result count as surviving unless it cleared something
above `SELF`:

| tier | example | independent of generator? |
|---|---|---|
| `INVARIANT` | a deterministic ground truth fixed by law/maths | yes |
| `CERTIFICATE` | a machine-checkable proof object (e.g. an SDP dual) | yes |
| `EXPERIMENT` | a measured, real-world consequence | yes |
| `PRIOR_ART` | the published record (already done?) | yes |
| `CROSS_MODEL` | a *different* model as adversary | partially |
| `SELF` | the generator judging itself | **no — never sufficient alone** |

## Why this exists

This harness is the distilled operating discipline from a quantum-chemistry
research pilot (see the parent repository). In that pilot ~14 candidate
directions were broad-cast and screened; 11 were retired against external
anchors — several of them by the prior-art anchor, exactly the `B` case above,
including one "strongest" direction that turned out to have been published 25
years earlier. The harness is what makes that screening reproducible and
auditable instead of a matter of opinion.

It is deliberately small and opinionated. It does not spawn agents or call models
— there are excellent tools for that. It does the one thing those tools leave
out: it makes it hard to fool yourself.

## Status

`v0.1` — core discipline, runnable demo, append-only ledger. Pure standard
library. Apache-2.0.
