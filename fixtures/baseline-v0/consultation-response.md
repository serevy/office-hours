# Synthetic expert response

I would prefer bounded exponential backoff with jitter over a fixed one-second retry. The workload is not latency-critical, and the remote service already demonstrated burst sensitivity, so spacing repeated attempts reduces the chance of making the failure worse.

Keep the policy bounded: set a maximum delay and a maximum retry count, and preserve the existing idempotency requirement. If the worker already has an operator-visible failure state after retries are exhausted, I would avoid adding a more elaborate retry subsystem at this stage.
