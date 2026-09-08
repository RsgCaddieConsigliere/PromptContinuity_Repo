from __future__ import annotations
from collections import defaultdict

def reused_attachment_candidates(parsed_emails: list[dict]) -> list[dict]:
    by_hash = defaultdict(list)
    for email_idx, email in enumerate(parsed_emails, start=1):
        email_key = email.get("message_id") or email.get("path") or f"EMAIL-{email_idx}"
        for att in email.get("attachments", []):
            by_hash[att["sha256"]].append({"email_key": email_key,"filename": att.get("filename", ""),"ordinal": att.get("ordinal")})
    out = []
    for sha, refs in sorted(by_hash.items()):
        if len(refs) < 2:
            continue
        out.append({"sha256": sha,"relationship_type": "REUSED_ATTACHMENT_BYTES","references": refs,"basis": "ATTACHMENT_SHA256_MATCH","confidence": 1.0})
    return out
