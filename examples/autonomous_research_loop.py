"""
Autonomous research loop: the model proposes a hypothesis AND the code that tests
it; an executor RUNS the code; the execution output — not the model — decides;
the loop reflects and iterates. Bring your own key.

    export OPENAI_API_KEY=...          # or ANTHROPIC_API_KEY
    python examples/autonomous_research_loop.py \
        --question "Find a closed form for the sum of the first n odd numbers" \
        --provider openai --rounds 3 --allow-exec

Offline (no key, no execution risk) it runs a deterministic stub so you can see the
shape of the loop:

    python examples/autonomous_research_loop.py --rounds 2

SECURITY: with --allow-exec this runs model-written Python in a subprocess. That is
not a sandbox. Use a container/VM for anything real. Without --allow-exec the loop
only proposes (it will not execute), so it is safe to run anywhere.
"""
import argparse, json, os, re, sys, time, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from looplab.models import StubModel, OpenAIModel, AnthropicModel
from looplab.executors import run_python

PROMPT = """You are doing research on: {question}

History so far (most recent last):
{history}

Propose ONE concrete next step. Return ONLY JSON:
{{"hypothesis": "<a specific, testable claim>",
  "prediction": "<a short string the test will print if the claim holds, e.g. PASS or a number>",
  "code": "<self-contained Python that tests the claim and prints the prediction on success>"}}
The code must be runnable as-is with the standard library and print your prediction to stdout."""

STUB = [  # offline canned rounds: one verifies (code really runs), one is refuted by execution
    {"hypothesis": "sum of the first n odd numbers equals n^2",
     "prediction": "PASS",
     "code": "n=10\nif sum(2*i-1 for i in range(1,n+1))==n*n: print('PASS')\nelse: print('FAIL')"},
    {"hypothesis": "sum of the first n odd numbers equals n^2 + 1",
     "prediction": "PASS",
     "code": "n=10\nif sum(2*i-1 for i in range(1,n+1))==n*n+1: print('PASS')\nelse: print('FAIL')"},
]


def _json(text, fallback):
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try: return json.loads(m.group(0))
        except Exception: pass
    return fallback


def make_model(provider):
    if provider == "openai":
        return OpenAIModel()
    if provider == "anthropic":
        return AnthropicModel()
    it = iter(STUB)
    return StubModel(responder=lambda p: json.dumps(next(it, {"hypothesis": "(none)",
                     "prediction": "", "code": "print('no more ideas')"})))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", default="Find a closed form for the sum of the first n odd numbers")
    ap.add_argument("--provider", default="stub", choices=["stub", "openai", "anthropic"])
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--allow-exec", action="store_true",
                    help="actually run model-written code (NOT sandboxed — use a container for real work)")
    ap.add_argument("--ledger", default="examples/artifacts/autonomous_ledger.jsonl")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.ledger), exist_ok=True)
    model = make_model(args.provider)
    history, verified = [], []

    print(f"Q: {args.question}\nprovider={args.provider}  rounds={args.rounds}  "
          f"exec={'on' if args.allow_exec else 'OFF (proposal-only)'}\n" + "-" * 60)

    for r in range(1, args.rounds + 1):
        step = _json(model.complete(PROMPT.format(question=args.question,
                     history="\n".join(history) or "none")), STUB[0])
        hyp, pred, code = step.get("hypothesis", ""), step.get("prediction", ""), step.get("code", "")
        print(f"\n[round {r}] hypothesis: {hyp}\n          predicts: {pred!r}")

        if not args.allow_exec:
            verdict, detail, out = "PROPOSED", "execution disabled (--allow-exec to run)", ""
        else:
            res = run_python(code, timeout=args.timeout)            # the executor RUNS it
            out = (res["stdout"] or res["stderr"]).strip()
            ok = res["ok"] and pred and pred.strip() in res["stdout"]  # execution decides, not the model
            verdict, detail = ("VERIFIED", "") if ok else ("REJECTED", out or "prediction not produced")
            if ok:
                verified.append(hyp)
        print(f"          => {verdict}  {detail}")

        rec = {"t": time.time(), "round": r, "hypothesis": hyp, "prediction": pred,
               "code_sha": hashlib.sha256(code.encode()).hexdigest()[:12],
               "verdict": verdict, "stdout": out}
        with open(args.ledger, "a") as f:
            f.write(json.dumps(rec) + "\n")
        history.append(f"tried: {hyp} -> {verdict} ({detail})")

    print("\n" + "-" * 60)
    print(f"verified by execution: {len(verified)}")
    for v in verified:
        print(f"  + {v}")
    print(f"audit trail: {args.ledger}")
    if not args.allow_exec:
        print("\n(ran in proposal-only mode; re-run with --allow-exec to execute and verify)")


if __name__ == "__main__":
    main()
