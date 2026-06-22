"""
ResearchLoop — the engineered research loop, with a pluggable model.

This runs the cycle the way a careful researcher (or research agent) does it:

    generate candidates  ->  adversary tries to refute / prior-art them
                         ->  external anchors verify the survivors
                         ->  record everything, harvest, iterate until dry

The model (generator) and the adversary are pluggable backends — bring your own
API key (see looplab.models). The **anchors are yours**: real computations or
checks for your domain. That is the non-fakeable part. The engine never lets the
model's own say-so decide a result — only an independent anchor can (the
discipline is inherited from looplab.core).

    from looplab import ResearchLoop, Tier, Anchor
    from looplab.models import AnthropicModel, OpenAIModel

    engine = ResearchLoop(
        question="propose orbital transforms that lower selected-CI cost",
        model=AnthropicModel(model="claude-sonnet-4-6"),     # generator
        adversary=OpenAIModel(model="gpt-5.5"),              # a *different* model
        anchors=[Anchor("cost_vs_FCI", Tier.INVARIANT, my_real_evaluator)],
        max_rounds=4,
    )
    report = engine.run()
    print(report.summary())
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field

from .core import Anchor, Preregister, Loop, Result, Tier


def _extract_json(text: str, fallback):
    """Pull the first JSON value out of a model response; tolerate prose around it."""
    for pat in (r"\[.*\]", r"\{.*\}"):
        m = re.search(pat, text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return fallback


GEN_PROMPT = """You are a research generator. GENERATE up to {n} distinct, concrete,
testable candidate approaches to the following question. Be specific and falsifiable.

QUESTION: {question}

Already tried (do not repeat): {seen}

Return ONLY a JSON list of short strings, one per candidate."""

REFUTE_PROMPT = """You are an adversary. Try to REFUTE the candidate below, or flag it as
already-known prior art. Be skeptical; default to refuted=true if it is vacuous, already
published, or logically broken.

QUESTION: {question}
CANDIDATE: {candidate}

Return ONLY JSON: {{"refuted": true|false, "reason": "..."}}"""


@dataclass
class ResearchReport:
    question: str
    rounds: int
    survivors: list[str]
    killed: list[dict]            # {candidate, by, reason}
    ledger_path: str

    def summary(self) -> str:
        out = [f"Question: {self.question}",
               f"Rounds: {self.rounds} | survivors: {len(self.survivors)} | killed: {len(self.killed)}",
               "", "Survivors (cleared an independent external anchor):"]
        out += [f"  + {s}" for s in self.survivors] or ["  (none)"]
        out += ["", "Killed (with reason):"]
        out += [f"  - {k['candidate']}  [{k['by']}] {k['reason']}" for k in self.killed] or ["  (none)"]
        out += ["", f"Audit trail: {self.ledger_path}"]
        return "\n".join(out)


class ResearchLoop:
    def __init__(self, question, model, anchors, *, adversary=None,
                 max_rounds=3, per_round=4, ledger="research_ledger.jsonl"):
        if not anchors:
            raise ValueError("Supply at least one external anchor — the non-fakeable verifier "
                             "for your domain. Without it the loop cannot certify anything.")
        self.question = question
        self.model = model
        self.adversary = adversary
        self.anchors = anchors
        self.max_rounds = max_rounds
        self.per_round = per_round
        self.prereg = Preregister(question=question, anchors=[a.name for a in anchors])
        self.prereg.freeze(ledger.replace(".jsonl", "_prereg.json"))
        self.loop = Loop(self.prereg, anchors, ledger=ledger)
        self.ledger = ledger

    def _generate(self, seen):
        raw = self.model.complete(GEN_PROMPT.format(
            n=self.per_round, question=self.question, seen=list(seen) or "none"))
        cands = _extract_json(raw, fallback=[l.strip("-* ") for l in raw.splitlines() if l.strip()])
        return [str(c).strip() for c in cands if str(c).strip()][: self.per_round]

    def _refute(self, candidate):
        if not self.adversary:
            return (False, "")
        raw = self.adversary.complete(REFUTE_PROMPT.format(
            question=self.question, candidate=candidate))
        v = _extract_json(raw, fallback={"refuted": False, "reason": ""})
        return (bool(v.get("refuted")), str(v.get("reason", "")))

    def run(self) -> ResearchReport:
        seen, survivors, killed = set(), [], []
        rounds = 0
        for rounds in range(1, self.max_rounds + 1):
            cands = [c for c in self._generate(seen) if c not in seen]
            if not cands:
                break                                   # dry: nothing new to try
            for c in cands:
                seen.add(c)
                refuted, reason = self._refute(c)
                if refuted:                              # adversary (cross-model) kill
                    killed.append({"candidate": c, "by": "adversary", "reason": reason})
                    continue
                res = self.loop.evaluate(c)              # external anchors decide (non-fakeable)
                if res.survived:
                    survivors.append(c)
                else:
                    killed.append({"candidate": c, "by": "anchor", "reason": res.retired_because})
        return ResearchReport(self.question, rounds, survivors, killed, self.ledger)
