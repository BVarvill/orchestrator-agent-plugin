---
name: verify-merge
description: The orchestrator's checklist before merging a worker's pull request, and the steps after. Use when a worker reports "PR #N is open", when Ben says "integrate", "review the PRs", "merge it", or "review each open PR and merge the good ones".
---

# Verify, then merge

Never trust the report alone. A wrong assumption at the merge seat is still wrong.

## Before merging (all of them)

1. **The PR exists on GitHub.** Take the PR number from the worker's last line and look it up. A "done" that exists only in the worker's worktree is not done.
2. **CI is green AND actually ran.** A job that dies in seconds is a setup or billing problem, not a pass. If checks are still running, wait with one blocking command (`gh pr checks N --watch`), not repeated polling.
3. **Scope.** Diff against the branch's fork point, not today's main: `gh pr view N --json files`. Only the order's files, or the PR says why.
4. **Read the code that matters.** The 2 to 5 files in the PR's code review guide. Look for the order's named attack.
5. **Spot-check the key claims** against the code and the data. One number, one behaviour.
6. **Re-run any check CI does not cover**, from a clean tree.
7. **The report meets the `pr-report` standard.** If the six-line box would not let Ben explain the change in his own words, send it back.
8. **Red tier:** the `reviewer` agent's cold read, and the dry-run evidence.
9. **Private data.** No customer names or real records in the diff, commits or PR text.

## Merging

- Only on Ben's "integrate", or a standing permission he gave in this project.
- `gh pr merge N --merge`, then `git fetch` and confirm main moved.

## After merging (do not skip)

1. **Promote "Decided"** into DECISIONS.md: the decision, at least two rejected options, the reversal condition.
2. **Promote "Learned"** into TRAPS.md, each fact with its source.
3. **File every open question.** A review is not finished while a question in the PR has no home. Put each one on the board or in the order it belongs to, linked to the PR.
4. **Update PLAN.md**: move the order to Done.
5. **Tell Ben**, short: merged, what it means for him, what (if anything) he must decide.

## Sending a PR back

Send it back to the same worker (continue it, do not start fresh) with a numbered list: what is wrong, where, and what "fixed" looks like.
Fixing it yourself is fine only for a trivial in-scope slip, and you say so.

## Clean up

After a merge, the worker's worktree and branch can go. Never remove a worktree whose work has not landed.
