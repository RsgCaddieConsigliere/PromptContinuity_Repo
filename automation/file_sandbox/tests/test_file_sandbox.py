import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "scan_manifest.py"
DELTA = ROOT / "delta_scan.py"

class FileSandboxTests(unittest.TestCase):
    def test_scan_dedup_and_delta(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            src = td / "source"
            src.mkdir()
            (src / "a.txt").write_text("alpha\n", encoding="utf-8")
            (src / "a-copy.txt").write_text("alpha\n", encoding="utf-8")
            (src / "b.txt").write_text("beta\n", encoding="utf-8")
            out1 = td / "out1"
            subprocess.run([sys.executable, str(SCAN), str(src), "--out-dir", str(out1)], check=True)
            summary = json.loads((out1 / "SCAN_SUMMARY.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["files_scanned"], 3)
            self.assertEqual(summary["unique_hashes"], 2)
            self.assertEqual(summary["duplicate_groups"], 1)

            (src / "b.txt").write_text("beta changed\n", encoding="utf-8")
            (src / "a.txt").rename(src / "a-moved.txt")
            (src / "c.txt").write_text("gamma\n", encoding="utf-8")
            out2 = td / "out2"
            subprocess.run([sys.executable, str(SCAN), str(src), "--out-dir", str(out2)], check=True)
            delta = td / "delta.csv"
            subprocess.run([sys.executable, str(DELTA), str(out1 / "MASTER_MANIFEST.csv"), str(out2 / "MASTER_MANIFEST.csv"), "--out", str(delta)], check=True)
            with delta.open(newline="", encoding="utf-8") as f:
                statuses = [r["status"] for r in csv.DictReader(f)]
            self.assertIn("MOVED_SAME_CONTENT", statuses)
            self.assertIn("MODIFIED", statuses)
            self.assertIn("NEW", statuses)
            self.assertIn("UNCHANGED", statuses)

if __name__ == "__main__":
    unittest.main()
