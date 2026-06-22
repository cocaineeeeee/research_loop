"""looplab — an anchor-first research loop.

Generate candidates with a pluggable model, let an adversary refute them, verify
the survivors against an external non-fakeable anchor, keep an append-only audit
trail, iterate. The discipline (freeze the ruler, anchor every claim, never let
the model judge itself) is enforced in code.

    from looplab import ResearchLoop, Anchor, Tier
    from looplab.models import OpenAIModel, AnthropicModel, StubModel   # bring your own key
"""
from .core import Tier, Anchor, Verdict, Preregister, Loop, Result
from .engine import ResearchLoop, ResearchReport

__all__ = [
    "Tier", "Anchor", "Verdict", "Preregister", "Loop", "Result",
    "ResearchLoop", "ResearchReport",
]
__version__ = "0.3.0"
