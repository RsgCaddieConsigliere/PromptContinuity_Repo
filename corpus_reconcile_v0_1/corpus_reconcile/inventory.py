from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from typing import Mapping

from .constants import ProtectionClass
from .hashing import sha256_with_stat_guard
from .identity import (
    content_id_from_sha256,
    first_observation_file_instance_id,
    normalize_relative_path,
    observation_id,
)

OS_NOISE_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def _hidden_flag(relative_path: str) -> bool:
    return any(part.startswith(".") for part in Path(relative_path).parts)


def _escapes_root(root: Path, path: Path) -> bool:
    try:
        root_real = root.resolve()
        target_real = path.resolve(strict=False)
        return os.path.commonpath([str(root_real), str(target_real)]) != str(root_real)
    except (OSError, ValueError):
        return True


def inventory_local(
    root: str | Path,
    matter: str = "PILOT",
    *,
    root_id: str = "LOCAL-PILOT",
    run_id: str = "RUN-LOCAL",
    instance_registry: Mapping[str, Mapping] | None = None,
) -> list[dict]:
    """Read-only deterministic filesystem census.

    instance_registry is keyed by CURRENT_RELATIVE_PATH from prior control state. Existing
    registry entries preserve FILE_INSTANCE_ID across approved moves/renames and in-place
    byte changes. UUIDv5 assignment is used only when no existing instance can be resolved.
    """
    root = Path(root).resolve()
    registry = instance_registry or {}
    rows: list[dict] = []

    for current_root, dir_names, file_names in os.walk(root, followlinks=False):
        dir_names.sort()
        file_names.sort()
        current = Path(current_root)

        # Directory symlinks are inventoried as objects and removed from descent.
        for dirname in list(dir_names):
            p = current / dirname
            if not p.is_symlink():
                continue
            dir_names.remove(dirname)
            rel = normalize_relative_path(str(p.relative_to(root)))
            prior = registry.get(rel, {})
            file_instance_id = prior.get("file_instance_id") or first_observation_file_instance_id(
                root_id=root_id,
                original_relative_path=prior.get("original_relative_path", rel),
                sha256=None,
                marker="SYMLINK",
            )
            st = p.lstat()
            protection = prior.get("protection_class", ProtectionClass.UNKNOWN.value)
            rows.append({
                "src_id": observation_id(run_id=run_id, file_instance_id=file_instance_id),
                "run_id": run_id,
                "root_id": root_id,
                "file_instance_id": file_instance_id,
                "first_observed_run_id": prior.get("first_observed_run_id", run_id),
                "content_id": None,
                "matter": matter,
                "original_relative_path": prior.get("original_relative_path", rel),
                "current_relative_path": rel,
                "original_name": Path(prior.get("original_relative_path", rel)).name,
                "mime_type": "inode/symlink",
                "size_bytes_pre": st.st_size,
                "size_bytes_post": st.st_size,
                "mtime_ns_pre": st.st_mtime_ns,
                "mtime_ns_post": st.st_mtime_ns,
                "local_sha256": None,
                "fixity_status": "NOT_APPLICABLE",
                "hash_error": "",
                "protection_class": protection,
                "sticky_protection_source": prior.get("sticky_protection_source", ""),
                "source_or_derivative_role": prior.get("source_or_derivative_role", "UNKNOWN"),
                "quarantine_flag": protection == ProtectionClass.QUARANTINE.value,
                "symlink_flag": True,
                "path_escape_flag": _escapes_root(root, p),
                "extension_mismatch_flag": False,
                "hidden_flag": _hidden_flag(rel),
                "exclusion_status": "INVENTORIED_NOT_FOLLOWED",
                "exclusion_reason": "SYMLINK_DIRECTORY",
                "google_native": False,
                "fixity_basis": "NOT_APPLICABLE",
            })

        for filename in file_names:
            p = current / filename
            rel = normalize_relative_path(str(p.relative_to(root)))
            prior = registry.get(rel, {})
            hidden = _hidden_flag(rel)
            os_noise = p.name in OS_NOISE_NAMES
            symlink = p.is_symlink()
            mime, _ = mimetypes.guess_type(p.name)

            if symlink:
                st = p.lstat()
                fixity = {
                    "sha256": None,
                    "fixity_status": "NOT_APPLICABLE",
                    "hash_error": "",
                    "size_bytes_pre": st.st_size,
                    "size_bytes_post": st.st_size,
                    "mtime_ns_pre": st.st_mtime_ns,
                    "mtime_ns_post": st.st_mtime_ns,
                }
            elif os_noise:
                st = p.stat()
                fixity = {
                    "sha256": None,
                    "fixity_status": "EXCLUDED_OS_NOISE",
                    "hash_error": "",
                    "size_bytes_pre": st.st_size,
                    "size_bytes_post": st.st_size,
                    "mtime_ns_pre": st.st_mtime_ns,
                    "mtime_ns_post": st.st_mtime_ns,
                }
            else:
                fixity = sha256_with_stat_guard(p)

            sha = fixity["sha256"]
            original_rel = prior.get("original_relative_path", rel)
            file_instance_id = prior.get("file_instance_id") or first_observation_file_instance_id(
                root_id=root_id,
                original_relative_path=original_rel,
                sha256=sha,
                marker="SYMLINK" if symlink else "UNHASHED_FIRST_OBSERVATION",
            )
            protection = prior.get("protection_class", ProtectionClass.UNKNOWN.value)

            rows.append({
                "src_id": observation_id(run_id=run_id, file_instance_id=file_instance_id),
                "run_id": run_id,
                "root_id": root_id,
                "file_instance_id": file_instance_id,
                "first_observed_run_id": prior.get("first_observed_run_id", run_id),
                "content_id": content_id_from_sha256(sha),
                "matter": matter,
                "original_relative_path": original_rel,
                "current_relative_path": rel,
                "original_name": Path(original_rel).name,
                "mime_type": mime or "application/octet-stream",
                "size_bytes_pre": fixity["size_bytes_pre"],
                "size_bytes_post": fixity["size_bytes_post"],
                "mtime_ns_pre": fixity["mtime_ns_pre"],
                "mtime_ns_post": fixity["mtime_ns_post"],
                "local_sha256": sha,
                "fixity_status": fixity["fixity_status"],
                "hash_error": fixity["hash_error"],
                "protection_class": protection,
                "sticky_protection_source": prior.get("sticky_protection_source", ""),
                "source_or_derivative_role": prior.get("source_or_derivative_role", "UNKNOWN"),
                "quarantine_flag": protection == ProtectionClass.QUARANTINE.value,
                "symlink_flag": symlink,
                "path_escape_flag": _escapes_root(root, p) if symlink else False,
                "extension_mismatch_flag": False,
                "hidden_flag": hidden,
                "exclusion_status": "EXCLUDED_OS_NOISE" if os_noise else "INCLUDED",
                "exclusion_reason": "KNOWN_OS_NOISE" if os_noise else "",
                "google_native": False,
                "fixity_basis": "LOCAL_SHA256" if sha else "NOT_APPLICABLE",
            })

    return rows
