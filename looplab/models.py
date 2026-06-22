"""
Pluggable model backends. Bring your own API key.

A backend only needs to implement `complete(prompt) -> str`. The research engine
builds generation and refutation on top of that single method, so any provider
(or a local model, or a deterministic stub for testing) drops in unchanged.

    from looplab.models import AnthropicModel, OpenAIModel, StubModel
    gen = AnthropicModel(api_key=..., model="claude-sonnet-4-6")
    adv = OpenAIModel(api_key=..., model="gpt-5.5")        # a *different* model = independent adversary
"""
from __future__ import annotations
import json
import os
from typing import Callable


class Model:
    """Backend interface. Implement `complete`."""
    name: str = "model"

    def complete(self, prompt: str, *, temperature: float = 0.7, max_tokens: int = 1024) -> str:
        raise NotImplementedError


class StubModel(Model):
    """Deterministic, dependency-free backend for tests/demos with no API key.

    Either pass a `responder(prompt)->str`, or a fixed list of candidate strings
    it will emit (as JSON) when asked to generate.
    """
    name = "stub"

    def __init__(self, responder: Callable[[str], str] | None = None,
                 candidates: list[str] | None = None):
        self._responder = responder
        self._candidates = candidates or []

    def complete(self, prompt: str, *, temperature: float = 0.7, max_tokens: int = 1024) -> str:
        if self._responder:
            return self._responder(prompt)
        # Default behaviour: on a "generate" prompt, emit the canned candidates.
        if "GENERATE" in prompt and self._candidates:
            return json.dumps(self._candidates)
        # On a "refute" prompt, never refute (let the external anchor decide).
        return json.dumps({"refuted": False, "reason": ""})


class _HTTPModel(Model):
    """Shared helper: a model reached over HTTP via the stdlib (no SDK needed)."""
    def __init__(self, api_key: str | None, model: str, base_url: str, env_key: str):
        self.api_key = api_key or os.environ.get(env_key, "")
        self.model = model
        self.base_url = base_url
        self.name = model
        if not self.api_key:
            raise ValueError(
                f"No API key. Pass api_key=... or set ${env_key}. "
                f"(For offline tests use StubModel.)"
            )

    def __repr__(self):  # never expose the key in logs / reprs / tracebacks
        return f"{type(self).__name__}(model={self.model!r}, api_key='***')"

    def _post(self, url: str, headers: dict, payload: dict) -> dict:
        import urllib.request
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", **headers},
        )
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())


class OpenAIModel(_HTTPModel):
    """OpenAI / OpenAI-compatible chat-completions endpoint."""
    def __init__(self, api_key: str | None = None, model: str = "gpt-5.5",
                 base_url: str = "https://api.openai.com/v1"):
        super().__init__(api_key, model, base_url, "OPENAI_API_KEY")

    def complete(self, prompt, *, temperature=0.7, max_tokens=1024):
        out = self._post(
            f"{self.base_url}/chat/completions",
            {"Authorization": f"Bearer {self.api_key}"},
            {"model": self.model, "messages": [{"role": "user", "content": prompt}],
             "temperature": temperature, "max_tokens": max_tokens},
        )
        return out["choices"][0]["message"]["content"]


class AnthropicModel(_HTTPModel):
    """Anthropic messages endpoint."""
    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-4-6",
                 base_url: str = "https://api.anthropic.com/v1"):
        super().__init__(api_key, model, base_url, "ANTHROPIC_API_KEY")

    def complete(self, prompt, *, temperature=0.7, max_tokens=1024):
        out = self._post(
            f"{self.base_url}/messages",
            {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
            {"model": self.model, "max_tokens": max_tokens, "temperature": temperature,
             "messages": [{"role": "user", "content": prompt}]},
        )
        return "".join(b.get("text", "") for b in out["content"])
