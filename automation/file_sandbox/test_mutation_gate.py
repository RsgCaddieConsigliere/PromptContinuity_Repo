import csv, json, subprocess, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("mutation_gate.py")
FIELDS = ["ACTION_ID","BATCH_ID","ACTION_TYPE","SOURCE_PATH","TARGET_PATH","PROVIDER_ID","CURRENT_PARENT_ID","TARGET_PARENT_ID","EXPECTED_SHA256","HITL_STATUS","N13_STATUS","AUTH_ID","NOTES"]

class GateTests(unittest.TestCase):
    def setup_env(self):
        td = tempfile.TemporaryDirectory(); root = Path(td.name)
        src = root / "source"; canary = root / "canary"; src.mkdir(); canary.mkdir()
        (src / "a.txt").write_text("alpha", encoding="utf-8")
        auth = {"AUTH_ID":"AUTH-1","CANARY_ROOT":str(canary),"ALLOWED_ACTIONS":["COPY","MKDIR","WRITE_NEW","RENAME","MOVE"],"CANARY_ONLY":"YES","DELETE_ALLOWED":"NO","SOURCE_MUTATION_AUTHORITY":"NOT_GRANTED","HITL_STATUS":"APPROVED"}
        ap = root / "auth.json"; ap.write_text(json.dumps(auth), encoding="utf-8")
        return td, root, src, canary, ap
    def run_batch(self, root, auth, row, execute=False):
        bp = root / "batch.csv"; rp = root / "receipt.csv"
        with bp.open("w", newline="", encoding="utf-8") as f:
            w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerow(row)
        cmd=["python3",str(SCRIPT),"--auth",str(auth),"--batch",str(bp),"--receipt",str(rp)]
        if execute: cmd.append("--execute")
        p=subprocess.run(cmd,capture_output=True,text=True)
        with rp.open(newline="",encoding="utf-8") as f: rec=list(csv.DictReader(f))[0]
        return p, rec
    def base(self, action, src, dst):
        return dict.fromkeys(FIELDS, "") | {"ACTION_ID":"A1","BATCH_ID":"B1","ACTION_TYPE":action,"SOURCE_PATH":str(src) if src else "","TARGET_PATH":str(dst) if dst else "","HITL_STATUS":"APPROVED","N13_STATUS":"PASS","AUTH_ID":"AUTH-1","NOTES":"new derivative"}
    def test_dry_run_does_not_mutate(self):
        td, root, src, canary, auth=self.setup_env()
        try:
            dst=canary/"a.txt"; p,r=self.run_batch(root,auth,self.base("COPY",src/"a.txt",dst),False)
            self.assertEqual(p.returncode,0); self.assertFalse(dst.exists()); self.assertEqual(r["STATUS"],"VALIDATED")
        finally: td.cleanup()
    def test_copy_executes_inside_canary(self):
        td, root, src, canary, auth=self.setup_env()
        try:
            dst=canary/"a.txt"; p,r=self.run_batch(root,auth,self.base("COPY",src/"a.txt",dst),True)
            self.assertEqual(p.returncode,0); self.assertEqual(dst.read_text(),"alpha"); self.assertEqual(r["STATUS"],"EXECUTED")
        finally: td.cleanup()
    def test_rename_inside_canary(self):
        td, root, src, canary, auth=self.setup_env()
        try:
            a=canary/"a.txt"; a.write_text("alpha"); b=canary/"b.txt"
            p,r=self.run_batch(root,auth,self.base("RENAME",a,b),True)
            self.assertEqual(p.returncode,0); self.assertFalse(a.exists()); self.assertTrue(b.exists())
        finally: td.cleanup()
    def test_rename_outside_canary_blocked(self):
        td, root, src, canary, auth=self.setup_env()
        try:
            p,r=self.run_batch(root,auth,self.base("RENAME",src/"a.txt",canary/"a.txt"),False)
            self.assertNotEqual(p.returncode,0); self.assertEqual(r["REASON"],"RENAME_MOVE_MUST_STAY_INSIDE_CANARY")
        finally: td.cleanup()
    def test_restricted_component_blocked(self):
        td, root, src, canary, auth=self.setup_env()
        try:
            dst=canary/"0000X-Files-Restricted"/"a.txt"
            p,r=self.run_batch(root,auth,self.base("COPY",src/"a.txt",dst),False)
            self.assertNotEqual(p.returncode,0); self.assertEqual(r["REASON"],"ARCHIVE_OR_RESTRICTED_COMPONENT")
        finally: td.cleanup()
    def test_archive_component_blocked(self):
        td, root, src, canary, auth=self.setup_env()
        try:
            dst=canary/"99_ARCHIVE"/"a.txt"
            p,r=self.run_batch(root,auth,self.base("COPY",src/"a.txt",dst),False)
            self.assertNotEqual(p.returncode,0); self.assertEqual(r["REASON"],"ARCHIVE_OR_RESTRICTED_COMPONENT")
        finally: td.cleanup()
    def test_unapproved_row_blocked(self):
        td, root, src, canary, auth=self.setup_env()
        try:
            row=self.base("COPY",src/"a.txt",canary/"a.txt"); row["HITL_STATUS"]="PENDING"
            p,r=self.run_batch(root,auth,row,False)
            self.assertNotEqual(p.returncode,0); self.assertEqual(r["REASON"],"ROW_HITL_NOT_APPROVED")
        finally: td.cleanup()
    def test_delete_action_blocked(self):
        td, root, src, canary, auth=self.setup_env()
        try:
            row=self.base("DELETE",src/"a.txt",None)
            p,r=self.run_batch(root,auth,row,False)
            self.assertNotEqual(p.returncode,0); self.assertEqual(r["REASON"],"ACTION_NOT_AUTHORIZED")
        finally: td.cleanup()

if __name__ == "__main__": unittest.main()
