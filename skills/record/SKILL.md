---
name: record
description: Record a data point about the work into records/events.jsonl - a ruling from Ben, an order written, a PR sent back or merged, a measured number, a hard fact learned, an incident, or a gap found. Use at every one of those moments without being asked, when Ben says "record this", "log this", "note that", or gives a ruling.
---

# Record data at every opportunity

Two kinds of data are worth keeping:
- **About the work:** rulings, orders, PRs, costs, incidents.
- **About the subject:** findings and data files about what the project is working on.

Every useful event becomes one line of data.
Later, that data answers questions no one thought to ask at the start: what an order costs, which model was worth it, how often PRs go back, what Ben ruled and when.

## How

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/record.py" <kind> "<one plain line>" [--order ID] [--pr N] [--data key=value ...]
```

It appends to `records/events.jsonl` at the repo root. Commit that file with the next docs commit.

## When (record without being asked)

| Moment | Kind | Example |
|---|---|---|
| Ben rules on anything | `ruling` | his words, short, with the date implied |
| An order is written | `order_written` | `--order O12 --data tier=amber model=sonnet` |
| A worker starts | `worker_launched` | `--order O12` |
| A worker opens a PR | `pr_opened` | `--order O12 --pr 31` |
| A PR goes back | `pr_sent_back` | the reason, one line |
| A PR merges | `pr_merged` | `--pr 31 --data files=7 tests_added=12` |
| A lasting choice | `decision` | also write it in DECISIONS.md |
| A hard fact about the inputs | `learned` | the fact and its source |
| A fact or number about the subject | `finding` | "Reply rate 24 percent, 2,685 emails, 2024-2026 sheets" |
| A data file that took effort to make | `save` | `record.py save out.csv "Reply rates by year"` (add `--private` if it holds private data) |
| A gap is found | `gap` | from the `what-are-we-missing` skill |
| A number is measured | `metric` | `--data value=0.91 n=297 set=held-out` |
| Something goes wrong | `incident` | what happened, the effect, the fix |

**Automatic, free:** every subagent run (`agent_run`, with its model and token totals) and every session end (`session`) are recorded by hooks. Do not record those by hand.

## Keep the data, not just the conclusion

- **If a query, script or analysis produced a useful table, save the table** (`record.py save`). Re-running it later may be slow, costly or impossible (the source can change).
- **Private data** (names, emails, records) goes with `--private`: it is copied to `records/private/`, which is never committed.
- **Before closing any piece of work, ask: what data here would be useful later?** Save it, or say why not.

## Rules

- **One plain line per summary.** Numbers go in `--data`.
- **No private data.** No customer names, emails or record contents. The file is committed.
- **Append only.** Never edit or delete a line. A correction is a new line.
- **A ruling is recorded the moment it is given,** before building on it.

## Reading it back

Use the `recall` skill.

When Ben asks "what does an order cost", "how often do PRs go back", or similar, answer from `records/events.jsonl` with a short script, not from memory. Say how many records the answer rests on.
