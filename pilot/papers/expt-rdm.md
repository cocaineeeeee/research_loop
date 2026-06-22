# Certified intervals for quantum crystallography: bounding electronic observables over the N-representable feasible set

**Claim.** Reconstructing the 1-RDM from experimental scattering data is an
underdetermined inverse problem. Instead of reporting a single regularized best-fit 1-RDM
(prior art), this work **bounds a derived electronic observable over the entire feasible
set**. For a linear functional `f(γ) = Tr(Fγ)` and the feasible set
`{γ : 0 ⪯ γ ⪯ 2I, Tr γ = N, Tr(Aₖγ) = dₖ}` (ensemble N-representability + data),
solving **two SDPs** (min and max of f) gives a certified interval `[f_LB, f_UB]` guaranteed
to contain the true value for *any* state consistent with the data. The interval is a
rigorous consequence of the constraints, not a confidence band, and cannot be made
artificially narrow.

**External check.** An **SDP duality / convex-feasibility certificate**, demonstrated on three
real crystals with reciprocal-space structure factors (urea, Ne fcc, LiH rock salt), each
from an all-electron periodic ab initio calculation with analytic structure factors:
- the certified kinetic-energy interval **always brackets the periodic exact value** and
  **narrows monotonically** as reflection shells are added (Ne fcc: 1.6×10² → 5×10⁻⁷ Ha
  across 125 reflections);
- under additive Gaussian structure-factor noise the interval **widens but never escapes the
  truth**;
- all five sanity gates PASS for all three crystals.

**Honest status.** Submission-ready manuscript (target: *IUCrJ* / Acta Cryst. A; fallback
PRA/JCTC); **not yet peer-reviewed**; authors anonymized for review. **Boundaries
(explicit):** the structure factors are **realistic *simulated*** values from periodic ab
initio, **not** measured intensities — real diffraction data is the pending upgrade; this is
a bridge, not the endpoint. Energy intervals are not at chemical accuracy on sparse data.
**Credit/scoop stated up front:** the SDP-with-N-representability 1-RDM *best-fit*
reconstruction is prior art (De Bruyne–Gillet / Yu–Gillet); the abstract
SDP→certified-bound machine was reported concurrently in quantum information
(Mortimer/Acín, arXiv:2601.10408). The increment is the first use of certified [min, max]
intervals in quantum crystallography.

**Keywords.** quantum crystallography, 1-RDM reconstruction, N-representability, semidefinite
programming, SDP, certified bounds, structure factors, inverse problem, kinetic energy, urea,
neon, lithium hydride, X-ray scattering, electron density, CVXPY.
