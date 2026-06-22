"""
looplab.core — an anti-self-deception harness for AI-accelerated research.

The unit of work in AI-accelerated research is shifting from "develop one idea"
to "broad-cast many candidates and filter them." When generation is cheap, the
load-bearing component is the *filter*: an evaluation that cannot be faked. This
module enforces, as code, the discipline that makes such a filter trustworthy:

  1. Pre-register the ruler (anchors + thresholds) and freeze it *before* looking
     at results. Changing it afterwards is recorded as goalpost-moving.
  2. Every verdict must carry an evidence artifact. No orphan claims.
  3. A candidate may not be marked SURVIVED on self-judgement alone — the highest
     anchor that passed it must be independent of the generator.
  4. The ledger is append-only: a complete audit trail.

The harness is domain-agnostic. You supply the candidates and the anchors (the
external checks for *your* field); the harness enforces the discipline.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from enum import IntEnum
from pathlib import Path
from typing import Callable, Iterable


# --------------------------------------------------------------------------- #
# Anchor independence hierarchy. Higher = more independent of the generator.
# A claim's credibility is bounded by the highest *independent* anchor it clears.
# --------------------------------------------------------------------------- #
class Tier(IntEnum):
    SELF = 0            # the generator judging itself — never sufficient alone
    CROSS_MODEL = 1     # a different model as adversary — partially independent
    PRIOR_ART = 2       # the published record (has this already been done?)
    EXPERIMENT = 3      # a real-world / measured consequence
    CERTIFICATE = 4     # a machine-checkable proof object (e.g. an SDP dual)
    INVARIANT = 5       # a deterministic ground truth fixed by law/maths

    @property
    def independent(self) -> bool:
        """SELF is not independent of the generator; everything above is."""
        return self >= Tier.CROSS_MODEL


@dataclass
class Verdict:
    """Result of one anchor checking one candidate."""
    anchor: str
    tier: Tier
    passed: bool
    evidence: str                 # path / URL / hash of the raw artifact — REQUIRED
    detail: str = ""

    def __post_init__(self) -> None:
        if not self.evidence:
            raise ValueError(
                f"Anchor '{self.anchor}' returned a verdict with no evidence "
                f"artifact. No orphan claims: every verdict must point to a raw "
                f"output (file path, URL, or content hash)."
            )


@dataclass
class Anchor:
    """An external, non-fakeable check supplied by the user for their domain.

    `check` takes a candidate and returns (passed, evidence, detail). `evidence`
    must be a pointer to a raw artifact — the thing a skeptic could re-inspect.
    """
    name: str
    tier: Tier
    check: Callable[[object], tuple]

    def run(self, candidate: object) -> Verdict:
        passed, evidence, *rest = self.check(candidate)
        return Verdict(self.name, self.tier, bool(passed), str(evidence),
                       detail=(rest[0] if rest else ""))


# --------------------------------------------------------------------------- #
# Pre-registration: freeze the ruler before looking at the data.
# --------------------------------------------------------------------------- #
@dataclass
class Preregister:
    question: str
    anchors: list[str]                       # anchor names that constitute the ruler
    thresholds: dict = field(default_factory=dict)
    notes: str = ""
    frozen_at: float | None = None
    fingerprint: str | None = None

    def freeze(self, path: str | Path) -> str:
        """Hash and timestamp the ruler. The fingerprint is the anti-goalpost-
        moving seal: if the ruler later differs, the mismatch is detectable."""
        body = json.dumps(
            {"question": self.question, "anchors": sorted(self.anchors),
             "thresholds": self.thresholds, "notes": self.notes},
            sort_keys=True,
        )
        self.fingerprint = hashlib.sha256(body.encode()).hexdigest()[:16]
        self.frozen_at = time.time()
        Path(path).write_text(json.dumps(asdict(self), indent=2))
        return self.fingerprint


# --------------------------------------------------------------------------- #
# The loop: run candidates through the frozen ruler, with provenance.
# --------------------------------------------------------------------------- #
@dataclass
class Result:
    candidate: str
    verdicts: list[Verdict]

    @property
    def survived(self) -> bool:
        """SURVIVED requires at least one *independent* anchor to pass and no
        independent anchor to fail. SELF verdicts (the generator judging itself)
        are recorded but never decide — neither to pass nor to reject."""
        independent = [v for v in self.verdicts if v.tier.independent]
        independent_pass = [v for v in independent if v.passed]
        independent_fail = [v for v in independent if not v.passed]
        return bool(independent_pass) and not independent_fail

    @property
    def top_independent_tier(self) -> Tier | None:
        passed = [v.tier for v in self.verdicts if v.passed and v.tier.independent]
        return max(passed) if passed else None

    @property
    def retired_because(self) -> str:
        # Only an independent anchor's failure is a reason to retire; SELF never decides.
        fails = [v for v in self.verdicts if not v.passed and v.tier.independent]
        if fails:
            return f"{fails[0].anchor}: {fails[0].detail}".strip().rstrip(":")
        if not any(v.passed and v.tier.independent for v in self.verdicts):
            return "no independent anchor passed — not independently verified"
        return ""


class Loop:
    """Append-only screening loop. Records every verdict to a ledger."""

    def __init__(self, prereg: Preregister, anchors: list[Anchor],
                 ledger: str | Path = "ledger.jsonl"):
        if prereg.fingerprint is None:
            raise RuntimeError("Pre-register must be frozen before running the loop.")
        declared = sorted(prereg.anchors)
        supplied = sorted(a.name for a in anchors)
        if declared != supplied:
            # The ruler changed after freezing — surface it loudly.
            raise RuntimeError(
                f"Ruler changed after freeze (goalpost-moving guard).\n"
                f"  pre-registered anchors: {declared}\n"
                f"  supplied anchors:       {supplied}"
            )
        self.prereg = prereg
        self.anchors = anchors
        self.ledger_path = Path(ledger)
        self.results: list[Result] = []

    def evaluate(self, candidate: str, payload: object = None) -> Result:
        verdicts = [a.run(payload if payload is not None else candidate)
                    for a in self.anchors]
        res = Result(candidate, verdicts)
        self._append(res)
        self.results.append(res)
        return res

    def _append(self, res: Result) -> None:
        row = {
            "t": time.time(),
            "ruler": self.prereg.fingerprint,
            "candidate": res.candidate,
            "survived": res.survived,
            "top_independent_tier": (res.top_independent_tier.name
                                     if res.top_independent_tier else None),
            "verdicts": [
                {"anchor": v.anchor, "tier": v.tier.name, "passed": v.passed,
                 "evidence": v.evidence, "detail": v.detail}
                for v in res.verdicts
            ],
        }
        with self.ledger_path.open("a") as f:
            f.write(json.dumps(row) + "\n")

    # ----- reporting -------------------------------------------------------- #
    def survivors(self) -> list[Result]:
        return [r for r in self.results if r.survived]

    def kill_map(self) -> list[dict]:
        """Negative results are a boundary map, not waste."""
        return [{"candidate": r.candidate, "retired_because": r.retired_because}
                for r in self.results if not r.survived]

    def calibration_report(self) -> str:
        n = len(self.results)
        surv = self.survivors()
        lines = [
            f"Ruler {self.prereg.fingerprint} | candidates screened: {n}",
            f"  survived (independently anchored): {len(surv)}",
            f"  retired: {n - len(surv)}",
            "",
            "Survivors (with highest independent anchor cleared):",
        ]
        for r in surv:
            lines.append(f"  + {r.candidate}  [{r.top_independent_tier.name}]")
        lines.append("")
        lines.append("Kill-map (boundary of the explored region):")
        for k in self.kill_map():
            lines.append(f"  - {k['candidate']}  ->  {k['retired_because']}")
        return "\n".join(lines)
