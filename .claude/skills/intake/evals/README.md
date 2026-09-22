# Intake skill golden cases

These are the same hand-written extraction records the repository's golden
tests use (`tests/fixtures/intake/`), copied here as the skill's evaluation
set. Each one renders to YAML that `build.validate_record` accepts, every
exact quote verifies verbatim in its named capture, and rendering is
deterministic.

- `plaid-ai-annotator.extraction.yaml` — an agent with metrics and a duplicate
  observation alias.
- `zup-codegen.extraction.yaml` — an agent with lessons and no metrics.
- `duolingo-agentic-workflows.extraction.yaml` — a platform with workflow
  primitives.

A change to a prompt or question version reruns the suite before it ships:

```sh
uv run python -m unittest discover -s tests -p "test_intake_*.py"
```

The suite enforces the tie: `tests/test_intake_skill.py` fails when the
config's model, prompt, or question versions drift from the code, when a gate
threshold changes without the config, or when these files stop matching the
test fixtures byte for byte.
