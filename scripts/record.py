#!/usr/bin/env python3
"""WHAT THIS FILE IS

The project's data recorder. Every useful event in the orchestrator method
becomes one line of JSON in `records/events.jsonl`, at the repo root.
Over time that file answers questions no one thought to ask at the start:
  - What does an order cost, and which model was worth it?
  - How often is a PR sent back, and why?
  - How long from order to merge?
  - What did Ben rule, in his own words, and when?

Three ways in:
  1. By hand (the `record` skill), at the moments listed there:
       record.py ruling "Two leads per org, never three" --order O28
       record.py metric "golden accuracy" --data value=0.91 n=297
  2. Keep a data file that took effort to make (a query result, a table):
       record.py save path/to/table.csv "Reply rates by year, 2024-2026"
       record.py save notes.json "Raw lead list" --private
     The file is COPIED into records/data/ (committed) or records/private/
     (never committed: the script keeps records/.gitignore), and a
     data_saved line points to it with its size, rows and checksum.
  3. Automatically, from hooks (no model call, no tokens):
       record.py --hook subagent   (SubagentStop: one line per agent run,
                                    with its model and token totals)
       record.py --hook session    (SessionEnd: one line per session)

Rules:
  - KINDS is a closed list. An unknown kind fails loudly.
  - Append only. Lines are never edited or deleted.
  - No private data: never put customer names, emails or record contents in
    a summary. The file is meant to be committed.
  - Hooks never block or break a session: any error is swallowed silently.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

KINDS = {
    "order_written": "an order was written",
    "worker_launched": "a worker started an order",
    "pr_opened": "a worker opened a pull request",
    "pr_sent_back": "a PR went back to its worker, with the reason",
    "pr_merged": "a PR was merged",
    "ruling": "Ben ruled on something, in his own words",
    "decision": "a lasting choice (also goes in DECISIONS.md)",
    "learned": "a hard fact about the inputs, with its source",
    "finding": "a fact or number discovered about the project's subject, with its source",
    "data_saved": "a data file kept in records/data or records/private (use: record.py save)",
    "gap": "something we were missing, found by what-are-we-missing",
    "metric": "a measured number (accuracy, cost, time, count)",
    "incident": "something went wrong, and what happened",
    "agent_run": "automatic: one subagent run finished",
    "session": "automatic: one session ended",
}


def repo_root() -> Path | None:
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return Path(out.stdout.strip())


def is_orchestrator_repo(root: Path) -> bool:
    return (root / "PLAN.md").is_file() and (root / "orders").is_dir()


def append(root: Path, event: dict) -> None:
    path = root / "records" / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **event}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def usage_from_transcript(path: str) -> dict:
    """Sum token use and list the models from a Claude Code transcript.
    Returns {} if the file is missing or unreadable."""
    keys = ("input_tokens", "output_tokens",
            "cache_read_input_tokens", "cache_creation_input_tokens")
    # A transcript writes one reply as several lines (one per content block),
    # each carrying the same message id and usage. Keep the LAST line per id,
    # or every reply is counted two or three times.
    by_id: dict[str, dict] = {}
    models: set[str] = set()
    try:
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = row.get("message") if isinstance(row, dict) else None
                if not isinstance(msg, dict) or msg.get("role") != "assistant":
                    continue
                if msg.get("model") and not msg["model"].startswith("<"):
                    models.add(msg["model"])
                by_id[msg.get("id") or f"line{n}"] = msg.get("usage") or {}
    except OSError:
        return {}
    totals = {k: sum(int(u.get(k) or 0) for u in by_id.values()) for k in keys}
    turns = len(by_id)
    return {**totals, "models": sorted(models), "assistant_turns": turns}


def from_hook(which: str) -> None:
    """Hook mode: read the hook's JSON from stdin, write one line, never fail."""
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001 - a hook must never break the session
        data = {}
    try:
        root = repo_root()
        if root is None or not is_orchestrator_repo(root):
            return
        if which == "subagent":
            transcript = data.get("agent_transcript_path") or ""
            append(root, {"kind": "agent_run",
                          "agent_type": data.get("agent_type", "unknown"),
                          "agent_id": data.get("agent_id", ""),
                          "transcript": transcript,
                          "session_id": data.get("session_id", ""),
                          "usage": usage_from_transcript(transcript) if transcript else {}})
        elif which == "session":
            transcript = data.get("transcript_path") or ""
            append(root, {"kind": "session",
                          "session_id": data.get("session_id", ""),
                          "reason": data.get("reason", ""),
                          "transcript": transcript,
                          "cwd": os.path.basename(data.get("cwd", "") or ""),
                          "usage": usage_from_transcript(transcript) if transcript else {}})
    except Exception:  # noqa: BLE001 - recording is best effort in hooks
        return


