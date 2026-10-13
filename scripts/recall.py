#!/usr/bin/env python3
"""WHAT THIS FILE IS

"What did we do earlier about X?" - answered from what was written down,
not from memory. It searches, cheapest and most trusted first:

  1. records/events.jsonl  - rulings, findings, metrics, decisions, incidents
  2. records/data/ and records/private/  - file names, and the first lines of
     each saved file
  3. DECISIONS.md, PLAN.md and orders/*.md
  4. (only with --transcripts) the saved chat transcripts Claude Code keeps on
     this machine for this project and its worktrees, under
     ~/.claude/projects/. Slower and noisier, so it is opt-in.

A line matches when it contains EVERY search word (case does not matter).
Output is capped, so the answer stays cheap to read.

    recall.py "reply rate"
    recall.py "two leads per org" --transcripts
    recall.py "colleague rule" --kind ruling
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SNIPPET = 220


def repo_root() -> Path:
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.exit("not inside a git repo")
    # A worktree's top level is the worktree; the main checkout holds the
    # shared records too, so search both when they differ.
    return Path(out.stdout.strip())


def main_checkout(root: Path) -> Path:
    try:
        out = subprocess.run(["git", "rev-parse", "--path-format=absolute",
                              "--git-common-dir"], capture_output=True, text=True,
                             check=True, cwd=root)
        return Path(out.stdout.strip()).parent
    except (subprocess.CalledProcessError, FileNotFoundError):
        return root


def matches(text: str, words: list[str]) -> bool:
    low = text.lower()
    return all(w in low for w in words)


def snippet(text: str, words: list[str]) -> str:
    text = re.sub(r"\s+", " ", text)
    i = text.lower().find(words[0]) if words else 0
    start = max(0, i - SNIPPET // 3)
    cut = text[start:start + SNIPPET]
    return ("..." if start else "") + cut + ("..." if start + SNIPPET < len(text) else "")


def search_events(roots: list[Path], words: list[str], kind: str, limit: int) -> list[str]:
    hits = []
    for root in roots:
        path = root / "records" / "events.jsonl"
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not matches(line, words):
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if kind and e.get("kind") != kind:
                continue
            extra = {k: v for k, v in e.items()
                     if k not in ("at", "kind", "summary", "usage", "transcript")}
            hits.append(f"[{e.get('at', '')[:10]}] {e.get('kind')}: {e.get('summary', '')}"
                        + (f" {json.dumps(extra)}" if extra else ""))
    return hits[-limit:]


def search_files(roots: list[Path], words: list[str], limit: int) -> list[str]:
    hits: list[str] = []
    seen: set[Path] = set()
    for root in roots:
        files = [root / "DECISIONS.md", root / "PLAN.md", *sorted((root / "orders").glob("*.md"))]
        for sub in ("data", "private"):
            folder = root / "records" / sub
            if folder.is_dir():
                files += sorted(p for p in folder.iterdir() if p.is_file())
        for f in files:
            if not f.is_file() or f.resolve() in seen:
                continue
            seen.add(f.resolve())
            rel = f.relative_to(root)
            if "records" in rel.parts and matches(f.name, words):
                hits.append(f"{rel}: (file name matches)")
            try:
                lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            if "records" in rel.parts:
                lines = lines[:50]          # saved data: header lines only
            for n, line in enumerate(lines, 1):
                if matches(line, words):
                    hits.append(f"{rel}:{n}: {snippet(line, words)}")
                    if len(hits) >= limit:
                        return hits
    return hits


def transcript_dirs(root: Path) -> list[Path]:
    """Claude Code keeps each project's chats in ~/.claude/projects/<path with
    / and . turned into ->. Worktrees of the project share the prefix."""
    base = Path.home() / ".claude" / "projects"
    key = re.sub(r"[/.]", "-", str(root))
    return sorted(d for d in base.glob(key + "*") if d.is_dir()) if base.is_dir() else []


def message_text(row: dict) -> tuple[str, str]:
    msg = row.get("message")
    if not isinstance(msg, dict) or msg.get("role") not in ("user", "assistant"):
        return "", ""
    content = msg.get("content")
    if isinstance(content, str):
        return msg["role"], content
    parts = [c.get("text", "") for c in content or [] if isinstance(c, dict) and c.get("type") == "text"]
    return msg["role"], " ".join(parts)


def search_transcripts(root: Path, words: list[str], limit: int) -> list[str]:
    hits = []
    files = []
    for d in transcript_dirs(root):
        files += [p for p in d.glob("*.jsonl")]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)   # newest first
    for f in files:
        try:
            with f.open(encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if not matches(line, words):    # cheap raw filter first
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    role, text = message_text(row)
                    if not text or not matches(text, words):
                        continue
                    when = str(row.get("timestamp", ""))[:10]
                    hits.append(f"[{when}] {role} in {f.parent.name[-30:]}/{f.stem[:8]}: "
                                f"{snippet(text, words)}")
                    if len(hits) >= limit:
                        return hits
        except OSError:
            continue
    return hits


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", help="words that must all appear")
    ap.add_argument("--kind", default="", help="only events of this kind (e.g. ruling)")
    ap.add_argument("--transcripts", action="store_true",
                    help="also search old chat transcripts (slower)")
    ap.add_argument("--limit", type=int, default=15, help="max hits per source")
    a = ap.parse_args()
    words = [w.lower() for w in a.query.split()]
    root = repo_root()
    roots = list(dict.fromkeys([root, main_checkout(root)]))

    sections = [("Records (events.jsonl)", search_events(roots, words, a.kind, a.limit)),
                ("Saved data, decisions, plan, orders", search_files(roots, words, a.limit))]
    if a.transcripts:
        sections.append(("Chat transcripts (newest first)",
                         search_transcripts(root, words, a.limit)))
    total = 0
    for title, hits in sections:
        print(f"## {title}: {len(hits)} hit(s)")
        for h in hits:
            print(f"- {h}")
        total += len(hits)
    if total == 0:
        print("\nNothing found." + ("" if a.transcripts else
              " Try --transcripts, or fewer or different words."))


if __name__ == "__main__":
    main()
