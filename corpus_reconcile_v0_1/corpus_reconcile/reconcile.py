from __future__ import annotations
from collections import defaultdict

def exact_duplicate_relationships(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    by_hash = defaultdict(list)
    for r in rows:
        sha = r.get("drive_sha256") or r.get("local_sha256") or r.get("sha256")
        if sha:
            by_hash[sha].append(r)
    relationships, families = [], []
    n = 0
    for sha, members in sorted(by_hash.items()):
        if len(members) < 2:
            continue
        n += 1
        family_id = f"FAM-EXACT-{n:04d}"
        ordered = sorted(members, key=lambda x: (x.get("created_time", ""), x.get("original_path", "")))
        canonical = ordered[0]
        families.append({"family_id": family_id,"family_type": "EXACT_BYTE_DUPLICATE","canonical_src_id": canonical["src_id"],"sha256": sha,"member_count": len(ordered),"status": "CANDIDATE"})
        for m in ordered[1:]:
            relationships.append({"from_src_id": m["src_id"],"to_src_id": canonical["src_id"],"relationship_type": "EXACT_BYTE_DUPLICATE","basis": "SHA256_MATCH","confidence": 1.0,"family_id": family_id})
    return relationships, families
