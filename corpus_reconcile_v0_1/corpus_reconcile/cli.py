from __future__ import annotations
import argparse, json
from .inventory import inventory_local
from .reconcile import exact_duplicate_relationships
from .email_parser import parse_eml
from .zip_manifest import zip_manifest

def main():
    p = argparse.ArgumentParser(prog="corpus-reconcile")
    sub = p.add_subparsers(required=True)
    a = sub.add_parser("inventory")
    a.add_argument("root"); a.add_argument("--matter", default="PILOT")
    e = sub.add_parser("parse-eml"); e.add_argument("path")
    z = sub.add_parser("zip-manifest"); z.add_argument("path")
    args = p.parse_args()
    if args.__dict__.get("root"):
        rows = inventory_local(args.root, args.matter)
        rels, families = exact_duplicate_relationships(rows)
        out = {"source_objects": rows, "relationships": rels, "duplicate_families": families}
    elif getattr(args, "path", None) and args.path.lower().endswith(".eml"):
        out = parse_eml(args.path)
    else:
        out = zip_manifest(args.path)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
