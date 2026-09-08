import pytest
from corpus_reconcile.constants import TxAction, TxState
from corpus_reconcile.state_machine import Transaction, validate_action
from corpus_reconcile.reconcile import exact_duplicate_relationships
from corpus_reconcile.naming import propose_name
from corpus_reconcile.email_relationships import reused_attachment_candidates
from corpus_reconcile.zip_manifest import zip_manifest

def test_happy_path():
    tx = Transaction("TXN-1", TxAction.RENAME)
    for state in [TxState.HITL_PENDING, TxState.APPROVED, TxState.PRECONDITION_CHECK, TxState.EXECUTING, TxState.APPLIED, TxState.READBACK_VERIFIED, TxState.CLOSED]:
        tx = tx.transition(state)
    assert tx.state == TxState.CLOSED

def test_illegal_skip_rejected():
    with pytest.raises(ValueError):
        Transaction("TXN-1", TxAction.RENAME).transition(TxState.EXECUTING)

def test_delete_not_supported():
    with pytest.raises(ValueError):
        validate_action("DELETE")

def test_exact_duplicates():
    rows = [{"src_id":"A","local_sha256":"abc","original_path":"/a"},{"src_id":"B","local_sha256":"abc","original_path":"/b"},{"src_id":"C","local_sha256":"def","original_path":"/c"}]
    rels, fams = exact_duplicate_relationships(rows)
    assert len(fams) == 1 and len(rels) == 1 and rels[0]["confidence"] == 1.0

def test_name_is_deterministic():
    assert propose_name(date="2026-04-14", matter="AAA-CSAA", object_type="EMAIL", source="CSAA", description="Repair Payment", extension="pdf") == "2026-04-14__AAA-CSAA__EMAIL__CSAA__Repair-Payment__v01.pdf"

def test_reused_attachment_candidate():
    emails = [{"message_id":"<a>","attachments":[{"ordinal":1,"filename":"x.txt","sha256":"abc"}]},{"message_id":"<b>","attachments":[{"ordinal":1,"filename":"renamed.txt","sha256":"abc"}]}]
    out = reused_attachment_candidates(emails)
    assert len(out) == 1 and out[0]["relationship_type"] == "REUSED_ATTACHMENT_BYTES"

def test_zip_manifest(tmp_path):
    import zipfile
    p = tmp_path / "bundle.zip"
    with zipfile.ZipFile(p, "w") as z:
        z.writestr("a.txt", b"alpha"); z.writestr("nested/b.txt", b"beta")
    out = zip_manifest(p)
    assert out["member_count"] == 2 and all(len(m["sha256"]) == 64 for m in out["members"])
