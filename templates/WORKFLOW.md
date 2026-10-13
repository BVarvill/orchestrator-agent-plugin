# Workflow

How work gets done in this repo.
Read this and CLAUDE.md before any work.

## Roles

- **Orchestrator:** plans, writes orders, verifies, merges, writes the lasting docs. The only session that merges.
- **Workers:** one order each, in their own git worktree and branch. Never the orchestrator's checkout.
- **Ben:** decides what gets built and every business rule. Nothing merges until he says "integrate".

## Risk tiers

| Tier | What | Who checks | Ben's part |
|---|---|---|---|
| **Green** | evals, docs, read-only tools | orchestrator | one line in the digest |
| **Amber** | new code, no outside writes | orchestrator plus the reviewer agent | reads the six-line box, says integrate |
| **Red** | writes to any live system, money, or a frozen eval set | orchestrator, reviewer, and a dry run on real data | sees the dry run, approves the first real write of each kind |

## The loop

1. Ben describes what he wants.
2. The orchestrator writes `orders/<ID>.md` and adds it to PLAN.md.
3. A worker builds in its own worktree: build, verify, attack its own work, fix, repeat.
4. It stops when every definition-of-perfect clause has evidence, or it is blocked, or the same failure survives three fixes.
5. It runs `make check`, opens the PR, ends with "PR #N is open - say 'integrate' in the orchestrator window".
6. Ben says "integrate".
7. The orchestrator re-checks everything itself, merges, promotes "Decided" into DECISIONS.md and "Learned" into TRAPS.md.

## The pull request

The template in `.github/pull_request_template.md` is mandatory.
The six-line "Read this first" box must let Ben explain the change in his own words, or the PR goes back.

## Gates that never move

- `make check` before every push; CI green on every PR.
- No private data in git.
- Spending caps on every model call.
- Frozen sets keep their hash; re-pinned only with a written reason.
