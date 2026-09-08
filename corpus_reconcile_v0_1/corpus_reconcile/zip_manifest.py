from __future__ import annotations
import hashlib
import zipfile
from pathlib import Path
from .hashing import sha256_file

def zip_manifest(path: str | Path) -> dict:
    p = Path(path)
    members = []
    with zipfile.ZipFile(p, "r") as zf:
        for info in sorted(zf.infolist(), key=lambda x: x.filename):
            if info.is_dir():
                continue
            data = zf.read(info.filename)
            members.append({
                "name": info.filename,
                "size_bytes": info.file_size,
                "compressed_size_bytes": info.compress_size,
                "crc32": f"{info.CRC:08x}",
                "sha256": hashlib.sha256(data).hexdigest(),
            })
    return {"path": str(p), "zip_sha256": sha256_file(p), "member_count": len(members), "members": members}
