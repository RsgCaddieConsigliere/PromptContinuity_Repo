from __future__ import annotations

from collections import defaultdict

from .identity import deterministic_rank


def _exception_class(row: dict) -> str:
    flags = []
    for key in ("path_escape_flag", "extension_mismatch_flag", "quarantine_flag", "symlink_flag", "hidden_flag"):
        if row.get(key):
            flags.append(key.removesuffix("_flag").upper())
    if row.get("fixity_status") not in {"HASHED_STABLE", "NOT_APPLICABLE", "EXCLUDED_OS_NOISE"}:
        flags.append(str(row.get("fixity_status") or "FIXITY_UNKNOWN"))
    return "+".join(sorted(flags)) if flags else "NORMAL"


def _file_type(row: dict) -> str:
    mime = row.get("mime_type") or "application/octet-stream"
    return mime.split("/", 1)[0]


def stratified_sample(rows: list[dict], *, max_objects: int = 50, run_seed: str = "G0G5-v1") -> list[dict]:
    """Deterministic round-robin sample across protection/file/exception strata.

    The full census must already exist. Relationship-family enrichment may be added to rows
    before calling this function; relationship_family is included in the stratum when present.
    """
    if max_objects < 1:
        return []

    strata: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = (
            row.get("protection_class", "UNKNOWN"),
            _file_type(row),
            row.get("relationship_family", "NO_FAMILY"),
            _exception_class(row),
        )
        strata[key].append(row)

    ranked: dict[tuple, list[dict]] = {}
    for key, members in strata.items():
        ranked[key] = sorted(
            members,
            key=lambda row: (
                deterministic_rank(row["file_instance_id"], run_seed),
                row.get("original_relative_path", ""),
                row["file_instance_id"],
            ),
        )

    selected: list[dict] = []
    ordered_keys = sorted(ranked)
    offset = 0
    while len(selected) < min(max_objects, len(rows)):
        progressed = False
        for key in ordered_keys:
            members = ranked[key]
            if offset < len(members):
                selected.append(members[offset])
                progressed = True
                if len(selected) >= max_objects:
                    break
        if not progressed:
            break
        offset += 1
    return selected
