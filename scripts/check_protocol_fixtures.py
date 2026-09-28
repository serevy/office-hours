#!/usr/bin/env python3
"""Lightweight deterministic checks for the Office Hours protocol fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec"
FIXTURES = ROOT / "fixtures" / "protocol-v0.1"


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


def serialized_bytes(value: dict[str, Any]) -> int:
    return len(
        json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    )


def require_keys(value: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in value]
    if missing:
        raise AssertionError(f"{label} missing required keys: {missing}")


def check_packet(
    packet: dict[str, Any], packet_required: list[str], label: str
) -> None:
    require_keys(packet, packet_required, label)
    if packet["protocol_version"] != "0.1":
        raise AssertionError(f"{label} has unexpected protocol version")
    max_bytes = packet["context_budget"]["max_bytes"]
    actual_bytes = serialized_bytes(packet)
    if actual_bytes > max_bytes:
        raise AssertionError(
            f"{label} exceeds context budget: {actual_bytes} > {max_bytes}"
        )


def check_result(
    result: dict[str, Any],
    request: dict[str, Any],
    result_required: list[str],
    label: str,
) -> None:
    require_keys(result, result_required, label)
    if result["protocol_version"] != "0.1":
        raise AssertionError(f"{label} has unexpected protocol version")
    if result["consultation_id"] != request["consultation_id"]:
        raise AssertionError(f"{label} consultation id does not match request")
    if result["request_revision"] != request["revision"]:
        raise AssertionError(f"{label} request revision does not match request")

    status = result["status"]
    if status == "advice":
        if not result.get("advice"):
            raise AssertionError(f"{label} advice status requires advice")
        if "requested_context" in result:
            raise AssertionError(f"{label} advice status must not request more context")
    elif status == "need_more_context":
        if result.get("advice"):
            raise AssertionError(f"{label} need_more_context must not contain advice")
        requested = result.get("requested_context")
        if not isinstance(requested, list) or not requested:
            raise AssertionError(
                f"{label} need_more_context requires requested_context"
            )
    else:
        raise AssertionError(f"{label} has unsupported status: {status}")

    max_bytes = request["response_budget"]["max_bytes"]
    actual_bytes = serialized_bytes(result)
    if actual_bytes > max_bytes:
        raise AssertionError(
            f"{label} exceeds response budget: {actual_bytes} > {max_bytes}"
        )


def main() -> int:
    packet_schema = load(SPEC / "consultation-packet.schema.json")
    result_schema = load(SPEC / "consultation-result.schema.json")

    packet_required = packet_schema["required"]
    result_required = result_schema["required"]

    initial = load(FIXTURES / "initial-request.json")
    need_more = load(FIXTURES / "need-more-context.json")
    enriched = load(FIXTURES / "enriched-request.json")
    advice = load(FIXTURES / "advice.json")

    check_packet(initial, packet_required, "initial request")
    check_result(need_more, initial, result_required, "need-more-context result")
    check_packet(enriched, packet_required, "enriched request")
    check_result(advice, enriched, result_required, "advice result")

    if enriched["consultation_id"] != initial["consultation_id"]:
        raise AssertionError("incremental request changed consultation id")
    if enriched["revision"] != initial["revision"] + 1:
        raise AssertionError("incremental request revision did not increase by one")

    requested_keys = {item["key"] for item in need_more["requested_context"]}
    initial_evidence = {item["key"] for item in initial["evidence"]}
    enriched_evidence = {item["key"] for item in enriched["evidence"]}

    if requested_keys <= initial_evidence:
        raise AssertionError("fixture does not actually demonstrate missing context")
    if not requested_keys <= enriched_evidence:
        raise AssertionError("enriched request did not supply requested context")

    print("Protocol v0.1 fixtures passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
