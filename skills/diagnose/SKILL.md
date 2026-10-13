---
name: diagnose
description: Find the real cause of a bug before fixing it. Use for any bug report, a failing or flaky test, "why is X broken", "this doesn't work", or before writing a fix order.
---

# Diagnose before fixing

A fix for the wrong cause looks done and comes back later.

## Steps

1. **Reproduce it the way a user hits it.** End to end, as close to real use as you can. If you cannot reproduce it, say so; do not fix a guess.
2. **Split three things:**
   - the **trigger** (what starts it),
   - the **mask** (what hides it, or makes it look like something else),
   - the **symptom** (what the user sees).
3. **Compare with a path that works.** What is different between the broken run and a good one?
4. **Test a counterfactual.** Change only the suspected cause. The bug must go away. Change it back. The bug must return.
5. **Look for evidence against your theory.** One fact it cannot explain means it is not the cause yet.
6. **Write the failing test** that captures the real cause. Red first.
7. Then fix. Green after. Keep the test.

## Rules

- **The first plausible cause is often wrong.** In one real case, "multiple windows using the CRM" looked like the cause; the real one was a page left open by another step.
- **A diagnosis is not permission to change code.** It goes to the orchestrator or Ben first, unless the fix is clearly in the current order's scope.
- **Every postmortem becomes a regression test the same day.** Test data uses made-up names.
- **Report:** the trigger, the mask, the symptom, the counterfactual result, and what is still unexplained.
