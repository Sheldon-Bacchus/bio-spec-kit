from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "extensions" / "bio-integration" / "scripts" / "run_shared_integration.py"
FIXTURE = ROOT / "tests" / "fixtures" / "shared-integration"


class SharedIntegrationMVPTest(unittest.TestCase):
    def run_wrapper(self, output: Path, pa: Path | None = None, luad: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--pa",
                str(pa or FIXTURE / "pa_deg.tsv"),
                "--luad",
                str(luad or FIXTURE / "luad_deg.tsv"),
                "--output",
                str(output),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_clean_fixture_writes_four_direction_strata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            result = self.run_wrapper(output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            verdict = json.loads((output / "integration-verdict.json").read_text(encoding="utf-8"))
            self.assertEqual(verdict["shared_count"], 4)
            self.assertEqual(verdict["category_counts"], {"UpUp": 1, "DownDown": 1, "UpDown": 1, "DownUp": 1})
            self.assertFalse(verdict["release_ready"])
            self.assertEqual(json.loads((output / "claim.json").read_text(encoding="utf-8"))["status"], "descriptive_only")

    def test_duplicate_gene_fails_closed_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pa = root / "pa.tsv"
            shutil.copyfile(FIXTURE / "pa_deg.tsv", pa)
            with pa.open("a", encoding="utf-8") as handle:
                handle.write("GENE_A\t3.0\tTRUE\tup\n")
            output = root / "run"
            result = self.run_wrapper(output, pa=pa)
            self.assertEqual(result.returncode, 2)
            verdict = json.loads((output / "integration-verdict.json").read_text(encoding="utf-8"))
            self.assertEqual(verdict["error_code"], "duplicate_gene_id")
            self.assertFalse(verdict["release_ready"])

    def test_direction_conflict_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pa = root / "pa.tsv"
            text = (FIXTURE / "pa_deg.tsv").read_text(encoding="utf-8").replace("GENE_A\t2.0\tTRUE\tup", "GENE_A\t2.0\tTRUE\tdown")
            pa.write_text(text, encoding="utf-8")
            output = root / "run"
            result = self.run_wrapper(output, pa=pa)
            self.assertEqual(result.returncode, 2)
            verdict = json.loads((output / "integration-verdict.json").read_text(encoding="utf-8"))
            self.assertEqual(verdict["error_code"], "direction_effect_conflict")

    def test_row_order_is_canonical_and_input_change_propagates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pa_reordered = root / "pa-reordered.tsv"
            with (FIXTURE / "pa_deg.tsv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle, delimiter="\t"))
            with pa_reordered.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t", lineterminator="\n")
                writer.writeheader()
                writer.writerows(reversed(rows))
            first = root / "first"
            second = root / "second"
            self.assertEqual(self.run_wrapper(first).returncode, 0)
            self.assertEqual(self.run_wrapper(second, pa=pa_reordered).returncode, 0)
            self.assertEqual((first / "shared_all.tsv").read_bytes(), (second / "shared_all.tsv").read_bytes())
            first_verdict = json.loads((first / "integration-verdict.json").read_text(encoding="utf-8"))
            changed = root / "pa-changed.tsv"
            changed.write_text((FIXTURE / "pa_deg.tsv").read_text(encoding="utf-8").replace("GENE_A\t2.0", "GENE_A\t2.5"), encoding="utf-8")
            third = root / "third"
            self.assertEqual(self.run_wrapper(third, pa=changed).returncode, 0)
            third_verdict = json.loads((third / "integration-verdict.json").read_text(encoding="utf-8"))
            self.assertNotEqual(first_verdict["run_id"], third_verdict["run_id"])
            self.assertNotEqual((first / "shared_all.tsv").read_bytes(), (third / "shared_all.tsv").read_bytes())


if __name__ == "__main__":
    unittest.main()
