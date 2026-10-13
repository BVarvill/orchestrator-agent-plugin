---
name: write-order
description: Write a worker order in Ben's fixed format (orders/<ID>.md). Use when the orchestrator is about to hand work to a worker, when Ben says "write an order", "write the order for this", or "make this an order".
---

# Write an order

One order is one job for one worker. Save it as `orders/<ID>.md`, add it to PLAN.md, commit it on main before launching.

## Before writing

- Check the work needs a worker at all (`orchestrate`, "When not to spawn").
- Read the code the order touches. Name real files and functions, not guesses.
- Pick the tier (green, amber, red) and the model (`cost-guard`).
- Run `what-are-we-missing` on the plan.
- After saving: `record.py order_written "<intent>" --order <ID> --data tier=<tier> model=<model>`.

## The template

```markdown
# <ID>: <the intent in plain words, not the implementation>

Tier: **<green|amber|red>**. Model: **<haiku|sonnet|opus>**, effort **<low|medium|high>**. Launch: <orchestrator | Ben pastes>, because <one line>.

## Ben's intent (the acceptance criteria - never widen this)
<What Ben asked for, in his words where possible, with the date.>

## The point
<What and why, in a few lines. The problem before the code.>

## Files
<The exact files or folders it may touch. Anything else needs a reason in the PR.>

## The rules
<Hard constraints. What it must preserve. Safety gates (dry run, "go one").>

## Definition of perfect
1. <A checkable clause, with the command or test that proves it.>
2. ...
N. `make check` green; CI green and actually ran.

## Data to keep
<What this job will produce that is worth keeping: findings, numbers, tables. Say where each goes: `finding`, `metric`, or `record.py save` (with `--private` for private data). Write "none" only if truly none.>

## What it must NOT do
<The tempting wrong moves, named.>

## Out of scope
<What a keen worker might add but must not.>

## The loop
Build, verify, attack, fix, repeat.
Stop when every clause has evidence, or it is truly blocked, or the same failure survives three fixes.
The attack that matters most: <the one failure this job is most likely to hide>.

## Report
A PR in the `pr-report` format.
End with: "PR #N is open - say 'integrate' in the orchestrator window."
```

## Rules for a good order

- **Intent and spec are separate.** "Ben's intent" is the contract. The rest is the orchestrator's plan, which the worker may improve if it says why.
- **Every definition-of-perfect clause is checkable** by a command, a test, or a named file. "Works well" is not a clause.
- **Name the files.** A worker touching files outside the order is the most common surprise.
- **Name the attack.** The worker spends its checking effort where it matters.
- **Red orders stop before the first live write** and wait for "go one".
- **No private data** in the order: no customer names, emails or real records. Use made-up examples.

## The worker prompt (when Ben pastes it, or for the `worker` agent)

```
Read CLAUDE.md and WORKFLOW.md first. You are a WORKER: work only in your own
git worktree, on a branch off origin/main (<commit> or later), never the
primary checkout. Your order is orders/<ID>.md. Read all of it before writing
code. <Two or three lines: the short version and the one hard rule.>
When the definition of perfect is met: run the checks, push, open the PR, and
end with: "PR #N is open - say 'integrate' in the orchestrator window."
```
