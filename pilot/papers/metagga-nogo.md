# A two-body-cumulant witness for the non-injectivity of meta-GGA ingredients in strongly correlated states

**Claim.** The meta-GGA ingredient map `Ψ ↦ {ρ, ∇ρ, τ}` (density, gradient,
kinetic-energy density — the inputs to TPSS, SCAN, r²SCAN) is **non-injective** on strongly
correlated N-representable states. At fixed orbitals all three ingredients are functionals of
the 1-RDM, so two states with equal 1-RDMs present identical ingredients yet can carry
different energies. An explicit, machine-checkable witness pair of seniority-zero
four-electron states (stretched H₄, 4e/4o) has 1-RDMs equal to machine precision
(`‖Δγ‖_F = 0`) but Hamiltonian expectation values differing by `ΔE = 68.4 mHa`, forcing any
descriptor-only model to err by ≥34.2 mHa on one member. The distinguishing information is
**localized in the 2-RDM cumulant**.

**External check.** An explicit **machine-checkable counterexample**, not a fit:
- Three algebraic lemmas (seniority selection rule; equal-1-RDM covering symmetry;
  gap-as-pure-cumulant), each confirmed to machine zero on the actual H₄–H₁₄ Hamiltonians.
- Real-space grid-equality of `ρ, ∇ρ, τ` (max pointwise |A−B| = 0; ∫ρ = 4).
- Extensivity: the gap grows across stretched H₄–H₁₂ (linear fit R² = 0.999);
  upgraded to an **exact size-consistent theorem** in a decoupled-dimer model (per-dimer
  slope δ = −U, confirmed to 7×10⁻¹⁵ Ha by Jordan–Wigner exact diagonalization).
- Reproduced in CASCI active spaces of four real molecules (N₂, C₂, H₂O, BH).
- Weak-correlation control: the gap collapses below chemical accuracy (0.78 mHa) as the
  occupations detune toward (2,2,0,0).

**Honest status.** Submission-ready Letter (target: *PRL*); **not yet peer-reviewed**;
authors anonymized for review. **Boundary (explicit):** the underlying fact that the 1-RDM
does not fix the 2-RDM / energy is textbook; the contribution is its explicit quantification,
the meta-GGA-specific framing, and the cumulant localization. This is **not** a contradiction
of Hohenberg–Kohn, Gilbert, or Levy–Lieb DFT, and not a claim that the exact functional fails
to exist; energies are `⟨Ψ|H|Ψ⟩`, not exact correlation energies. No MC-PDFT (on-top
pair-density) no-go is claimed. Exact constant-slope linearity is proved only for the
idealized dimer model; for physical H-chains the claim is empirical extensive growth.

**Keywords.** density functional theory, meta-GGA, SCAN, TPSS, r²SCAN, strong correlation,
1-RDM, 2-RDM cumulant, N-representability, non-injectivity, Jacob's ladder, kinetic-energy
density, seniority zero, Gilbert theorem, FCI, hydrogen chains.
