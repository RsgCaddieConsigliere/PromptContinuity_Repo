from __future__ import annotations
import re
from pathlib import Path

SAFE = re.compile(r"[^A-Za-z0-9._-]+")

def safe_token(value: str) -> str:
    value = value.strip().replace(" ", "-")
    value = SAFE.sub("-", value)
    return re.sub(r"-+", "-", value).strip("-") or "UNSPECIFIED"

def propose_name(*, date: str, matter: str, object_type: str, source: str, description: str, version: str = "v01", extension: str = "") -> str:
    ext = extension if extension.startswith(".") or not extension else f".{extension}"
    stem = "__".join(safe_token(x) for x in [date, matter, object_type, source, description, version])
    return stem + ext

def extension_of(name: str) -> str:
    return Path(name).suffix
