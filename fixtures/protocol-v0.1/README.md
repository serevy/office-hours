# Protocol v0.1 deterministic fixture

This fixture demonstrates the insufficient-context path without any private data.

1. `initial-request.json` asks for a retry-policy decision.
2. `need-more-context.json` asks only for the missing rate-limit evidence.
3. `enriched-request.json` keeps the consultation id, increments the revision, and adds that evidence.
4. `advice.json` returns bounded advice.

The fixture is deterministic. It is a protocol behavior test, not a model-quality benchmark.
