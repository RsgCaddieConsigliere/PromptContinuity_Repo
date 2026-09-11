#!/usr/bin/env python3
import argparse, csv, hashlib, json, shutil, sys
from pathlib import Path

RESTRICTED_COMPONENT = "0000X-Files-Restricted"
ARCHIVE_COMPONENTS = {"99_ARCHIVE", "ARCHIVE"}
ALLOWED_ACTIONS = {"COPY", "MKDIR", "WRITE_NEW", "RENAME", "MOVE"}


def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def within(path: Path, root: Path):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def blocked_component(path: Path):
    parts = set(path.parts)
    if RESTRICTED_COMPONENT in parts:
        return RESTRICTED_COMPONENT
    if parts & ARCHIVE_COMPONENTS:
        return sorted(parts & ARCHIVE_COMPONENTS)[0]
    return None


def load_auth(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["AUTH_ID", "CANARY_ROOT", "ALLOWED_ACTIONS", "CANARY_ONLY", "DELETE_ALLOWED", "SOURCE_MUTATION_AUTHORITY", "HITL_STATUS"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError("missing auth fields: " + ",".join(missing))
    if data["CANARY_ONLY"] != "YES":
        raise ValueError("v0.1 requires CANARY_ONLY=YES")
    if data["DELETE_ALLOWED"] != "NO":
        raise ValueError("DELETE must remain disabled")
    if data["SOURCE_MUTATION_AUTHORITY"] != "NOT_GRANTED":
        raise ValueError("v0.1 does not execute source mutation")
    if data["HITL_STATUS"] != "APPROVED":
        raise ValueError("HITL_STATUS must be APPROVED")
    allowed = set(data["ALLOWED_ACTIONS"] if isinstance(data["ALLOWED_ACTIONS"], list) else str(data["ALLOWED_ACTIONS"]).split(","))
    if not allowed <= ALLOWED_ACTIONS:
        raise ValueError("authorization includes unsupported action")
    data["_allowed"] = allowed
    return data


def load_rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def validate_row(row, auth, canary_root: Path):
    action = row["ACTION_TYPE"].strip().upper()
    if action not in ALLOWED_ACTIONS or action not in auth["_allowed"]:
        return False, "ACTION_NOT_AUTHORIZED"
    src = Path(row["SOURCE_PATH"]).expanduser() if row.get("SOURCE_PATH") else None
    dst = Path(row["TARGET_PATH"]).expanduser() if row.get("TARGET_PATH") else None
    for p in [src, dst]:
        if p and blocked_component(p):
            return False, "ARCHIVE_OR_RESTRICTED_COMPONENT"
    if action in {"RENAME", "MOVE"}:
        if not src or not dst or not within(src, canary_root) or not within(dst, canary_root):
            return False, "RENAME_MOVE_MUST_STAY_INSIDE_CANARY"
        if row.get("N13_STATUS") not in {"PASS", "NOT_APPLICABLE_CANARY_COPY"}:
            return False, "N13_GATE_NOT_SATISFIED"
    if action == "COPY":
        if not src or not dst or not within(dst, canary_root):
            return False, "COPY_TARGET_MUST_BE_INSIDE_CANARY"
    if action in {"MKDIR", "WRITE_NEW"}:
        if not dst or not within(dst, canary_root):
            return False, "WRITE_TARGET_MUST_BE_INSIDE_CANARY"
    if row.get("HITL_STATUS") != "APPROVED":
        return False, "ROW_HITL_NOT_APPROVED"
    if row.get("AUTH_ID") != auth["AUTH_ID"]:
        return False, "AUTH_ID_MISMATCH"
    return True, "PASS"


def execute_row(row):
    action = row["ACTION_TYPE"].strip().upper()
    src = Path(row["SOURCE_PATH"]).expanduser() if row.get("SOURCE_PATH") else None
    dst = Path(row["TARGET_PATH"]).expanduser() if row.get("TARGET_PATH") else None
    before = sha256_file(src) if src and src.is_file() else ""
    if action == "COPY":
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    elif action == "MKDIR":
        dst.mkdir(parents=True, exist_ok=True)
    elif action == "WRITE_NEW":
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            raise FileExistsError(str(dst))
        dst.write_text(row.get("NOTES", ""), encoding="utf-8")
    elif action in {"RENAME", "MOVE"}:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            raise FileExistsError(str(dst))
        src.rename(dst)
    after = sha256_file(dst) if dst and dst.is_file() else ""
    return before, after


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", required=True)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args()
    auth = load_auth(Path(args.auth))
    canary_root = Path(auth["CANARY_ROOT"]).expanduser().resolve()
    rows = load_rows(Path(args.batch))
    receipt = []
    failed = False
    for row in rows:
        ok, reason = validate_row(row, auth, canary_root)
        status = "VALIDATED" if ok else "BLOCKED"
        before = after = ""
        if ok and args.execute:
            try:
                before, after = execute_row(row)
                status = "EXECUTED"
            except Exception as e:
                status = "FAILED"
                reason = type(e).__name__ + ":" + str(e)
                failed = True
        elif not ok:
            failed = True
        receipt.append({"ACTION_ID": row.get("ACTION_ID", ""), "ACTION_TYPE": row.get("ACTION_TYPE", ""), "STATUS": status, "REASON": reason, "SOURCE_PATH": row.get("SOURCE_PATH", ""), "TARGET_PATH": row.get("TARGET_PATH", ""), "BEFORE_SHA256": before, "AFTER_SHA256": after, "AUTH_ID": row.get("AUTH_ID", "")})
    out = Path(args.receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["ACTION_ID","ACTION_TYPE","STATUS","REASON","SOURCE_PATH","TARGET_PATH","BEFORE_SHA256","AFTER_SHA256","AUTH_ID"]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(receipt)
    return 2 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
