#!/usr/bin/env python3
"""Read-only recursive inventory and SHA-256 manifest builder.

The script never renames, moves, deletes, edits, or OCRs source files.
It writes inventory outputs outside the source tree.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, mimetypes
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

FIELDS = [
    "asset_key","src_id","original_relative_path","original_filename","extension",
    "bytes","mtime_utc","mime_guess","sha256","source_mode","lock_status",
    "duplicate_group","needs_snapshot_export","scan_utc"
]

def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def mode_for(path: Path) -> tuple[str, str, str]:
    ext = path.suffix.lower()
    if ext in {".gdoc", ".gsheet", ".gslides", ".gdraw", ".gform", ".gsite"}:
        return "GOOGLE_NATIVE_LIVE", "LIVE-NOT-LOCKED", "YES"
    return "BLOB_NATIVE", "HASHED-BYTES", "NO"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_root", type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    root = args.source_root.resolve()
    out = args.out_dir.resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Source root not found or not a directory: {root}")
    out.mkdir(parents=True, exist_ok=True)
    scan_utc = datetime.now(timezone.utc).isoformat()
    rows = []
    hash_to_rows = defaultdict(list)
    errors = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        try:
            rel = path.relative_to(root).as_posix()
            stat = path.stat()
            digest = sha256_file(path)
            source_mode, lock_status, needs_snapshot = mode_for(path)
            row = {
                "asset_key": f"ASSET-SHA256-{digest[:16]}",
                "src_id": "",
                "original_relative_path": rel,
                "original_filename": path.name,
                "extension": path.suffix.lower(),
                "bytes": stat.st_size,
                "mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "mime_guess": mimetypes.guess_type(path.name)[0] or "",
                "sha256": digest,
                "source_mode": source_mode,
                "lock_status": lock_status,
                "duplicate_group": "",
                "needs_snapshot_export": needs_snapshot,
                "scan_utc": scan_utc,
            }
            rows.append(row)
            hash_to_rows[digest].append(row)
        except Exception as exc:
            errors.append({"path": str(path), "error": repr(exc)})
    dup_groups = []
    group_num = 1
    for digest, members in sorted(hash_to_rows.items()):
        if len(members) > 1:
            gid = f"DUP-{group_num:06d}"
            group_num += 1
            for row in members:
                row["duplicate_group"] = gid
            dup_groups.append({"duplicate_group": gid, "sha256": digest, "count": len(members), "paths": [m["original_relative_path"] for m in members]})
    with (out / "MASTER_MANIFEST.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    with (out / "SOURCE_ASSETS.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    (out / "EXACT_DUPLICATES.json").write_text(json.dumps(dup_groups, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "SCAN_EXCEPTIONS.json").write_text(json.dumps(errors, indent=2, ensure_ascii=False), encoding="utf-8")
    summary = {
        "scan_utc": scan_utc,
        "source_root": str(root),
        "files_scanned": len(rows),
        "bytes_scanned": sum(int(r["bytes"]) for r in rows),
        "unique_hashes": len(hash_to_rows),
        "duplicate_groups": len(dup_groups),
        "exceptions": len(errors),
        "google_native_live_pointer_files": sum(r["source_mode"] == "GOOGLE_NATIVE_LIVE" for r in rows),
    }
    (out / "SCAN_SUMMARY.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
