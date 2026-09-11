#!/usr/bin/env python3
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def fail(msg):
    print(msg, file=sys.stderr)
    return 2


def load_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        if not r.fieldnames:
            raise ValueError(f"{path}: missing header")
        return r.fieldnames, list(r)


def main():
    if len(sys.argv) not in {3, 4}:
        return fail("usage: source_review_receipt_validator.py SCHEMA.json RECEIPTS.csv [SOURCE_SET_MANIFEST.csv]")

    schema = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    fields, rows = load_csv(sys.argv[2])
    missing = [c for c in schema["required_columns"] if c not in fields]
    if missing:
        return fail("missing receipt columns: " + ",".join(missing))
    if not rows:
        return fail("receipt ledger has no rows")

    review_ids = set()
    source_keys = set()
    for i, row in enumerate(rows, start=2):
        rid = row["SOURCE_REVIEW_ID"].strip()
        sid = row["SOURCE_ID"].strip()
        ssid = row["SOURCE_SET_ID"].strip()
        if not rid or rid in review_ids:
            return fail(f"row {i}: blank/duplicate SOURCE_REVIEW_ID")
        review_ids.add(rid)
        key = (ssid, sid)
        if not ssid or not sid or key in source_keys:
            return fail(f"row {i}: blank/duplicate SOURCE_SET_ID+SOURCE_ID")
        source_keys.add(key)

        rs = row["REVIEW_STATUS"].strip()
        cs = row["COVERAGE_STATUS"].strip()
        ad = row["ARCHIVE_DISPOSITION"].strip()
        if rs not in schema["allowed_review_status"]:
            return fail(f"row {i}: invalid REVIEW_STATUS")
        if cs not in schema["allowed_coverage_status"]:
            return fail(f"row {i}: invalid COVERAGE_STATUS")
        if ad not in schema["allowed_archive_disposition"]:
            return fail(f"row {i}: invalid ARCHIVE_DISPOSITION")

        sha = row["SHA256"].strip()
        if rs in schema["sha256_required_statuses"] and not HEX64.fullmatch(sha):
            return fail(f"row {i}: valid SHA256 required")
        if cs in schema["full_coverage_statuses"] and not row["COVERAGE_LOCATORS"].strip():
            return fail(f"row {i}: full coverage requires COVERAGE_LOCATORS")
        if rs == "COMPLETE" and cs not in schema["full_coverage_statuses"]:
            return fail(f"row {i}: COMPLETE requires full coverage status")
        if ad.startswith("REVIEW_COMPLETE") and rs not in {"COMPLETE", "EXACT_DUPLICATE_REVIEW_SKIPPED"}:
            return fail(f"row {i}: review-complete archive disposition requires completed review")
        if not row["FINDINGS_DISPOSITION"].strip():
            return fail(f"row {i}: FINDINGS_DISPOSITION required even when no findings were adopted")
        if not row["REVIEW_RUN_ID"].strip():
            return fail(f"row {i}: REVIEW_RUN_ID required")

    if len(sys.argv) == 4:
        mf_fields, mf_rows = load_csv(sys.argv[3])
        if "SOURCE_SET_ID" not in mf_fields or "SOURCE_ID" not in mf_fields:
            return fail("source-set manifest requires SOURCE_SET_ID,SOURCE_ID")
        manifest_keys = {(r["SOURCE_SET_ID"].strip(), r["SOURCE_ID"].strip()) for r in mf_rows}
        if ("", "") in manifest_keys:
            return fail("source-set manifest contains blank identity")
        missing_receipts = sorted(manifest_keys - source_keys)
        extra_receipts = sorted(source_keys - manifest_keys)
        if missing_receipts:
            return fail("missing receipts for: " + ";".join(f"{a}/{b}" for a, b in missing_receipts))
        if extra_receipts:
            return fail("receipt rows not present in manifest: " + ";".join(f"{a}/{b}" for a, b in extra_receipts))

    digest = hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest()
    print(f"PASS receipts={len(rows)} unique_sources={len(source_keys)} ledger_sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
