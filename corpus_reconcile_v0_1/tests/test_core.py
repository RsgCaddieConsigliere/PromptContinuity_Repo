import hashlib
import io
import zipfile

import pytest

from corpus_reconcile.constants import ProtectionClass, TxAction, TxState
from corpus_reconcile.email_parser import parse_eml
from corpus_reconcile.email_relationships import reused_attachment_candidates
from corpus_reconcile.identity import content_id_from_sha256, first_observation_file_instance_id
from corpus_reconcile.inventory import inventory_local
from corpus_reconcile.naming import propose_name
from corpus_reconcile.planner import make_transaction, mutation_eligibility
from corpus_reconcile.reconcile import exact_duplicate_relationships
from corpus_reconcile.sampling import stratified_sample
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


def test_stratified_sample_is_deterministic_and_diverse():
    rows = [
        {"file_instance_id": "I-1", "protection_class": "SOURCE_IMMUTABLE", "mime_type": "application/pdf", "original_relative_path": "a.pdf", "fixity_status": "HASHED_STABLE"},
        {"file_instance_id": "I-2", "protection_class": "DERIVATIVE", "mime_type": "application/pdf", "original_relative_path": "b.pdf", "fixity_status": "HASHED_STABLE"},
        {"file_instance_id": "I-3", "protection_class": "UNKNOWN", "mime_type": "text/plain", "original_relative_path": "c.txt", "fixity_status": "HASH_ERROR"},
        {"file_instance_id": "I-4", "protection_class": "DERIVATIVE", "mime_type": "text/plain", "original_relative_path": "d.txt", "fixity_status": "HASHED_STABLE"},
    ]
    first = stratified_sample(rows, max_objects=3, run_seed="SEED-1")
    second = stratified_sample(rows, max_objects=3, run_seed="SEED-1")
    assert [r["file_instance_id"] for r in first] == [r["file_instance_id"] for r in second]
    assert len({(r["protection_class"], r["mime_type"].split("/", 1)[0]) for r in first}) >= 2


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
    path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("a.txt", b"alpha")
        archive.writestr("nested/b.txt", b"beta")
    out = zip_manifest(path)
    assert out["manifest_status"] == "MANIFESTED_STABLE"
    assert out["fixity_status"] == "HASHED_STABLE"
    assert out["member_count"] == 2 and all(len(member["sha256"]) == 64 for member in out["members"])


def test_eml_parser_binds_metadata_and_attachments_to_one_guarded_stream(monkeypatch, tmp_path):
    raw = (
        b"Message-ID: <stable@example.test>\r\n"
        b"Date: Tue, 8 Sep 2026 00:00:00 -0700\r\n"
        b"From: sender@example.test\r\n"
        b"To: receiver@example.test\r\n"
        b"Subject: Stable EML\r\n"
        b"MIME-Version: 1.0\r\n"
        b"Content-Type: multipart/mixed; boundary=BOUNDARY\r\n\r\n"
        b"--BOUNDARY\r\nContent-Type: text/plain\r\n\r\nBody\r\n"
        b"--BOUNDARY\r\nContent-Type: text/plain\r\n"
        b"Content-Disposition: attachment; filename=test.txt\r\n\r\nalpha\r\n"
        b"--BOUNDARY--\r\n"
    )
    sha = hashlib.sha256(raw).hexdigest()
    sentinel = tmp_path / "mail.eml"
    sentinel.write_bytes(b"different-on-disk-bytes")

    def guarded(_path):
        return {
            "data": raw,
            "sha256": sha,
            "fixity_status": "HASHED_STABLE",
            "hash_error": "",
            "size_bytes_pre": len(raw),
            "size_bytes_post": len(raw),
            "mtime_ns_pre": 1,
            "mtime_ns_post": 1,
        }

    monkeypatch.setattr("corpus_reconcile.email_parser.read_bytes_with_stat_guard", guarded)
    out = parse_eml(sentinel)
    assert out["parse_status"] == "PARSED_STABLE"
    assert out["raw_mime_sha256"] == sha == out["sha256"]
    assert out["message_id"] == "<stable@example.test>"
    assert out["attachment_count"] == 1
    assert out["attachments"][0]["sha256"] == hashlib.sha256(b"alpha").hexdigest()


def test_zip_manifest_binds_members_to_one_guarded_stream(monkeypatch, tmp_path):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("a.txt", b"alpha")
        archive.writestr("b.txt", b"beta")
    raw = buffer.getvalue()
    sha = hashlib.sha256(raw).hexdigest()
    sentinel = tmp_path / "bundle.zip"
    sentinel.write_bytes(b"not-a-zip")

    def guarded(_path):
        return {
            "data": raw,
            "sha256": sha,
            "fixity_status": "HASHED_STABLE",
            "hash_error": "",
            "size_bytes_pre": len(raw),
            "size_bytes_post": len(raw),
            "mtime_ns_pre": 1,
            "mtime_ns_post": 1,
        }

    monkeypatch.setattr("corpus_reconcile.zip_manifest.read_bytes_with_stat_guard", guarded)
    out = zip_manifest(sentinel)
    assert out["manifest_status"] == "MANIFESTED_STABLE"
    assert out["zip_sha256"] == sha
    assert {m["name"] for m in out["members"]} == {"a.txt", "b.txt"}
    assert {m["sha256"] for m in out["members"]} == {
        hashlib.sha256(b"alpha").hexdigest(),
        hashlib.sha256(b"beta").hexdigest(),
    }
