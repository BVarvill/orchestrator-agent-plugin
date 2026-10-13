---
name: bearings
description: Show where the project stands - branch, main, what is in flight, open PRs with CI state, worktrees - from one cheap script with no model reasoning. Use when Ben says "bearings", "where are we", "what's in flight", "status", or at the start of an orchestrator session if the start-up digest is missing.
---

# Bearings

Run the script once and relay the result. Do not rebuild it by hand with many separate commands.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/bearings.sh"
```

Then tell Ben, short:
1. **Waiting on him:** PRs ready to integrate, and any question he owes.
2. **Running:** workers in flight.
3. **Next:** the top item on the board.

If a PR's CI shows FAILED, say so first.