def save(argv: list[str]) -> None:
    """Copy a data file into records/data (or records/private) and log it."""
    import hashlib
    import shutil
    ap = argparse.ArgumentParser(prog="record.py save",
                                 description="Keep a data file and record that it was kept")
    ap.add_argument("path")
    ap.add_argument("summary", help="what the data is, one plain line, no private data")
    ap.add_argument("--private", action="store_true",
                    help="holds private data: goes to records/private/, never committed")
    ap.add_argument("--order", default="")
    a = ap.parse_args(argv)
    src = Path(a.path)
    if not src.is_file():
        sys.exit(f"no such file: {src}")
    root = repo_root()
    if root is None:
        sys.exit("not inside a git repo: nothing saved")
    records = root / "records"
    records.mkdir(exist_ok=True)
    ignore = records / ".gitignore"
    if "private/" not in (ignore.read_text() if ignore.exists() else ""):
        with ignore.open("a") as f:
            f.write("private/\n")
    folder = records / ("private" if a.private else "data")
    folder.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    dest = folder / f"{stamp}-{src.name}"
    shutil.copy2(src, dest)
    raw = dest.read_bytes()
    rows = raw.count(b"\n")
    event = {"kind": "data_saved", "summary": a.summary,
             "path": str(dest.relative_to(root)), "private": a.private,
             "bytes": len(raw), "rows": rows,
             "sha256": hashlib.sha256(raw).hexdigest()[:16]}
    if a.order:
        event["order"] = a.order
    append(root, event)
    print(f"saved {dest.relative_to(root)} ({len(raw)} bytes, {rows} lines)"
          + (" - private, not committed" if a.private else ""))


def main() -> None:
    if len(sys.argv) >= 3 and sys.argv[1] == "--hook":
        from_hook(sys.argv[2])
        return
    if len(sys.argv) >= 2 and sys.argv[1] == "save":
        save(sys.argv[2:])
        return
    ap = argparse.ArgumentParser(description="Record one event to records/events.jsonl")
    ap.add_argument("kind", help="one of: " + ", ".join(KINDS))
    ap.add_argument("summary", help="one plain line, no private data")
    ap.add_argument("--order", default="")
    ap.add_argument("--pr", default="")
    ap.add_argument("--data", nargs="*", default=[], metavar="KEY=VALUE")
    a = ap.parse_args()
    if a.kind not in KINDS:
        sys.exit(f"unknown kind {a.kind!r}. Known kinds:\n" +
                 "\n".join(f"  {k}: {v}" for k, v in KINDS.items()))
    root = repo_root()
    if root is None:
        sys.exit("not inside a git repo: nothing recorded")
    extra = {}
    for pair in a.data:
        if "=" not in pair:
            sys.exit(f"--data needs KEY=VALUE, got {pair!r}")
        k, v = pair.split("=", 1)
        extra[k] = v
    event = {"kind": a.kind, "summary": a.summary}
    if a.order:
        event["order"] = a.order
    if a.pr:
        event["pr"] = a.pr
    if extra:
        event["data"] = extra
    append(root, event)
    print(f"recorded {a.kind}: {a.summary}")


if __name__ == "__main__":
    main()
