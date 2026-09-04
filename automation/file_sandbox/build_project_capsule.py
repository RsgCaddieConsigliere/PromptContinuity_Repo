#!/usr/bin/env python3
"""Build a compact project capsule from a Project Portfolio CSV row and optional queue CSV.

This helper does not read native evidence. It packages structured current state for token-efficient cross-AI handoff.
"""
from __future__ import annotations
import argparse, csv
from datetime import datetime, timezone
from pathlib import Path

def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_registry", type=Path)
    ap.add_argument("project_id")
    ap.add_argument("--job-queue", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    projects = rows(args.project_registry)
    project = next((r for r in projects if r.get("project_id") == args.project_id), None)
    if not project:
        raise SystemExit(f"Project not found: {args.project_id}")
    jobs = []
    if args.job_queue and args.job_queue.exists():
        jobs = [r for r in rows(args.job_queue) if r.get("project_id") == args.project_id and r.get("status") not in {"COMPLETE", "CANCELLED", "SUPERSEDED"}]
    generated = datetime.now(timezone.utc).isoformat()
    lines = [
        "# PROJECT CONTROL CAPSULE", "",
        f"Project ID: `{project.get('project_id','')}`",
        f"Project name: {project.get('project_name','')}",
        f"Generated: {generated}",
        "Purpose: compact cross-AI state handoff. Derivative state only; native/official sources control.", "",
        "## Target outcome", project.get("target_outcome", ""), "",
        "## Status / phase", f"{project.get('status','')} / {project.get('current_phase','')}", "",
        "## Current source freeze", project.get("current_source_freeze_id", "") or "NONE / NOT RECORDED", "",
        "## Completion gate", project.get("completion_gate_status", ""), "",
        "## Current next action", project.get("next_action", ""), "",
        "## Recommended execution surface", project.get("next_best_platform", ""), "",
        "## Quantified open state",
        f"- New files: {project.get('new_files_count','')}",
        f"- Changed files: {project.get('changed_files_count','')}",
        f"- Gaps: {project.get('open_gaps_count','')}",
        f"- Conflicts: {project.get('open_conflicts_count','')}",
        f"- Decisions: {project.get('open_decisions_count','')}",
        f"- Verification queue: {project.get('verification_queue_count','')}", "",
        "## Open jobs"
    ]
    if jobs:
        for j in jobs:
            lines.append(f"- `{j.get('job_id','')}` [{j.get('status','')}] {j.get('objective','')} -> writer={j.get('writer_platform','')} reviewer={j.get('reviewer_platform','')}")
    else:
        lines.append("- None recorded")
    lines += ["", "## Guardrails", "- Do not infer completion from missing rows.", "- Do not mutate source files from this capsule.", "- Reopen native/official sources for material promotion or disputed context.", "- AI-to-AI agreement is not corroboration."]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
