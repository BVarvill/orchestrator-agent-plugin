#!/usr/bin/env bash
# WHAT THIS FILE IS
# "Where did I leave off?" in one cheap read, with no model call.
# It prints a short digest: the branch, main's last commit, what PLAN.md says
# is in flight, the open pull requests with their CI state, and the worktrees.
#
# Two ways it runs:
#   bash bearings.sh          - by hand, or from the /bearings skill
#   bash bearings.sh --hook   - from the SessionStart hook. Then it stays
#                               SILENT unless this repo uses the orchestrator
#                               method (it has PLAN.md and an orders/ folder),
#                               so other projects pay zero tokens for it.
#
# Why a script and not the agent: reading git and GitHub is mechanics, not
# judgment. A script does it for free; an agent doing it spends tokens on
# every session start (idea from firstmate's "scripts for mechanics, agents
# for judgment").

set -u
HOOK=0
[ "${1:-}" = "--hook" ] && HOOK=1

root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$root" || exit 0

if [ ! -f PLAN.md ] || [ ! -d orders ]; then
  [ "$HOOK" = 1 ] && exit 0
  echo "bearings: this repo has no PLAN.md and orders/ folder (not an orchestrator project)."
  exit 0
fi

echo "## Bearings (orchestrator plugin, no model call)"
echo "- branch: $(git branch --show-current 2>/dev/null || echo detached)"
git fetch -q origin 2>/dev/null
echo "- main: $(git log -1 --format='%h %s' origin/main 2>/dev/null || git log -1 --format='%h %s' main 2>/dev/null)"

# The "In flight" section of PLAN.md, at most 10 lines.
inflight=$(awk '/^## In flight/{f=1;next} /^## /{f=0} f && NF' PLAN.md | head -10)
if [ -n "$inflight" ]; then
  echo "- in flight (PLAN.md):"
  echo "$inflight" | sed 's/^/  /'
fi

# Open pull requests and their CI result. Skipped quietly if gh is missing.
if command -v gh >/dev/null 2>&1; then
  prs=$(gh pr list --state open --limit 10 \
    --json number,title,statusCheckRollup \
    --jq '.[] | "  #\(.number) \(.title) [CI: \(
      if (.statusCheckRollup|length)==0 then "none"
      elif ([.statusCheckRollup[]|select(.conclusion=="FAILURE")]|length)>0 then "FAILED"
      elif ([.statusCheckRollup[]|select(.status!="COMPLETED")]|length)>0 then "running"
      else "green" end)]"' 2>/dev/null)
  if [ -n "$prs" ]; then
    echo "- open PRs:"
    echo "$prs"
  else
    echo "- open PRs: none (or GitHub not reachable)"
  fi
fi

n=$(git worktree list 2>/dev/null | wc -l | tr -d ' ')
echo "- worktrees: $n (run 'git worktree list' for detail)"
echo "Read this once. Do not re-run the same reads by hand."
