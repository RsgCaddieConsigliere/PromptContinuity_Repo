import csv, subprocess, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "drive_wmr_manifest_validator.py"
SCHEMA = HERE / "drive_wmr_manifest_schema.json"
FIELDS = ["ACTION_ID","BATCH_ID","ORIGINAL_PROVIDER_ID","ORIGINAL_PARENT_ID","ORIGINAL_NAME","COPY_INBOUND_PARENT_ID","COPY_FINAL_PARENT_ID","PROPOSED_FINAL_NAME","HITL_STATUS","EXECUTION_STATUS"]

class Tests(unittest.TestCase):
    def run_rows(self, rows):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/"m.csv"
            with p.open("w", newline="", encoding="utf-8") as f:
                w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
            return subprocess.run(["python3",str(SCRIPT),str(SCHEMA),str(p)],capture_output=True,text=True)
    def base(self):
        return {"ACTION_ID":"A1","BATCH_ID":"B1","ORIGINAL_PROVIDER_ID":"OID","ORIGINAL_PARENT_ID":"PID","ORIGINAL_NAME":"draft.md","COPY_INBOUND_PARENT_ID":"CID1","COPY_FINAL_PARENT_ID":"CID2","PROPOSED_FINAL_NAME":"copy.md","HITL_STATUS":"PENDING","EXECUTION_STATUS":"NOT_STARTED"}
    def test_valid(self):
        self.assertEqual(self.run_rows([self.base()]).returncode,0)
    def test_duplicate_action_id_blocked(self):
        r=self.base(); self.assertNotEqual(self.run_rows([r,r.copy()]).returncode,0)
    def test_missing_identity_blocked(self):
        r=self.base(); r["ORIGINAL_PROVIDER_ID"]=""; self.assertNotEqual(self.run_rows([r]).returncode,0)
    def test_forbidden_component_blocked(self):
        r=self.base(); r["PROPOSED_FINAL_NAME"]="99_ARCHIVE/file.md"; self.assertNotEqual(self.run_rows([r]).returncode,0)
    def test_bad_status_blocked(self):
        r=self.base(); r["EXECUTION_STATUS"]="DONE"; self.assertNotEqual(self.run_rows([r]).returncode,0)

if __name__ == "__main__": unittest.main()
