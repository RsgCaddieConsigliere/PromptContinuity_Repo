from __future__ import annotations

from .constants import ProtectionClass
from .identity import deterministic_transaction_id
from .state_machine import validate_action


def mutation_eligibility(*, protection_class: str, sticky_protected: bool = False, path_escape: bool = False, collision_status: str = "CLEAR") -> tuple[bool, str]:
    if sticky_protected:
        return False, "STICKY_PROTECTED"
    if path_escape:
        return False, "PATH_ESCAPE"
    if collision_status != "CLEAR":
        return False, f"COLLISION_{collision_status}"
    if protection_class not in {ProtectionClass.MUTABLE_WORK_PRODUCT.value, ProtectionClass.DERIVATIVE.value}:
        return False, f"PROTECTION_{protection_class}_NON_MUTABLE"
    return True, ""


def make_transaction(
    *,
    action: str,
    file_instance_id: str,
    drive_id: str,
    old_parent: str,
    old_name: str,
    expected_fixity: str,
    protection_class: str,
    sticky_protected: bool = False,
    path_escape: bool = False,
    collision_status: str = "CLEAR",
    new_parent: str | None = None,
    new_name: str | None = None,
    reason: str = "",
) -> dict:
    act = validate_action(action)
    target_parent = new_parent or old_parent
    target_name = new_name or old_name
    source_descriptor = f"{old_parent}/{old_name}"
    destination_descriptor = f"{target_parent}/{target_name}"
    eligible, block_reason = mutation_eligibility(
        protection_class=protection_class,
        sticky_protected=sticky_protected,
        path_escape=path_escape,
        collision_status=collision_status,
    )
    return {
        "tx_id": deterministic_transaction_id(
            file_instance_id=file_instance_id,
            action=act.value,
            source_path=source_descriptor,
            destination_path=destination_descriptor,
            expected_fixity=expected_fixity,
        ),
        "file_instance_id": file_instance_id,
        "action": act.value,
        "state": "DRAFT",
        "drive_id": drive_id,
        "old_parent_id": old_parent,
        "old_name": old_name,
        "expected_fixity": expected_fixity,
        "new_parent_id": target_parent,
        "new_name": target_name,
        "reason": reason,
        "protection_class": protection_class,
        "eligibility_status": "ELIGIBLE" if eligible else "BLOCKED",
        "block_reason": block_reason,
        "collision_status": collision_status,
        "policy_authorized": False,
        "hitl_required": True,
        "approved_by": "",
        "approved_at": "",
        "rollback_action": {"parent_id": old_parent, "name": old_name},
    }
