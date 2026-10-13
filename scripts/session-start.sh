#!/usr/bin/env bash
# WHAT THIS FILE IS
# The SessionStart hook. In a repo that uses the orchestrator method (it has
# PLAN.md and an orders/ folder) it prints two things into the session:
#   1. CORE.md - the always-on rules (how to write, decide, behave, cost);
#   2. the bearings digest (scripts/bearings.sh).
# In any other repo it prints nothing, so other projects pay zero tokens.
here="$(cd "$(dirname "$0")/.." && pwd)"
root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -f "$root/PLAN.md" ] && [ -d "$root/orders" ] || exit 0
cat "$here/CORE.md"
echo
bash "$here/scripts/bearings.sh" --hook
