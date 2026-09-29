#!/usr/bin/env sh
set -eu

force=0
if [ "${1:-}" = "--force" ]; then
  force=1
elif [ "$#" -gt 0 ]; then
  echo "usage: $0 [--force]" >&2
  exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
claude_home="${HOME}/.claude"

skill_source="$repo_root/skills/office-hours/SKILL.md"
skill_target_dir="$claude_home/skills/office-hours"
skill_target="$skill_target_dir/SKILL.md"

agent_source="$repo_root/agents/office-hours-expert.md"
agent_target_dir="$claude_home/agents"
agent_target="$agent_target_dir/office-hours-expert.md"

for source in "$skill_source" "$agent_source"; do
  if [ ! -f "$source" ]; then
    echo "source does not exist: $source" >&2
    exit 2
  fi
done

install_file() {
  source=$1
  target=$2
  target_dir=$3
  label=$4

  if [ -f "$target" ] && [ "$force" -ne 1 ]; then
    if cmp -s "$source" "$target"; then
      return
    fi
    echo "$label already exists and differs: $target" >&2
    echo "re-run with --force to replace it" >&2
    exit 1
  fi

  mkdir -p "$target_dir"
  cp "$source" "$target"
}

install_file "$skill_source" "$skill_target" "$skill_target_dir" "Office Hours skill"
install_file "$agent_source" "$agent_target" "$agent_target_dir" "Office Hours expert agent"

echo "Office Hours installed for Claude Code."
echo "Skill: $skill_target_dir"
echo "Agent: $agent_target"
echo
echo "Start a new Claude Code session, then run:"
echo "  /office-hours"
