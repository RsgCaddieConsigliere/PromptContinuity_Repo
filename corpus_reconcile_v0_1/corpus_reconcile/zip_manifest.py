from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path

from .hashing import read_bytes_with_stat_guard


def zip_manifest(path: str | Path) -> dict:
    """Manifest one stable ZIP byte stream so archive hash and member hashes share one observation."""
    p = Path(path)
    guarded = read_bytes_with_stat_guard(p)
    base = {
        "path": str(p),
        "zip_sha256": guarded["sha256"],
        "fixity_status": guarded["fixity_status"],
        "hash_error": guarded["hash_error"],
        "size_bytes_pre": guarded["size_bytes_pre"],
        "size_bytes_post": guarded["size_bytes_post"],
        "mtime_ns_pre": guarded["mtime_ns_pre"],
        "mtime_ns_post": guarded["mtime_ns_post"],
    }
    data = guarded["data"]
    if data is None:
        return {**base, "manifest_status": "BLOCKED_FIXITY", "member_count": 0, "members": []}

    members = []
    try:
        with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
            for info in sorted(zf.infolist(), key=lambda x: x.filename):
                if info.is_dir():
                    continue
                member_data = zf.read(info.filename)
                members.append(
                    {
                        "name": info.filename,
                        "size_bytes": info.file_size,
                        "compressed_size_bytes": info.compress_size,
                        "crc32": f"{info.CRC:08x}",
                        "sha256": hashlib.sha256(member_data).hexdigest(),
                    }
                )
    except Exception as exc:
        return {
            **base,
            "manifest_status": "ZIP_PARSE_ERROR",
            "manifest_error": f"{type(exc).__name__}: {exc}",
            "member_count": 0,
            "members": [],
        }

    return {**base, "manifest_status": "MANIFESTED_STABLE", "member_count": len(members), "members": members}
