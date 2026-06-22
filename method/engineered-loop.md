# Research as an engineered loop

`looplab` is small on purpose. This note is the idea it enforces.

When reasoning, compute, and hypothesis-generation all become cheap, the *value* of research does not vanish — it relocates onto the few things that cannot be commoditized. The claim here is specific, and the [pilot](../pilot/) is the test of it, including an honest map of where it fails.

> This is an operating discipline, stress-tested on one domain. It is **not** a claim that research has been "redefined." The honesty about the ceiling (last section) is part of the result.

## 1 — From a line to a filter

A single researcher traces *one trajectory* through knowledge space: serial, depth-first, one hypothesis at a time. With a fleet of agents the operation changes shape — broadcast *many* candidates across a region in parallel, then **filter**. The unit of work stops being "develop the one idea" and becomes "screen the region." Generation parallelizes; value moves downstream to the filter.

## 2 — The value collapses onto the evaluator

A loop only amplifies what its evaluator rewards. If the evaluator is fakeable, the loop is a high-gain amplifier of plausible nonsense. So the load-bearing component is a **non-fakeable evaluator** — one that bottoms out in something the system cannot rewrite. Anchors form a hierarchy by independence:

> physical invariant / deterministic ground truth → machine-checkable certificate → experiment → prior-art record → cross-model adversary → *self-judgement (zero independence)*

A claim's credibility is bounded by the highest *independent* anchor it clears. Every surviving claim must trace to an artifact. No orphan claims.

## 3 — Truth needs an adversary, not a judge

A model cannot reliably mark its own work. The loop separates **generator** from **adversary**: a *different* intelligence whose incentive is to break the claim — refute the logic, check whether it has already been done, red-team the framing — refereed by the external anchor. In the pilot, the adversary (an independent model running prior-art checks) is what caught every "already published" kill; self-review would have kept several alive.

## 4 — The substrate and the fuel

- **Multi-agent fleet** is what turns the line into a sweep: width, role specialization (generators, adversaries, scouts, verifiers), and *N* independent voters. Caveat: copies of one model share blind spots — more agents buy width, not independence.
- **Two kinds of compute.** Inference compute is the breadth of the broadcast. *Verification* compute is the evaluator's teeth: the kill-ruler is non-fakeable precisely because it is a real computation against an external invariant, not a model's say-so.

## The edges (the measured ceiling)

The loop is powerful and bounded, and the bounds are the honest part:

- **Reach.** It can only filter what the generator can sample. A model samples the *known* distribution, so it triages explored territory densely and reaches the genuinely-new almost never. Breakthrough-shaped results need information the public distribution does not contain — private data, an experiment, a new anchor, a problem chosen from real failure.
- **Cost.** Rigorous verification scales steeply; the certifiable frontier is small.
- **The commons.** A high-throughput loop that exhausts shared resources terminates itself; resource governance is part of the engineering.
- **Termination.** A loop with no stop rule burns compute on diminishing returns.

The irreplaceable human roles are exactly the four things the loop cannot do for itself: be the evaluator of last resort, be the most independent adversary, govern the resource, and **extend the reach**.

## What is commodity, what is scarce

| commodity (cheap, parallel, improving) | scarce (load-bearing) |
|---|---|
| hypothesis generation | a **non-fakeable** evaluator |
| inference / agent throughput | an **independent** adversary |
| most verification compute | **human reach** — taste, problem-selection, the brake |

As the left column keeps getting cheaper, the value flows to the right. `looplab` is an attempt to engineer the right column into the daily loop.
