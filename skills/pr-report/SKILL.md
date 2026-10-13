---
name: pr-report
description: How a worker writes its pull request so Ben can understand and decide. Use when opening or editing a PR, when a worker finishes an order, or when the orchestrator checks a PR's write-up.
---

# The PR report: written for Ben's understanding, not as a work log

The PR is the worker's only report. It must let Ben keep an accurate picture of the system and decide with confidence.

## The title

Say the **intent**, not the implementation.
Good: "Score the lead record in seconds, not half a minute".
Bad: "perf(scorer): cache keys".

## The six-line box (Ben always reads this)

```markdown
## Read this first

- **For:** <the problem this solves, two plain lines a new reader can follow>
- **Changes:** <before -> after, with one concrete example>
- **Touches live systems:** <none | the named systems>
- **Evidence:** <the headline number, with its caveat in the same line>
- **Biggest risk:** <one line, and how to undo it>
- **Your decision:** <nothing, safe to integrate | the exact question Ben must answer>
```

If Ben could not explain the change in his own words from this box, the PR is not done.

## Then these sections

1. **Purpose and context:** what the system does here today, what was wrong, what this changes. Define each technical term on first use.
2. **Behaviour change:** before, after, one example.
3. **Where it sits:** five lines at most. What calls what.
4. **Results:** a small table, baseline beside new, sample size and caveat next to every number.
5. **Risks and what is unverified:** and how to reverse it.
6. **Code review guide:** the 2 to 5 files that matter, in reading order, one line each.
7. **Verification:** `make check`, CI link, any live check, and **what these do not prove**.
8. **Patch size:** production code versus tests, tooling and docs. A big diff needs a reason. Name every file outside the order.
9. **Learned:** hard facts about the inputs, each with a source (go to TRAPS.md).
10. **Decided:** lasting choices with the option rejected (go to DECISIONS.md). Write "proposed, not decided" where Ben must rule.

## Rules

- **Three kinds of evidence, labelled:** implementation (tests pass), evaluation (the task got better or worse), operational (cost, failures, safety).
- **Say what was measured on tuning data, what on held-out data, and what is only inferred.**
- **Caveats sit beside the number they qualify.**
- **Never claim a check that did not run.**
- **Name the most important design decision and the biggest unresolved risk.**
- Plain words, short sentences, no em dashes, no private data.
- End your final message with: "PR #N is open - say 'integrate' in the orchestrator window."
