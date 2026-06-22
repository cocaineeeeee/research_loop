"""looplab — an anti-self-deception harness for AI-accelerated research.

Broad-cast many candidates; filter them through external, non-fakeable anchors;
keep a complete audit trail. The discipline is enforced in code, not in prose.
"""
from .core import (
    Tier, Anchor, Verdict, Preregister, Loop, Result,
)

__all__ = ["Tier", "Anchor", "Verdict", "Preregister", "Loop", "Result"]
__version__ = "0.1.0"
