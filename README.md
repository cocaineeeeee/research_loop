# Research as an Engineered Loop

**A working discipline for doing science when reasoning, compute, and hypothesis-generation have all become cheap — and an honest map of where it breaks.**

When inference and compute stop being the bottleneck, the *value* of research relocates. It does not disappear; it collapses onto the few things that cannot be commoditized: a **non-fakeable filter**, an **independent adversary**, and **human reach**. This repository is a pilot that builds that loop, runs it hard on a real problem (strongly correlated electronic structure), and reports — with the same honesty the method demands — exactly where it stops working.

> This is not a claim that research has been "redefined." It is an operating discipline, stress-tested on one domain, with its ceiling measured. The honesty about the ceiling is the point.

---

## The thesis in four principles

**1 — From a line to a filter.**
A single researcher traces *one trajectory* through knowledge space: serial, depth-first, one hypothesis at a time. With a fleet of agents the operation changes shape — broad-cast *many* candidates across a region of the space in parallel, then **filter**. The unit of work stops being "develop the one idea" and becomes "screen the region." Generation parallelizes; value moves downstream.

**2 — The value collapses onto the eval.**
A loop only amplifies what its evaluator rewards. If the evaluator is fakeable, the loop becomes a high-gain amplifier of plausible nonsense. So the load-bearing component is a **non-fakeable kill-ruler** — one that bottoms out in something the system cannot rewrite. Anchors form a hierarchy by independence:

> physical invariant / deterministic ground truth → machine-checkable certificate → experiment / real-world consequence → the prior-art record → cross-model adversary → *self-judgement (zero independence — forbidden)*

Every surviving claim must trace to an artifact at one of the upper tiers. No orphan claims.

**3 — Truth needs an adversary, not a judge.**
A model cannot reliably mark its own work. The loop therefore separates **generator** from **adversary**: a *different* intelligence whose incentive is to break the claim — refute the logic, check whether it has already been done, red-team the framing — refereed by the external anchor. Independence is everything: a human or an external anchor is maximally independent; a second model is partially independent; self-review is not independent at all.

**4 — The loop has edges, and the human is the one who extends them.**
The loop is powerful and bounded. It is bounded by **the generator's reach** (it can only filter what it can sample — and a model samples the *known* distribution, so the genuinely novel stays out of reach); by **the eval's cost** (rigorous verification scales steeply, capping the size of what can be certified); by **the commons** (a high-throughput loop that exhausts shared resources terminates itself); and by **the absence of a stop rule** (a loop with no convergence criterion burns compute on diminishing returns). The irreplaceable human roles are exactly the four things the loop cannot do for itself: be the eval of last resort, be the most independent adversary, govern the resource, and **extend the reach** by injecting information the public distribution does not contain.

---

## The pilot: what the loop actually did

The discipline was run on a concrete, unforgiving domain — certified bounds for strongly correlated quantum many-body systems, where the external anchor is a physical invariant (an energy that is provably fixed by the Hamiltonian and cannot be argued with).

**Broad-cast → filter, in numbers.** ~14 discovery-shaped directions were generated and screened against external anchors and the prior-art record.

| outcome | count | what it means |
|---|---:|---|
| **Retired (clean kill)** | 11 | each fell to a *nameable* failure mode — already published, provably impossible, equivalent to a known result, benchmark-in-disguise, or structurally vacuous |
| **Advanced** | 3 | survived the filter; under active development |
| **Yield (manuscripts)** | 3 | submission-ready results that cleared every gate |

The 11 retirements are not waste — together they are a **boundary map** of the explored region (what is already known, already impossible, or already equivalent). Mapping the boundary honestly is a deliverable, not a failure.

**The kill-map (selected).** Every direction was retired against an external anchor, never against opinion:

| direction (abstracted) | retired because | failure mode |
|---|---|---|
| extend an impossibility result to the time domain | already in the literature | prior-art |
| separate states via an ensemble construction | ground state is a vertex of the convex set | provably impossible |
| a "new" correlation propagation cone | collapses to a known bound under an honest threshold | equivalent-to-known |
| a coupling-from-spectrum non-identifiability no-go | published 25 years earlier (isospectral families) | prior-art |
| a quantized topological order parameter from correlations | the invariant is identically zero for real systems | structurally vacuous |

*(The adversary — an independent model running prior-art checks — is what caught the prior-art kills. Self-review would have kept several of them alive.)*

**The yield (three manuscripts, honest status).**

- **A computable, rigorous error certificate for a local-correlation truncation.** Turns an empirically-calibrated approximation into one with a guaranteed, machine-verifiable error bound. *Status: submission-ready manuscript; results verified on a 47-system benchmark, zero violations.*
- **A non-injectivity result for a widely-used class of density-functional ingredients.** A clean, falsifiable witness that a standard descriptor set cannot resolve strong-correlation energy — with an explicit, machine-checkable counterexample, and a careful statement of what it does *not* claim. *Status: submission-ready manuscript.*
- **Certified intervals for quantities reconstructed from experimental data.** Replaces a single best-fit with a provable [lower, upper] bracket via a machine-checkable certificate. *Status: submission-ready manuscript.*

---

## Where it breaks (the measured ceiling)

The most useful output of the pilot is its own limit, established by the same adversarial method.

- **It triages the known region near-perfectly and reaches the genuinely-new almost never.** The retirements cluster on "already known / already impossible." A generator that samples the public distribution filters densely over explored territory and thinly over the rest. *Breakthrough-shaped results require information the public distribution does not contain* — private data, an experiment, a new anchor, or a problem chosen from real-world failure. The loop relocates the hard problem; it does not dissolve it.
- **The verification cost caps the scale.** Rigorous anchors are expensive; the certifiable frontier is small-system-bounded.
- **More agents buy width, not independence.** Copies of one model share blind spots. Robustness comes from *different* intelligences (cross-model, human, anchor), not from throughput.

This ceiling is not a disclaimer bolted on at the end. It is the result.

---

## Why this is the right shape for the moment

The components of the loop sort cleanly into commodity and scarce:

| commodity (cheap, parallel, improving fast) | scarce (load-bearing) |
|---|---|
| hypothesis generation | a **non-fakeable** evaluator |
| inference / agent throughput | an **independent** adversary |
| most verification compute | **human reach** (taste, problem-selection, the brake) |

The bet of this repository is that as the left column keeps getting cheaper, *all* of the value flows to the right column — and that a research practice should be engineered around the right column, not the left.

---

## Contents

- `papers/` — the three manuscripts (preprints + reproducible code and data).
- `screening/` — the full discovery kill-map and the rationale for each retirement.
- `method/` — the operating discipline: the broad-cast / adversary / non-fakeable-eval loop, the preregistration and calibration templates, and the resource-governance rules.
- `notes/` — the post-mortem on the measured ceiling.

*Every quantitative claim traces to a raw artifact in this repository. Items marked "submission-ready" are manuscripts, not yet peer-reviewed; status labels are kept literal on purpose.*

---

*Author and contact details withheld for now.*
