from __future__ import annotations

import hashlib
from pathlib import Path

CHUNK = 1024 * 1024


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while chunk := f.read(CHUNK):
            h.update(chunk)
    return h.hexdigest()


def sha256_with_stat_guard(path: str | Path) -> dict:
    """Hash a regular file and reject the digest as a baseline if it changed mid-scan."""
    p = Path(path)
    pre = p.stat()
    try:
        digest = sha256_file(p)
    except Exception as exc:  # fail closed; caller records the diagnostic separately
        return {
            "sha256": None,
            "fixity_status": "HASH_ERROR",
            "hash_error": f"{type(exc).__name__}: {exc}",
            "size_bytes_pre": pre.st_size,
            "size_bytes_post": None,
            "mtime_ns_pre": pre.st_mtime_ns,
            "mtime_ns_post": None,
        }

    post = p.stat()
    changed = pre.st_size != post.st_size or pre.st_mtime_ns != post.st_mtime_ns
    return {
        "sha256": None if changed else digest,
        "fixity_status": "STALE_DURING_SCAN" if changed else "HASHED_STABLE",
        "hash_error": "file size or mtime changed during hashing" if changed else "",
        "size_bytes_pre": pre.st_size,
        "size_bytes_post": post.st_size,
        "mtime_ns_pre": pre.st_mtime_ns,
        "mtime_ns_post": post.st_mtime_ns,
    }
