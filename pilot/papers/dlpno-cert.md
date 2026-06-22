# A rigorous a posteriori certificate for the PNO-occupation truncation layer of DLPNO-MP2

**Claim.** A computable, rigorous, one-sided *a posteriori* upper bound on the
PNO-occupation truncation error of closed-shell RHF frozen-core MP2 in the
pair-natural-orbital (PNO) representation — the energy lost by discarding PNOs whose
occupation falls below the threshold `TCutPNO`. The MP2 Hylleraas functional is a
positive-definite (coercive) quadratic form, so the truncation error is *exactly* a
quadratic form in a computable Galerkin residual, `Δ = ⟨r⊥|A⁻¹|r⊥⟩`, evaluated in
closed form through the diagonal canonical denominators — with no solve of the discarded
amplitude equations. The primary deliverable is a component-resolved (symmetric /
antisymmetric spin-channel) evaluation that is *exact*; a flat closed-form corollary with
proven constant `C = 3` is ~2× loose.

**External check.**
- **47-system, 188-row production benchmark** (polar hydrides; strongly correlated /
  near-degenerate N₂, C₂, F₂, O₃, C₂H₄; weak dimers; ions; 2nd/3rd-row heavy elements;
  cc-pVTZ subset): **zero violations** of the bound on every system × threshold × pair.
- Component-resolved bound: **1.00× tightness on all 159 resolvable rows**; flat `C=3`
  bound median 2.19× (range 1.28–3.00×).
- Anchor is full canonical MP2 (PySCF `mp.MP2`), reproduced in-house to ≤2.3×10⁻¹⁵ Ha.
- Head-to-head vs. the incumbent CPS extrapolation over 534 comparisons: CPS
  *underestimates* the true error in 46% and gets the sign wrong in 48%; the certificate is
  a rigorous upper bound on 534/534 (100%).

**Honest status.** Submission-ready manuscript (target: *JCTC*); **not yet peer-reviewed**;
authors anonymized for review. Scope is deliberately bounded: certifies the
**PNO-occupation layer only**, not pair-prescreening or PAO-domain layers; bounds the
truncation error relative to full-PNO MP2, **not** the MP2 method error vs. FCI; a coercivity
no-go means it does **not** extend to non-variational CCSD. The acene cost trend is a
3-point indicative study, not a scaling proof. Full manuscript and reproduction code
available on request; to be archived (Zenodo concept DOI) on release.

**Keywords.** quantum chemistry, local correlation, DLPNO, MP2, pair natural orbitals,
error certificate, a posteriori error bound, coercivity, Hylleraas functional, Galerkin
truncation, CPS extrapolation, PySCF, closed-shell RHF, frozen core.
