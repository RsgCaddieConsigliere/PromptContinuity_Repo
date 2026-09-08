from __future__ import annotations

from email import policy
from email.parser import BytesParser
import hashlib
from pathlib import Path

from .hashing import read_bytes_with_stat_guard

HEADER_FIELDS = ["Message-ID", "Date", "From", "To", "Cc", "Bcc", "Subject", "In-Reply-To", "References"]


def parse_eml(path: str | Path) -> dict:
    """Parse one stable EML byte stream and bind metadata/attachments to the same SHA-256."""
    p = Path(path)
    guarded = read_bytes_with_stat_guard(p)
    base = {
        "path": str(p),
        "sha256": guarded["sha256"],
        "raw_mime_sha256": guarded["sha256"],
        "fixity_status": guarded["fixity_status"],
        "hash_error": guarded["hash_error"],
        "size_bytes_pre": guarded["size_bytes_pre"],
        "size_bytes_post": guarded["size_bytes_post"],
        "mtime_ns_pre": guarded["mtime_ns_pre"],
        "mtime_ns_post": guarded["mtime_ns_post"],
    }
    data = guarded["data"]
    if data is None:
        return {**base, "parse_status": "BLOCKED_FIXITY", "attachment_count": 0, "attachments": []}

    try:
        msg = BytesParser(policy=policy.default).parsebytes(data)
    except Exception as exc:
        return {
            **base,
            "parse_status": "PARSE_ERROR",
            "parse_error": f"{type(exc).__name__}: {exc}",
            "attachment_count": 0,
            "attachments": [],
        }

    headers = {k.lower().replace("-", "_"): str(msg.get(k, "")) for k in HEADER_FIELDS}
    attachments = []
    for idx, part in enumerate(msg.iter_attachments(), start=1):
        payload = part.get_payload(decode=True) or b""
        attachments.append(
            {
                "ordinal": idx,
                "filename": part.get_filename() or f"attachment-{idx}",
                "content_type": part.get_content_type(),
                "size_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return {
        **base,
        **headers,
        "parse_status": "PARSED_STABLE",
        "attachment_count": len(attachments),
        "attachments": attachments,
    }
