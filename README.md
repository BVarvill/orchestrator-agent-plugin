# orchestrator: Ben's way of working, as a Claude Code plugin

One orchestrator session plans, writes orders, verifies and merges.
Workers build one order each in their own git worktree and report by pull request.
Ben decides what gets built and says "integrate".

## What is inside

| Part | Name | What it does |
|---|---|---|
| Skill | orchestrate | The core rules: roles, the loop, tiers, when to ask Ben, when not to spawn |
| Skill | write-order | The order template (intent separate from plan) |
| Skill | verify-merge | The checklist before and after a merge |
| Skill | pr-report | How a PR is written for Ben (the six-line box) |
| Skill | diagnose | Find the real cause before fixing a bug |
| Skill | cost-guard | Model and effort per job, no polling, small context |
| Skill | bearings | Where the project stands, from a script |
| Skill | project-setup | Start a new repo the orchestrator way |
| Agent | worker | Builds one order, sonnet by default |
| Agent | reviewer | Cold read-only PR review, sonnet (opus for red tier) |
| Agent | scout | Read-only research, haiku |
| Hook | SessionStart | Prints the bearings digest, only in repos with PLAN.md and orders/ |

Skills load only when their description matches the task, so they cost almost nothing until used.

## Where it lives

`~/.claude/skills/orchestrator/` loads in every session as `orchestrator@skills-dir`.
Turn it off: `claude plugin disable orchestrator@skills-dir`.
Its own token cost: `claude plugin details orchestrator`.

## Ideas taken from firstmate (github.com/kunchenguid/firstmate)

- Intent kept separate from the plan in every order.
- Evidence is not permission.
- The orchestrator decides in-scope findings; only scope growth, repeats, and risky choices go to Ben, in a five-part format.
- A review is not finished until every open question is filed.
- Landing is proven by records (the PR on GitHub), not by a report.
- Scripts for mechanics, agents for judgment; waiting is free, polling is not.
- A diagnosis protocol: trigger, mask, symptom, counterfactual.

Kept as Ben's own, where firstmate differs: only the orchestrator merges, on Ben's word (no auto-merge); the orchestrator does verify and spot-check; orders are richer.
