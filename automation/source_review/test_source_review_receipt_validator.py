import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "source_review_receipt_validator.py"
SCHEMA = HERE / "source_review_receipt_schema.json"
FIELDS = [
    "SOURCE_REVIEW_ID","SOURCE_SET_ID","SOURCE_ID","ORIGINAL_FILENAME","SHA256",
    "REVIEW_METHOD","REVIEW_STATUS","COVERAGE_STATUS","COVERAGE_LOCATORS",
    "FINDINGS_DISPOSITION","ARCHIVE_DISPOSITION","REVIEW_RUN_ID"
]


class Tests(unittest.TestCase):
    def row(self):
        return {
            "SOURCE_REVIEW_ID":"SRR-1","SOURCE_SET_ID":"SS-1","SOURCE_ID":"SRC-1",
            "ORIGINAL_FILENAME":"example.pdf","SHA256":"a"*64,"REVIEW_METHOD":"PDF_TEXT_PLUS_VISUAL",
            "REVIEW_STATUS":"COMPLETE","COVERAGE_STATUS":"FULL_TEXT_PLUS_VISUAL",
            "COVERAGE_LOCATORS":"pages 1-10","FINDINGS_DISPOSITION":"NO_NEW_MATERIAL_FINDINGS",
            "ARCHIVE_DISPOSITION":"REVIEW_COMPLETE_MOVE_NOT_AUTHORIZED","REVIEW_RUN_ID":"RUN-1"
        }

    def run_validator(self, rows, manifest_rows=None):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            receipts = td / "receipts.csv"
            with receipts.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
            cmd = ["python3", str(SCRIPT), str(SCHEMA), str(receipts)]
            if manifest_rows is not None:
                manifest = td / "manifest.csv"
                with manifest.open("w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=["SOURCE_SET_ID","SOURCE_ID"]); w.writeheader(); w.writerows(manifest_rows)
                cmd.append(str(manifest))
            return subprocess.run(cmd, capture_output=True, text=True)

    def test_complete_valid(self):
        self.assertEqual(self.run_validator([self.row()]).returncode, 0)

    def test_duplicate_source_in_source_set_blocked(self):
        a = self.row(); b = self.row(); b["SOURCE_REVIEW_ID"] = "SRR-2"
        self.assertNotEqual(self.run_validator([a,b]).returncode, 0)

    def test_complete_without_locators_blocked(self):
        r = self.row(); r["COVERAGE_LOCATORS"] = ""
        self.assertNotEqual(self.run_validator([r]).returncode, 0)

    def test_bad_hash_blocked(self):
        r = self.row(); r["SHA256"] = "bad"
        self.assertNotEqual(self.run_validator([r]).returncode, 0)

    def test_no_findings_still_requires_disposition(self):
        r = self.row(); r["FINDINGS_DISPOSITION"] = ""
        self.assertNotEqual(self.run_validator([r]).returncode, 0)

    def test_manifest_exact_coverage(self):
        m = [{"SOURCE_SET_ID":"SS-1","SOURCE_ID":"SRC-1"}]
        self.assertEqual(self.run_validator([self.row()], m).returncode, 0)

    def test_manifest_missing_receipt_blocked(self):
        m = [
            {"SOURCE_SET_ID":"SS-1","SOURCE_ID":"SRC-1"},
            {"SOURCE_SET_ID":"SS-1","SOURCE_ID":"SRC-2"}
        ]
        self.assertNotEqual(self.run_validator([self.row()], m).returncode, 0)


if __name__ == "__main__":
    unittest.main()
