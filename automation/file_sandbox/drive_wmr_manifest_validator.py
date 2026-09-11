#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path


def fail(msg):
    print(msg, file=sys.stderr)
    return 2


def main():
    if len(sys.argv) != 3:
        return fail("usage: drive_wmr_manifest_validator.py SCHEMA.json MANIFEST.csv")
    schema = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    with Path(sys.argv[2]).open(newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        if not r.fieldnames:
            return fail("missing header")
        missing = [c for c in schema["required_columns"] if c not in r.fieldnames]
        if missing:
            return fail("missing columns: " + ",".join(missing))
        rows = list(r)
    if not rows:
        return fail("manifest has no rows")
    seen = set()
    for i,row in enumerate(rows, start=2):
        aid = row["ACTION_ID"].strip()
        if not aid or aid in seen:
            return fail(f"row {i}: blank/duplicate ACTION_ID")
        seen.add(aid)
        if row["HITL_STATUS"] not in schema["allowed_hitl_status"]:
            return fail(f"row {i}: invalid HITL_STATUS")
        if row["EXECUTION_STATUS"] not in schema["allowed_execution_status"]:
            return fail(f"row {i}: invalid EXECUTION_STATUS")
        if not row["ORIGINAL_PROVIDER_ID"].strip() or not row["ORIGINAL_PARENT_ID"].strip():
            return fail(f"row {i}: missing original provider/parent identity")
        names = " ".join([row.get("ORIGINAL_NAME", ""), row.get("PROPOSED_FINAL_NAME", "")])
        for comp in schema["forbidden_name_components"]:
            if comp in names:
                return fail(f"row {i}: forbidden boundary component in name")
    print(f"PASS rows={len(rows)} unique_action_ids={len(seen)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
