import pytest

from corpus_reconcile.constants import ProtectionClass, TxAction, TxState
from corpus_reconcile.email_relationships import reused_attachment_candidates
from corpus_reconcile.identity import content_id_from_sha256, first_observation_file_instance_id
from corpus_reconcile.inventory import inventory_local
from corpus_reconcile.naming import propose_name
from corpus_reconcile.planner import make_transaction, mutation_eligibility
from corpus_reconcile.reconcile import exact_duplicate_relationships
from corpus_reconcile.state_machine import Transaction, validate_action
from corpus_reconcile.zip_manifest import zip_manifest


def test_happy_path():
    tx = Transaction("TXN-1", TxAction.RENAME)
    for state in [
        TxState.HITL_PENDING,
        TxState.APPROVED,
        TxState.PRECONDITION_CHECK,
        TxState.EXECUTING,
        TxState.APPLIED,
        TxState.READBACK_VERIFIED,
        TxState.CLOSED,
    ]:
        tx = tx.transition(state)
    assert tx.state == TxState.CLOSED


def test_illegal_skip_rejected():
    with pytest.raises(ValueError):
        Transaction("TXN-1", TxAction.RENAME).transition(TxState.EXECUTING)


def test_delete_not_supported():
    with pytest.raises(ValueError):
        validate_action("DELETE")


def test_content_and_instance_identity_split():
    sha = "a" * 64
    content_a = content_id_from_sha256(sha)
    content_b = content_id_from_sha256(sha)
    instance_a = first_observation_file_instance_id(root_id="ROOT-1", original_relative_path="a/file.pdf", sha256=sha)
    instance_b = first_observation_file_instance_id(root_id="ROOT-1", original_relative_path="b/file.pdf", sha256=sha)
    assert content_a == content_b == f"sha256:{sha}"
    assert instance_a != instance_b


def test_instance_identity_persists_across_in_place_byte_change(tmp_path):
    path = tmp_path / "draft.txt"
    path.write_text("version one", encoding="utf-8")
    first = inventory_local(tmp_path, root_id="ROOT-1", run_id="RUN-1")[0]
    registry = {
        first["current_relative_path"]: {
            "file_instance_id": first["file_instance_id"],
            "original_relative_path": first["original_relative_path"],
            "protection_class": ProtectionClass.MUTABLE_WORK_PRODUCT.value,
        }
    }
    path.write_text("version two", encoding="utf-8")
    second = inventory_local(tmp_path, root_id="ROOT-1", run_id="RUN-2", instance_registry=registry)[0]
    assert first["file_instance_id"] == second["file_instance_id"]
    assert first["content_id"] != second["content_id"]


def test_unknown_and_sticky_are_nonmutable():
    eligible, reason = mutation_eligibility(protection_class=ProtectionClass.UNKNOWN.value)
    assert not eligible and "NON_MUTABLE" in reason
    eligible, reason = mutation_eligibility(
        protection_class=ProtectionClass.DERIVATIVE.value,
        sticky_protected=True,
    )
    assert not eligible and reason == "STICKY_PROTECTED"


def test_transaction_id_is_deterministic_and_starts_draft():
    kwargs = dict(
        action="RENAME",
        file_instance_id="FILE-ABC",
        drive_id="DRIVE-1",
        old_parent="PARENT-A",
        old_name="old.pdf",
        expected_fixity="sha256:abc",
        protection_class=ProtectionClass.DERIVATIVE.value,
        new_name="new.pdf",
        reason="test",
    )
    a = make_transaction(**kwargs)
    b = make_transaction(**kwargs)
    assert a["tx_id"] == b["tx_id"]
    assert a["state"] == "DRAFT"
    assert a["eligibility_status"] == "ELIGIBLE"


def test_exact_duplicates_do_not_auto_select_canonical():
    rows = [
        {"src_id": "A", "file_instance_id": "I-A", "local_sha256": "abc", "current_relative_path": "a"},
        {"src_id": "B", "file_instance_id": "I-B", "local_sha256": "abc", "current_relative_path": "b"},
        {"src_id": "C", "file_instance_id": "I-C", "local_sha256": "def", "current_relative_path": "c"},
    ]
    rels, fams = exact_duplicate_relationships(rows)
    assert len(fams) == 1 and len(rels) == 1
    assert fams[0]["canonical_src_id"] is None
    assert rels[0]["certainty"] == "CONFIRMED"


def test_name_is_deterministic():
    assert propose_name(
        date="2026-04-14",
        matter="AAA-CSAA",
        object_type="EMAIL",
        source="CSAA",
        description="Repair Payment",
        extension="pdf",
    ) == "2026-04-14__AAA-CSAA__EMAIL__CSAA__Repair-Payment__v01.pdf"


def test_reused_attachment_candidate():
    emails = [
        {"message_id": "<a>", "attachments": [{"ordinal": 1, "filename": "x.txt", "sha256": "abc"}]},
        {"message_id": "<b>", "attachments": [{"ordinal": 1, "filename": "renamed.txt", "sha256": "abc"}]},
    ]
    out = reused_attachment_candidates(emails)
    assert len(out) == 1 and out[0]["relationship_type"] == "REUSED_ATTACHMENT_BYTES"


def test_zip_manifest(tmp_path):
    import zipfile

    path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("a.txt", b"alpha")
        archive.writestr("nested/b.txt", b"beta")
    out = zip_manifest(path)
    assert out["member_count"] == 2 and all(len(member["sha256"]) == 64 for member in out["members"])
