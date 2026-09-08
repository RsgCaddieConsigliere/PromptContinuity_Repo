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


def stat_snapshot(path: str | Path) -> dict:
    st = Path(path).stat()
    return {"size_bytes": st.st_size, "mtime_ns": st.st_mtime_ns}


def stat_changed(pre: dict, post: dict) -> bool:
    return pre["size_bytes"] != post["size_bytes"] or pre["mtime_ns"] != post["mtime_ns"]


def read_bytes_with_stat_guard(path: str | Path) -> dict:
    """Read one byte stream and reject it if file size/mtime changes during the read."""
    p = Path(path)
    pre = stat_snapshot(p)
    try:
        data = p.read_bytes()
    except Exception as exc:
        return {
            "data": None,
            "sha256": None,
            "fixity_status": "READ_ERROR",
            "hash_error": f"{type(exc).__name__}: {exc}",
            "size_bytes_pre": pre["size_bytes"],
            "size_bytes_post": None,
            "mtime_ns_pre": pre["mtime_ns"],
            "mtime_ns_post": None,
        }

    post = stat_snapshot(p)
    changed = stat_changed(pre, post)
    return {
        "data": None if changed else data,
        "sha256": None if changed else hashlib.sha256(data).hexdigest(),
        "fixity_status": "STALE_DURING_SCAN" if changed else "HASHED_STABLE",
        "hash_error": "file size or mtime changed during read" if changed else "",
        "size_bytes_pre": pre["size_bytes"],
        "size_bytes_post": post["size_bytes"],
        "mtime_ns_pre": pre["mtime_ns"],
        "mtime_ns_post": post["mtime_ns"],
    }


def sha256_with_stat_guard(path: str | Path) -> dict:
    """Hash a regular file and reject the digest as a baseline if it changed mid-scan."""
    p = Path(path)
    pre = stat_snapshot(p)
    try:
        digest = sha256_file(p)
    except Exception as exc:  # fail closed; caller records the diagnostic separately
        return {
            "sha256": None,
            "fixity_status": "HASH_ERROR",
            "hash_error": f"{type(exc).__name__}: {exc}",
            "size_bytes_pre": pre["size_bytes"],
            "size_bytes_post": None,
            "mtime_ns_pre": pre["mtime_ns"],
            "mtime_ns_post": None,
        }

    post = stat_snapshot(p)
    changed = stat_changed(pre, post)
    return {
        "sha256": None if changed else digest,
        "fixity_status": "STALE_DURING_SCAN" if changed else "HASHED_STABLE",
        "hash_error": "file size or mtime changed during hashing" if changed else "",
        "size_bytes_pre": pre["size_bytes"],
        "size_bytes_post": post["size_bytes"],
        "mtime_ns_pre": pre["mtime_ns"],
        "mtime_ns_post": post["mtime_ns"],
    }
