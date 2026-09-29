#!/usr/bin/env python3
"""Static and deterministic checks for the Claude Code Office Hours adapter."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict[str, Any]:
    value = json.loads(read(path))
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def run_fake(packet: str) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/fake_expert.py"), str(ROOT / packet)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    value = json.loads(completed.stdout)
    require(isinstance(value, dict), "fake expert output must be a JSON object")
    return value


def main() -> int:
    manifest = load_json(".claude-plugin/plugin.json")
    require(manifest.get("name") == "office-hours", "plugin name must be office-hours")

    skill = read("skills/office-hours/SKILL.md")
    require("name: office-hours" in skill, "skill must expose office-hours")
    require(
        "disable-model-invocation: true" in skill,
        "dogfood skill must remain user-invocable only",
    )
    require("allowed-tools: Agent" in skill, "skill must be able to invoke an expert agent")
    require(
        "office-hours-expert" in skill,
        "skill must reference the user-scope expert agent",
    )
    require(
        "office-hours:office-hours-expert" in skill,
        "skill must support plugin-scoped expert agent resolution",
    )

    agent = read("agents/office-hours-expert.md")
    require("name: office-hours-expert" in agent, "expert agent name is missing")
    require("model: opus" in agent, "dogfood expert should request the opus family")
    require("tools: Read, Grep, Glob" in agent, "expert tools must stay read-only")
    for forbidden in ("tools: Write", "tools: Edit", "tools: Bash", "tools: PowerShell"):
        require(forbidden not in agent, f"expert must not grant mutation tool: {forbidden}")

    windows_installer = read("scripts/install-claude-code.ps1")
    unix_installer = read("scripts/install-claude-code.sh")
    for installer, label in (
        (windows_installer, "PowerShell installer"),
        (unix_installer, "shell installer"),
    ):
        require("office-hours" in installer, f"{label} must install the skill")
        require("office-hours-expert" in installer, f"{label} must install the expert agent")

    insufficient = run_fake("fixtures/protocol-v0.1/initial-request.json")
    require(
        insufficient.get("status") == "need_more_context",
        "fake adapter must exercise need_more_context",
    )

    sufficient = run_fake("fixtures/protocol-v0.1/enriched-request.json")
    require(sufficient.get("status") == "advice", "fake adapter must return advice")
    require(
        sufficient.get("request_revision") == 2,
        "fake adapter must preserve request revision provenance",
    )

    print("Claude Code adapter checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
