from __future__ import annotations

import hashlib
import uuid
from pathlib import PurePosixPath


def normalize_relative_path(value: str) -> str:
    """Return a stable POSIX-style relative path without resolving the filesystem."""
    text = value.replace("\\", "/").lstrip("./")
    return str(PurePosixPath(text))


def root_namespace(root_id: str) -> uuid.UUID:
    if not root_id or not root_id.strip():
        raise ValueError("root_id is required for stable corpus identity")
    return uuid.uuid5(uuid.NAMESPACE_URL, f"corpus-reconcile-root:{root_id.strip()}")


def content_id_from_sha256(sha256: str | None) -> str | None:
    if not sha256:
        return None
    digest = sha256.lower()
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError("sha256 must be a 64-character lowercase/uppercase hex digest")
    return f"sha256:{digest}"


def first_observation_file_instance_id(*, root_id: str, original_relative_path: str, sha256: str | None, marker: str = "NO_SHA") -> str:
    """Assign a deterministic UUIDv5 only at first observation.

    For an ordinary binary, the name material is exactly normalized original path + SHA-256.
    For non-hashable filesystem objects (for example an inventoried symlink), marker makes
    the first-observation identity deterministic without pretending it has content fixity.
    """
    rel = normalize_relative_path(original_relative_path)
    identity_value = sha256.lower() if sha256 else marker
    value = f"{rel}\n{identity_value}"
    return f"FILE-{uuid.uuid5(root_namespace(root_id), value).hex.upper()}"


def observation_id(*, run_id: str, file_instance_id: str) -> str:
    value = f"{run_id}\n{file_instance_id}"
    return f"OBS-{uuid.uuid5(uuid.NAMESPACE_URL, value).hex.upper()}"


def deterministic_transaction_id(*, file_instance_id: str, action: str, source_path: str, destination_path: str, expected_fixity: str) -> str:
    material = "\n".join([
        file_instance_id,
        action,
        normalize_relative_path(source_path),
        normalize_relative_path(destination_path),
        expected_fixity,
    ])
    return f"TXN-{uuid.uuid5(uuid.NAMESPACE_URL, material).hex.upper()}"


def deterministic_rank(value: str, run_seed: str) -> str:
    return hashlib.sha256(f"{value}\n{run_seed}".encode("utf-8")).hexdigest()
