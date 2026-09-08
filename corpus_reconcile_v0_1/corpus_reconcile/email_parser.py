from __future__ import annotations
from email import policy
from email.parser import BytesParser
from pathlib import Path
import hashlib
from .hashing import sha256_file

HEADER_FIELDS = ["Message-ID", "Date", "From", "To", "Cc", "Bcc", "Subject", "In-Reply-To", "References"]

def parse_eml(path: str | Path) -> dict:
    p = Path(path)
    msg = BytesParser(policy=policy.default).parsebytes(p.read_bytes())
    headers = {k.lower().replace("-", "_"): str(msg.get(k, "")) for k in HEADER_FIELDS}
    attachments = []
    for idx, part in enumerate(msg.iter_attachments(), start=1):
        payload = part.get_payload(decode=True) or b""
        attachments.append({
            "ordinal": idx,
            "filename": part.get_filename() or f"attachment-{idx}",
            "content_type": part.get_content_type(),
            "size_bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    return {"path": str(p), "sha256": sha256_file(p), **headers, "attachment_count": len(attachments), "attachments": attachments}
