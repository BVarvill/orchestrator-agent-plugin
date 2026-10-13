---
name: what-are-we-missing
description: A short, honest check for blind spots - what we have not looked at, assumed, or left out. Use before writing an order, before merging a PR, before a live write, when a result looks too good, when stuck, and whenever Ben asks "what are we missing", "what else", "anything we've not thought of", or "review this".
---

# What are we missing?

Stop for two minutes and ask the questions below about the current situation.
Most will have a quick "covered" answer. The point is the one or two that do not.

## The questions

**The goal**
1. What is Ben really trying to achieve here, one level above the request?
2. Would he be surprised by anything in the plan?

**The data**
3. What data have we not looked at that could change the answer?
4. Is the data stale, partial, or measured on the same cases we tuned on?
5. Is there a past record that already answers this? (run `recall`)
6. What data is this work producing that we should keep? (`record`)

**The assumptions**
7. What are we taking as true without checking it?
8. What would have to be true for this plan to be wrong?
9. Have we confused "the tests pass" with "it works for the user"?

**The edges**
10. What happens with empty input, a duplicate, a very large case, or a strange name?
11. What happens if it runs twice, or stops halfway?

**The people and systems**
12. Who or what else does this touch: a live system, a colleague, a customer?
13. How would we undo it?

**The cost**
14. Is there a cheaper way that is just as good?
15. Is an agent the wrong answer here? Would a rule or a script do?

## The output

Reply with only what matters, in this shape:

- **Missing:** each real gap, one line, with what to do about it.
- **Checked and fine:** a one-line list of the questions that came up clean.
- **Needs Ben:** any gap that is his call (use the decision format in CORE.md).

Record each real gap: `record.py gap "<the gap>"`.
If nothing is missing, say so in one line. Do not invent gaps to look thorough.
