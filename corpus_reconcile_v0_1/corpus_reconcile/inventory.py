from __future__ import annotations
from pathlib import Path
import mimetypes
import uuid
from .hashing import sha256_file

SKIP_NAMES = {".DS_Store"}

def inventory_local(root: str | Path, matter: str = "PILOT") -> list[dict]:
    root = Path(root).resolve()
    rows = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name in SKIP_NAMES:
            continue
        stat = p.stat()
        mime, _ = mimetypes.guess_type(p.name)
        rows.append({
            "src_id": f"SRC-{uuid.uuid5(uuid.NAMESPACE_URL, str(p)).hex[:12].upper()}",
            "matter": matter,
            "original_path": str(p),
            "original_name": p.name,
            "mime_type": mime or "application/octet-stream",
            "size_bytes": stat.st_size,
            "local_sha256": sha256_file(p),
            "google_native": False,
            "fixity_basis": "LOCAL_SHA256",
        })
    return rows
