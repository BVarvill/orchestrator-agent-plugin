---
name: project-setup
description: Set up a new repo for the orchestrator method - CLAUDE.md, WORKFLOW.md, PLAN.md, DECISIONS.md, TRAPS.md, orders/, a Makefile check target, a pre-push hook, CI and the PR template. Use when Ben starts a new project, says "set this project up the orchestrator way", or "kick off a new project".
---

# Set up a project for the orchestrator method

## 1. Interview Ben first (small batches, never guess)

- What is it, and who is it for?
- What does "done" look like?
- Hard constraints: private data, money, live systems, deadlines.
- How will we measure success? Is there an answer key (golden set) we can score against?

## 2. Show the plan before creating anything

Propose the files below. **Creating a GitHub repo, pushing, or anything public waits for Ben's yes.**

| File | What goes in it |
|---|---|
| CLAUDE.md | Rules every session reads first. Short. Writing rules for Ben. |
| WORKFLOW.md | Roles, tiers, the loop, the PR standard, the merge checklist. |
| PLAN.md | The board: In flight, Next, Blocked, Done. |
| DECISIONS.md | Decision, rejected options, reversal condition. Orchestrator writes at merge. |
| TRAPS.md | Hard facts about the inputs, each with a source. Add-only. |
| orders/ | One file per job. |
| Makefile | `make check` = lint plus tests. |
| .githooks/pre-push | Runs `make check` and a private-data scan. |
| .github/workflows/ci.yml | Runs `make check` on every PR and on main. |
| .github/pull_request_template.md | The `pr-report` format. |

Copy the starting files from `${CLAUDE_PLUGIN_ROOT}/templates/` and fill them in.

## 3. The gates

- `make check` before every push.
- A scored answer key wherever accuracy matters, used as a merge gate.
- CI on every PR. Check that jobs actually start (a billing failure looks like test failures).
- Spending caps on anything that costs money.
- Checksums pinned on anything frozen; re-pinned only with a written reason.

## 4. Then propose the first three orders

Say which can run in parallel (no shared files) and which model each needs (`cost-guard`).
