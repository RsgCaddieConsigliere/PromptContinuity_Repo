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
