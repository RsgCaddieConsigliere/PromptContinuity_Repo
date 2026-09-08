from __future__ import annotations

import argparse
import json
from pathlib import Path

from .email_parser import parse_eml
from .inventory import inventory_local
from .reconcile import exact_duplicate_relationships
from .sampling import stratified_sample
from .zip_manifest import zip_manifest


def _load_registry(path: str | None) -> dict:
    if not path:
        return {}
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, list):
        return {row["current_relative_path"]: row for row in data}
    if isinstance(data, dict):
        return data
    raise ValueError("instance registry must be a JSON object or list of instance rows")


def _instance_rows(rows: list[dict]) -> list[dict]:
    out = []
    seen = set()
    for row in rows:
        file_instance_id = row["file_instance_id"]
        if file_instance_id in seen:
            continue
        seen.add(file_instance_id)
        out.append({
            "file_instance_id": file_instance_id,
            "root_id": row["root_id"],
            "original_relative_path": row["original_relative_path"],
            "original_filename": row["original_name"],
            "current_relative_path": row["current_relative_path"],
            "protection_class": row["protection_class"],
            "sticky_protection_source": row["sticky_protection_source"],
            "source_or_derivative_role": row["source_or_derivative_role"],
            "quarantine_flag": row["quarantine_flag"],
        })
    return out


def main():
    parser = argparse.ArgumentParser(prog="corpus-reconcile")
    sub = parser.add_subparsers(required=True)

    inventory = sub.add_parser("inventory")
    inventory.add_argument("root")
    inventory.add_argument("--matter", default="PILOT")
    inventory.add_argument("--root-id", default="LOCAL-PILOT", help="Stable parent-controlled corpus root ID; explicit value required for production runs")
    inventory.add_argument("--run-id", default="RUN-LOCAL", help="Unique append-only run ID; explicit value required for production runs")
    inventory.add_argument("--run-seed", default="G0G5-v1", help="Parent-controlled deterministic sampling seed")
    inventory.add_argument("--sample-size", type=int, default=50)
    inventory.add_argument("--instance-registry", help="JSON registry keyed by current_relative_path or list of prior file-instance rows")

    eml = sub.add_parser("parse-eml")
    eml.add_argument("path")

    zip_cmd = sub.add_parser("zip-manifest")
    zip_cmd.add_argument("path")

    args = parser.parse_args()
    if hasattr(args, "root"):
        rows = inventory_local(
            args.root,
            args.matter,
            root_id=args.root_id,
            run_id=args.run_id,
            instance_registry=_load_registry(args.instance_registry),
        )
        rels, families = exact_duplicate_relationships(rows)
        out = {
            "run_id": args.run_id,
            "root_id": args.root_id,
            "file_instances": _instance_rows(rows),
            "source_objects": rows,
            "relationships": rels,
            "duplicate_families": families,
            "stratified_source_set": stratified_sample(rows, max_objects=args.sample_size, run_seed=args.run_seed),
        }
    elif args.path.lower().endswith(".eml"):
        out = parse_eml(args.path)
    else:
        out = zip_manifest(args.path)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
