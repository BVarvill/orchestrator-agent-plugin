---
name: cost-guard
description: Keep agent work cheap without making it worse - which model and effort for which job, when not to spawn, how to wait for free, and how to keep context small. Use when choosing a model for a worker or subagent, before launching agents, when a task will read many files, or when Ben asks about cost or tokens.
---

# Cost guard

Spend where judgment matters. Do mechanics with scripts. Never pay to wait.

## 1. Pick the cheapest model that can do the job well

| Job | Model | Effort |
|---|---|---|
| Read and summarise files, search, list, extract | haiku | low |
| A clear build order with named files and tests | sonnet | medium |
| Research across many sources, a scout report | sonnet | medium |
| A cold code review of an amber PR | sonnet | medium |
| Red-tier review, unclear design, a hard bug, a decision interview | opus | high |
| The orchestrator itself | the session's model | as set |

- Never use the highest effort unless Ben asks.
- If a cheap model fails twice on the same job, step up one level. Say so in the report.
- **Ben's standing rule:** tiering is allowed. A worker never silently swaps to a bigger model; it says so.

## 2. Do not spawn when you do not need to

- Answer from code you can read in one or two files. No agent.
- Relay evidence you already have. No new research.
- Unclear intent: ask Ben first. A worker on a vague order is the most expensive mistake.
- One agent with a good order beats three agents with overlapping ones.

## 3. Delegate big reads

- When a task means reading many files or long pages, give it to a haiku or sonnet subagent and keep only its conclusion. The raw text never enters the orchestrator's context.
- Ask for a word limit and a fixed shape ("under 800 words, a table then bullets").

## 4. Waiting is free, polling is not

- **Never loop "sleep, then check".** Each check is a paid turn.
- Background agents tell you when they finish. Do other work or stop.
- For CI, use one blocking command (`gh pr checks N --watch`).
- For long jobs, a script waits and wakes you; the model does not watch.
- "No change" is never worth a message.

## 5. Keep context small

- **Always-loaded files stay short.** CLAUDE.md holds only what every session needs. Situational detail goes in a skill, which loads only when its description matches.
- Read only the part of a file you need (offsets, `grep`, `head`).
- Run `bearings` once at session start; do not re-read the same state by hand.
- Long command output: filter it (`tail`, `grep`, `--jq`) before it reaches the model.

## 6. Know what you spent

- `claude plugin details orchestrator-agent-plugin` shows this plugin's own token cost.
- Every model call in a product has a spending cap.
- Evals run with a hard limit (`claude plugin eval ... --max-cost-usd 2`).
- In a worker's report, under operational evidence: roughly what it cost, if known.

## 7. Cleanup has a cost too

- Old worktrees pile up (one project reached 100). Remove a worktree once its PR has merged.
