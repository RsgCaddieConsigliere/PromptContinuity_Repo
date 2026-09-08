from __future__ import annotations

import hashlib
from collections import defaultdict


def _exact_family_id(sha256: str) -> str:
    return f"FAM-EXACT-{hashlib.sha256(sha256.encode('ascii')).hexdigest()[:16].upper()}"


def exact_duplicate_relationships(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Group exact bytes without automatically selecting a canonical survivor."""
    by_hash = defaultdict(list)
    for row in rows:
        sha = row.get("drive_sha256") or row.get("local_sha256") or row.get("sha256")
        if sha and row.get("fixity_status") not in {"STALE_DURING_SCAN", "HASH_ERROR"}:
            by_hash[sha].append(row)

    relationships: list[dict] = []
    families: list[dict] = []
    for sha, members in sorted(by_hash.items()):
        if len(members) < 2:
            continue
        family_id = _exact_family_id(sha)
        ordered = sorted(
            members,
            key=lambda x: (
                x.get("file_instance_id", ""),
                x.get("current_relative_path") or x.get("original_path", ""),
            ),
        )
        families.append({
            "family_id": family_id,
            "family_type": "EXACT_BYTE_DUPLICATE",
            "canonical_src_id": None,
            "sha256": sha,
            "member_count": len(ordered),
            "status": "CANDIDATE",
            "rationale": "Exact SHA-256 family only; canonical survivor requires provenance/lineage/HITL analysis.",
        })
        anchor = ordered[0]
        for member in ordered[1:]:
            relationships.append({
                "from_src_id": member["src_id"],
                "to_src_id": anchor["src_id"],
                "relationship_type": "EXACT_BYTE_DUPLICATE",
                "basis": "SHA256_MATCH",
                "certainty": "CONFIRMED",
                "confidence": 1.0,
                "family_id": family_id,
            })
    return relationships, families
