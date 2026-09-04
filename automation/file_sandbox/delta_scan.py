#!/usr/bin/env python3
"""Compare two MASTER_MANIFEST.csv files and emit a read-only delta report."""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from pathlib import Path

def read_manifest(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("old_manifest", type=Path)
    ap.add_argument("new_manifest", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    old = read_manifest(args.old_manifest)
    new = read_manifest(args.new_manifest)
    old_by_path = {r["original_relative_path"]: r for r in old}
    new_by_path = {r["original_relative_path"]: r for r in new}
    new_hash_paths = defaultdict(set)
    for r in new:
        new_hash_paths[r["sha256"]].add(r["original_relative_path"])
    rows = []
    visited_new = set()
    for path, o in sorted(old_by_path.items()):
        if path in new_by_path:
            n = new_by_path[path]
            visited_new.add(path)
            status = "UNCHANGED" if o["sha256"] == n["sha256"] else "MODIFIED"
            rows.append({"status": status, "old_path": path, "new_path": path, "old_sha256": o["sha256"], "new_sha256": n["sha256"]})
        else:
            moved_to = sorted(new_hash_paths.get(o["sha256"], set()) - visited_new)
            if moved_to:
                np = moved_to[0]
                visited_new.add(np)
                rows.append({"status": "MOVED_SAME_CONTENT", "old_path": path, "new_path": np, "old_sha256": o["sha256"], "new_sha256": o["sha256"]})
            else:
                rows.append({"status": "MISSING", "old_path": path, "new_path": "", "old_sha256": o["sha256"], "new_sha256": ""})
    for path, n in sorted(new_by_path.items()):
        if path in visited_new or path in old_by_path:
            continue
        rows.append({"status": "NEW", "old_path": "", "new_path": path, "old_sha256": "", "new_sha256": n["sha256"]})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        fields = ["status","old_path","new_path","old_sha256","new_sha256"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    summary = {s: sum(1 for r in rows if r["status"] == s) for s in ["UNCHANGED","MODIFIED","NEW","MISSING","MOVED_SAME_CONTENT"]}
    print(json.dumps(summary, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
