---
name: recall
description: Answer "what did we do earlier about X", "did we already measure Y", "what did Ben rule on Z", or "we had data on this before" from the written record, not memory. Searches records, saved data, decisions, orders, then old chat transcripts. Use before re-doing any analysis, and whenever earlier work may already hold the answer.
---

# Recall: get back what was done before

Context fills up and earlier work drops out of view. The record does not.
Look it up before re-doing it, and before saying "we never did that".

## How

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/recall.py" "<words>"
```

- Every word must appear in a line for it to match. Start with 2 or 3 distinctive words.
- `--kind ruling` (or `finding`, `metric`, `decision`, ...) narrows the records.
- `--transcripts` also searches old chat transcripts for this project and its worktrees. Slower; use it when the records come up empty.
- `--limit N` changes how many hits each source shows (default 15).

## Order of trust

1. **Records and saved data** - written down on purpose, with a source.
2. **DECISIONS.md, PLAN.md, orders** - the agreed state.
3. **Transcripts** - what was said, which may have changed later. Check it against 1 and 2.

## Then

- Answer with the source of each fact (file and line, or the record's date).
- If a saved data file holds the answer, read it and say so; do not re-run the analysis.
- If the answer came only from a transcript and is still useful, **record it now** (`finding`, or `record.py save` for the data) so it is easy to find next time.
- If nothing is found, say so plainly, and say what you searched.
