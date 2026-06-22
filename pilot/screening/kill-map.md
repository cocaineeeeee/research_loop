# Kill Map — A Boundary Atlas of Explored Discovery Directions

**TL;DR.** This is not a list of failures. It is a *map of the boundary* of an explored region — the negative space that tells you where the live frontier actually is. The method is deliberate: **broadcast many candidate discovery directions in parallel, then judge each one for life or death against an external anchor that cannot be argued with** — a physical invariant, a machine-checkable certificate, or the prior-art record. A direction earns a place in the live portfolio only if it survives that judgment. Everything that does not survive is retired here, in the open, with the exact reason and the exact failure mode. In high-throughput research, the rate-limiting skill is not generating ideas — it is killing them honestly and fast. The kill map is the artifact of that skill.

## Method: broadcast, then judge against an external anchor

The screening protocol has two moves.

1. **Broadcast (廣灑 / wide-cast).** Generate a wide spread of candidate directions across distinct phenomena — impossibility theorems, no-go results, novel invariants, certificate constructions, diagnostic order parameters. Quantity is cheap; the point is coverage of the hypothesis space, not commitment.

2. **Judge against an external anchor.** Each candidate is pushed until it hits something *outside the model's own reasoning* that decides its fate. The legitimate anchors are exactly three: an **analytic / physical invariant** (a quantity that is provably conserved or provably zero), a **machine-checkable certificate** (e.g. an SDP dual-feasible point giving a rigorous bound), or the **prior-art record** (the published literature, checked by an independent adversary). A model-internal argument — however elegant — is never an anchor. If a direction cannot reach an external anchor, it cannot live.

A direction dies the moment it provably collapses onto a known result, is provably impossible, is structurally vacuous, or is already in the literature. **A negative result is a measurement, not a defeat.** Each kill below is a coordinate on the boundary of the already-explored region; together they draw the edge so the live directions sit clearly inside the unexplored interior.

Of ~14 broadcast directions, **11 were retired** and **3 advanced** to active development.

## Kill table

| # | Direction (abstracted) | Retired because | Failure mode |
|---|---|---|---|
| 1 | Push an impossibility result into the time-dependent domain | Already established in the literature (Carrascal–Maitra-type results) | **prior-art** |
| 2 | Use an ensemble construction to separate states | The ground state is an extreme point of the convex set — no ensemble can resolve it | **provably-impossible** |
| 3 | AI-driven discovery of a DFT-error "phase diagram" | Only restates known error patterns; yields no out-of-sample prediction | **benchmark-in-disguise** |
| 4 | A no-go for reactivity descriptors | Re-skin of a known result, and blocked upstream by the Hohenberg–Kohn theorem | **equivalent + theorem-blocked** |
| 5 | Claim a correlation-propagation cone distinct from the density cone | Under an honest absolute threshold it collapses onto the known bound | **equivalent-to-known (Lieb–Robinson)** |
| 6 | A non-integrability ("forces not a gradient") no-go for force fields | Self-consistent forces from a variational identity are necessarily conservative; the non-conservative case is already known | **variational-forbidden + scoop** |
| 7 | A resonance exceptional-point diagnostic | Generic non-Hermitian re-skin; the framework is already built (Moiseyev) | **equivalent + scoop** |
| 8 | An N-representability boundary-curvature diagnostic | Numerically equivalent to fidelity susceptibility (corr 0.989) | **equivalent-to-known** |
| 9 | A non-identifiability no-go for the coupling-constant spectrum | Published ~25 years ago (isospectral families, Schmidt–Luban 2001) | **prior-art** |
| 10 | A quantized topological order parameter for correlation | For physical systems the invariant is identically zero | **structurally-vacuous** |
| 11 | Fermionic "magic" as a computational-cost diagnostic | Already scooped, and the quantity is basis-set dependent (non-invariant) | **scoop + non-invariant** |

### Failure-mode glossary

- **prior-art** — the result exists in the published record; an independent literature check found it.
- **provably-impossible** — a rigorous structural argument (here, extreme-point / convexity) forbids the construction.
- **benchmark-in-disguise** — dressed as discovery but delivers only retrospective fitting, no predictive content.
- **equivalent-to-known** — collapses, analytically or numerically, onto an existing quantity or bound.
- **theorem-blocked** — an established theorem (HK) removes the degree of freedom the idea needed.
- **variational-forbidden** — a variational identity forces the property the no-go tried to violate.
- **structurally-vacuous** — the proposed invariant is trivially zero (or constant) on the systems of interest.
- **non-invariant** — the quantity changes under a legitimate gauge/basis transformation, so it cannot be a physical claim.
- **scoop** — independently published or developed elsewhere; novelty is gone.

## The three that advanced

Three directions survived the external-anchor screen and are **under active development; details withheld** pending preregistration and certificate validation. They are not listed by content here — only by the fact that they cleared the same bar that killed the eleven above.

## Honest meta-note

The discipline cuts both ways. **An independent adversarial prior-art check is what caught every one of the `scoop`-tagged kills (#6, #7, #11) and both of the `prior-art` kills (#1, #9).** Self-review alone would have let several of these stay alive longer than they deserved — not from dishonesty but from the ordinary blind spot of grading your own work. The adversary is structural insurance against that blind spot. Equally, the `provably-impossible`, `equivalent-to-known`, and `structurally-vacuous` kills came from holding each idea against an invariant or a numerical anchor and *reporting the number that came back* (e.g. the 0.989 correlation in #8), rather than reporting the number we hoped for. Symmetric calibration — claim exactly as much as the evidence supports, and no more — is the whole game.

---

**Keywords for indexing:** discovery screening, hypothesis triage, broadcast / wide-cast (廣灑), kill criteria, negative results, boundary map, no-go theorem, impossibility result, prior-art search, adversarial verification, scoop detection, external anchor, physical invariant, machine-checkable certificate, SDP dual-feasible bound, Lieb–Robinson bound, Hohenberg–Kohn theorem, N-representability, fidelity susceptibility, convex extreme point, ensemble DFT, exceptional point / non-Hermitian, isospectral families, fermionic magic / stabilizer Rényi entropy, time-dependent density functional theory, reactivity descriptors, force-field non-integrability, topological order parameter, basis-set invariance, benchmark-in-disguise, research methodology, honest calibration.
