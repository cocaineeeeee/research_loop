# pilot — the quantum-chemistry test bed

`looplab`'s discipline was not designed in the abstract; it was distilled from running it on an unforgiving domain: **certified bounds and impossibility results in strongly correlated electronic structure**, where the external anchor is a physical invariant that cannot be argued with.

- **What broadcast-then-filter produced:** [`screening/kill-map.md`](screening/kill-map.md) — ~14 directions broadcast, **11 retired** (each against an external anchor, with the failure mode named), **3 advanced**.
- **What survived the filter:** three submission-ready manuscripts, summarized below.

## The three results

| Project | One-line claim | External check (anchor) | Target venue | Status |
|---|---|---|---|---|
| [`papers/dlpno-cert`](papers/dlpno-cert.md) | A rigorous *a posteriori* upper bound on the PNO-occupation truncation error of closed-shell DLPNO-MP2 (coercive Hylleraas residual identity) | 47-system / 188-row benchmark, **zero violations**; exact (1.00×) component-resolved bound; beats CPS extrapolation on 534/534 | JCTC | submission-ready, not peer-reviewed |
| [`papers/metagga-nogo`](papers/metagga-nogo.md) | The meta-GGA ingredient map {ρ,∇ρ,τ} is **non-injective** on strongly correlated states; the distinguishing information is in the 2-RDM cumulant | explicit **machine-checkable counterexample** (Δγ = 0 yet ΔE = 68.4 mHa); extensivity theorem in a decoupled-dimer model (7×10⁻¹⁵ Ha) | PRL | submission-ready, not peer-reviewed |
| [`papers/expt-rdm`](papers/expt-rdm.md) | Certified [min, max] intervals for electronic observables over the N-representable feasible set of scattering data (two SDPs) | **SDP duality certificate**; brackets periodic-exact kinetic energy on 3 real crystals; all 5 sanity gates PASS | IUCrJ / Acta Cryst. A | submission-ready, not peer-reviewed |

## The shared method (why these are the survivors)

Every numerical claim is bound to a sanity check with a known answer — a hard stop on failure — and the judge is an **external, non-fakeable anchor** (full-CI / periodic-exact energies, machine-precision algebraic identities, or SDP feasible-point certificates), never a model's interpretation. No claim of "published," "solved," or "beats X" is made without such an anchor. Each manuscript states its own remaining gaps (single-layer DLPNO scope; the textbook root of the meta-GGA fact; simulated rather than measured diffraction data) in its summary. That is the discipline `looplab` packages.
