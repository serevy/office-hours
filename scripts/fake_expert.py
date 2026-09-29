#!/usr/bin/env python3
"""Deterministic fake ExpertProvider for adapter portability tests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_packet(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("packet must be a JSON object")
    return value


def consult(packet: dict[str, Any]) -> dict[str, Any]:
    evidence = packet.get("evidence", [])
    keys = {
        item.get("key")
        for item in evidence
        if isinstance(item, dict) and isinstance(item.get("key"), str)
    }

    base = {
        "protocol_version": "0.1",
        "consultation_id": packet["consultation_id"],
        "result_id": f"fake-{packet['consultation_id']}-r{packet['revision']}",
        "request_revision": packet["revision"],
        "risks": [],
        "provenance": {
            "expert": {
                "adapter": "deterministic-fake",
                "provider": "local-test",
                "model": "fixture-v0.1",
            },
            "trace_id": packet.get("provenance", {}).get("trace_id", "fake-trace"),
            "created_at": "2000-01-01T00:00:00Z",
        },
    }

    if "remote_rate_limit_signal" not in keys:
        return {
            **base,
            "status": "need_more_context",
            "risks": [
                "The remote service rate-limit behavior is required before choosing a retry policy."
            ],
            "requested_context": [
                {
                    "key": "remote_rate_limit_signal",
                    "reason": "The retry policy depends on whether the service exposes a retry delay and reacts badly to bursts.",
                    "max_bytes": 2048,
                }
            ],
        }

    return {
        **base,
        "status": "advice",
        "advice": "Prefer bounded exponential backoff with jitter and honor the retry-after hint when present.",
        "rationale": "The workload is not latency-critical and the supplied evidence says bursty retries reduce reliability.",
        "risks": [
            "Large backoff limits can make recovery slower.",
            "Retry exhaustion still needs an operator-visible failure state.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    result = consult(load_packet(args.packet))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
