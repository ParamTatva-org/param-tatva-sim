#!/usr/bin/env python3
"""
combine_py_to_json.py

Usage:
  python combine_py_to_json.py /path/to/project -o project_code.json \
    --ignore "*/.git/*" "*/venv/*" "*/.venv/*" "*/__pycache__/*" \
    --strip-comments --max-chars 200000

If you want to import it, call collect_py_to_json(...) directly.
"""
from __future__ import annotations
import argparse, fnmatch, hashlib, io, json, os, re, sys
from datetime import datetime
from typing import Iterable, List, Dict, Any

_COMMENT_RE = re.compile(
    r"""
    (?P<strings>
        (?:[uUbB]?[rR]?'''(?:.|\n)*?''' | [uUbB]?[rR]?\"\"\"(?:.|\n)*?\"\"\"
        | [uUbB]?[rR]?'(?:\\'|[^'\n])*' | [uUbB]?[rR]?\"(?:\\\"|[^\"\n])*\")
    )
    |
    (?P<comment>\#.*?$)
    """,
    re.VERBOSE | re.MULTILINE,
)

def _strip_comments_and_blank_lines(code: str) -> str:
    """Remove # comments while preserving strings and docstrings; drop trailing blank lines."""
    # Keep strings (group 'strings') exactly; remove comments (group 'comment').
    def _sub(m: re.Match) -> str:
        if m.group('strings') is not None:
            return m.group('strings')
        return ''  # drop comment
    cleaned = _COMMENT_RE.sub(_sub, code)
    # Drop lines that are now empty or whitespace-only (optional but useful for LLM token budget)
    cleaned = "\n".join(line for line in cleaned.splitlines() if line.strip() != "")
    return cleaned.strip() + "\n" if cleaned.strip() else ""

def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8', errors='replace')).hexdigest()

def _should_ignore(path: str, ignore_globs: Iterable[str]) -> bool:
    for pat in ignore_globs:
        if fnmatch.fnmatch(path, pat):
            return True
    return False

def collect_py_to_json(
    root_dir: str,
    ignore_globs: Iterable[str] = ("*/.git/*", "*/__pycache__/*", "*/venv/*", "*/.venv/*", "*/build/*", "*/dist/*"),
    strip_comments: bool = False,
    max_chars_per_file: int | None = None,
    include_hash: bool = True,
) -> Dict[str, Any]:
    """
    Walk root_dir, collect .py files into a JSON-serializable dict.
    Returns:
      {
        "root": "<abs path>",
        "generated_at_utc": "...",
        "files": [{"path": "...", "size": int, "sha256": "...", "content": "..."}]
      }
    """
    root_dir = os.path.abspath(root_dir)
    out: Dict[str, Any] = {
        "root": root_dir,
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "files": [],
    }

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Prune ignored directories early for speed
        pruned = []
        for d in list(dirnames):
            test_path = os.path.join(dirpath, d) + os.sep
            if _should_ignore(test_path, ignore_globs):
                pruned.append(d)
        for d in pruned:
            dirnames.remove(d)

        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, root_dir)
            # Check file-level ignores
            if _should_ignore(fpath, ignore_globs) or _should_ignore(rel, ignore_globs):
                continue

            try:
                with io.open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
            except Exception as e:
                # If a file can’t be read, include a stub entry for visibility
                out["files"].append({
                    "path": rel,
                    "size": None,
                    "sha256": None,
                    "content": f"<<ERROR READING FILE: {e}>>",
                })
                continue

            if strip_comments:
                content = _strip_comments_and_blank_lines(content)

            if max_chars_per_file is not None and len(content) > max_chars_per_file:
                content = content[:max_chars_per_file] + "\n<<TRUNCATED>>\n"

            entry = {
                "path": rel,
                "size": len(content),
                "content": content,
            }
            if include_hash:
                entry["sha256"] = _sha256(content)
            out["files"].append(entry)

    # Sort by path for stable diffs
    out["files"].sort(key=lambda x: x["path"])
    return out

def write_json(payload: Dict[str, Any], out_path: str) -> None:
    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def _parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Combine all .py files into one JSON for LLM ingestion.")
    p.add_argument("root", help="Root directory to scan")
    p.add_argument("-o", "--out", default="project_code.json", help="Output JSON path")
    p.add_argument("--ignore", nargs="*", default=[".*","walker.py"], help="Extra glob patterns to ignore (in addition to defaults)")
    p.add_argument("--strip-comments", action="store_true", help="Remove # comments and blank lines (strings/docstrings kept)")
    p.add_argument("--no-hash", action="store_true", help="Do not include sha256 for each file")
    p.add_argument("--max-chars", type=int, default=None, help="Max characters per file; excess is truncated")
    return p.parse_args(argv)

def main(argv: List[str] | None = None) -> int:
    ns = _parse_args(sys.argv[1:] if argv is None else argv)
    payload = collect_py_to_json(
        ns.root,
        ignore_globs=("*/.git/*", "*/__pycache__/*", "*/venv/*", "*/.venv/*", "*/build/*", "*/dist/*", *ns.ignore),
        strip_comments=ns.strip_comments,
        max_chars_per_file=ns.max_chars,
        include_hash=(not ns.no_hash),
    )
    write_json(payload, ns.out)
    print(f"Wrote {ns.out} with {len(payload['files'])} files.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
