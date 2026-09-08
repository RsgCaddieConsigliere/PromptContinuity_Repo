from __future__ import annotations
import uuid
from .state_machine import validate_action

def make_transaction(*, action: str, drive_id: str, old_parent: str, old_name: str, expected_fixity: str, new_parent: str | None = None, new_name: str | None = None, reason: str = "") -> dict:
    act = validate_action(action)
    return {
        "tx_id": f"TXN-{uuid.uuid4().hex[:12].upper()}",
        "action": act.value,
        "state": "HITL_PENDING",
        "drive_id": drive_id,
        "old_parent_id": old_parent,
        "old_name": old_name,
        "expected_fixity": expected_fixity,
        "new_parent_id": new_parent or old_parent,
        "new_name": new_name or old_name,
        "reason": reason,
        "policy_authorized": False,
        "hitl_required": True,
        "approved_by": "",
        "approved_at": "",
        "rollback_action": {"parent_id": old_parent, "name": old_name},
    }
