from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "extensions" / "bio-multiqc" / "scripts" / "run_multiqc.py"
CONFIG = ROOT / "extensions" / "bio-multiqc" / "config" / "multiqc_config.yaml"
FIXTURE = ROOT / "tests" / "fixtures" / "multiqc"
MULTIQC = ROOT / ".venv" / "Scripts" / "multiqc.exe"


def load_json(path: Path) -> dict:
    raw = path.read_bytes()
    for encoding in ("utf-8", "gb18030", "cp1252"):
        try:
            return json.loads(raw.decode(encoding))
        except UnicodeDecodeError:
            continue
    raise AssertionError(f"cannot decode JSON artifact: {path}")


class MultiQCVerticalSliceTest(unittest.TestCase):
    def run_wrapper(
        self, input_dir: Path, output_dir: Path, *, expected_total: int = 10000
    ) -> dict:
        command = [
            sys.executable,
            str(WRAPPER),
            "--input",
            str(input_dir),
            "--output",
            str(output_dir),
            "--config",
            str(CONFIG),
            "--multiqc-bin",
            str(MULTIQC),
            "--preset",
            "fastqc-multiqc-mvp",
            "--expected-total-sequences",
            str(expected_total),
        ]
        completed = subprocess.run(
            command, cwd=ROOT, check=False, capture_output=True, text=True
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"wrapper failed\nstdout={completed.stdout}\nstderr={completed.stderr}",
        )
        return json.loads(completed.stdout.strip().splitlines()[-1])

    def test_clean_entry_generates_content_verified_report(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bio-spec-multiqc-") as temp:
            temp_root = Path(temp)
            input_one = temp_root / "input-one"
            output_one = temp_root / "output-one"
            shutil.copytree(FIXTURE, input_one)

            verdict = self.run_wrapper(input_one, output_one)

            self.assertTrue(verdict["ok"])
            self.assertTrue(verdict["release_ready"])
            self.assertEqual(verdict["verification_errors"], [])
            self.assertEqual(verdict["runtime"]["multiqc"], "multiqc, version 1.35")

            data_path = output_one / "multiqc_report_data" / "multiqc_data.json"
            data = load_json(data_path)
            fastqc = data["report_general_stats_data"]["fastqc"]["test_R1"]
            self.assertEqual(fastqc["total_sequences"], 10000)
            self.assertEqual(fastqc["avg_sequence_length"], 100)
            self.assertEqual(fastqc["percent_gc"], 48)
            self.assertIn(
                "FastQC",
                output_one.joinpath("multiqc_report.html")
                .read_bytes()
                .decode("utf-8", errors="replace"),
            )

    def test_changed_fixture_changes_verified_artifact(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bio-spec-multiqc-change-") as temp:
            temp_root = Path(temp)
            input_one = temp_root / "input-one"
            input_two = temp_root / "input-two"
            output_one = temp_root / "output-one"
            output_two = temp_root / "output-two"
            shutil.copytree(FIXTURE, input_one)
            shutil.copytree(FIXTURE, input_two)
            fixture_two = input_two / "sample_fastqc" / "fastqc_data.txt"
            fixture_two.write_text(
                fixture_two.read_text(encoding="utf-8").replace(
                    "Total Sequences\t10000", "Total Sequences\t12345"
                ),
                encoding="utf-8",
            )

            first = self.run_wrapper(input_one, output_one)
            second = self.run_wrapper(input_two, output_two, expected_total=12345)

            first_data = load_json(
                output_one / "multiqc_report_data" / "multiqc_data.json"
            )
            second_data = load_json(
                output_two / "multiqc_report_data" / "multiqc_data.json"
            )
            self.assertEqual(
                first_data["report_general_stats_data"]["fastqc"]["test_R1"][
                    "total_sequences"
                ],
                10000,
            )
            self.assertEqual(
                second_data["report_general_stats_data"]["fastqc"]["test_R1"][
                    "total_sequences"
                ],
                12345,
            )
            self.assertNotEqual(
                load_json(output_one / "input-manifest.json")[
                    "sha256"
                ],
                load_json(output_two / "input-manifest.json")[
                    "sha256"
                ],
            )
            self.assertTrue(first["ok"] and second["ok"])

    def test_missing_executable_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bio-spec-multiqc-missing-") as temp:
            temp_root = Path(temp)
            input_dir = temp_root / "input"
            output_dir = temp_root / "output"
            shutil.copytree(FIXTURE, input_dir)
            command = [
                sys.executable,
                str(WRAPPER),
                "--input",
                str(input_dir),
                "--output",
                str(output_dir),
                "--config",
                str(CONFIG),
                "--multiqc-bin",
                "missing-multiqc-executable",
                "--preset",
                "fastqc-multiqc-mvp",
            ]
            completed = subprocess.run(
                command, cwd=ROOT, check=False, capture_output=True, text=True
            )
            self.assertEqual(completed.returncode, 2)
            verdict = load_json(output_dir / "multiqc-verdict.json")
            self.assertFalse(verdict["ok"])
            self.assertFalse(verdict["release_ready"])
            self.assertIn("not found", verdict["error"])


if __name__ == "__main__":
    unittest.main()
