from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kernel import evaluate  # noqa: E402


EXAMPLES = ROOT / "examples"


class EvidenceClosureKernelTests(unittest.TestCase):
    def run_example(self, name: str) -> tuple[dict, Path, tempfile.TemporaryDirectory[str]]:
        temp_dir = tempfile.TemporaryDirectory()
        input_dir = Path(temp_dir.name) / "input"
        output_dir = Path(temp_dir.name) / "output"
        shutil.copytree(EXAMPLES / name, input_dir)
        result = evaluate(input_dir, output_dir)
        return result, output_dir, temp_dir

    def test_supported_requires_review_not_release(self) -> None:
        result, output_dir, temp_dir = self.run_example("q1-minimal")
        self.addCleanup(temp_dir.cleanup)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["claim_status"], "supported")
        self.assertFalse(result["release_ready"])
        self.assertEqual(result["review_state"], "ready_for_review")
        self.assertTrue((output_dir / "claim.json").exists())
        self.assertTrue((output_dir / "provenance.json").exists())

    def test_main_rule_failure_is_not_supported(self) -> None:
        result, _, temp_dir = self.run_example("q1-not-supported")
        self.addCleanup(temp_dir.cleanup)
        self.assertEqual(result["claim_status"], "not_supported")
        self.assertEqual(result["validation_status"], "failed")

    def test_missing_independent_validation_is_inconclusive(self) -> None:
        result, _, temp_dir = self.run_example("q1-inconclusive")
        self.addCleanup(temp_dir.cleanup)
        self.assertEqual(result["claim_status"], "inconclusive")
        self.assertEqual(result["validation_status"], "inconclusive")

    def test_provenance_mismatch_is_not_evaluable(self) -> None:
        result, output_dir, temp_dir = self.run_example("q1-invalid-provenance")
        self.addCleanup(temp_dir.cleanup)
        self.assertEqual(result["claim_status"], "not_evaluable")
        self.assertFalse(result["provenance_valid"])
        self.assertFalse(result["release_ready"])
        verdict = json.loads((output_dir / "validation-verdict.json").read_text(encoding="utf-8"))
        self.assertEqual(verdict["status"], "not_evaluable")

    def test_missing_question_fields_blocks_without_silent_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            input_dir = Path(temp_name) / "input"
            output_dir = Path(temp_name) / "output"
            input_dir.mkdir()
            (input_dir / "question.json").write_text(
                json.dumps({"id": "Q-001", "text": "incomplete"}), encoding="utf-8"
            )
            result = evaluate(input_dir, output_dir)
            self.assertEqual(result["status"], "needs_clarification")
            self.assertEqual(result["claim_status"], "not_evaluable")
            self.assertIn("question.estimand", result["blockers"])
            self.assertIn("question.decision_rule", result["blockers"])

    def test_duplicate_gene_id_is_terminal_input_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            input_dir = Path(temp_name) / "input"
            output_dir = Path(temp_name) / "output"
            shutil.copytree(EXAMPLES / "q1-minimal", input_dir)
            (input_dir / "pa_effects.tsv").write_text(
                "gene_id\tlog2fc\nG1\t2.0\nG1\t1.0\n", encoding="utf-8"
            )
            result = evaluate(input_dir, output_dir)
            self.assertEqual(result["status"], "failed_terminal")
            self.assertEqual(result["error_code"], "duplicate_id")
            self.assertFalse(result["release_ready"])

    def test_same_fixture_is_repeatable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            input_dir = Path(temp_name) / "input"
            output_a = Path(temp_name) / "output-a"
            output_b = Path(temp_name) / "output-b"
            shutil.copytree(EXAMPLES / "q1-minimal", input_dir)
            first = evaluate(input_dir, output_a)
            second = evaluate(input_dir, output_b)
            self.assertEqual(first, second)
            for filename in ("observables.json", "validation-verdict.json", "claim.json", "provenance.json"):
                self.assertEqual(
                    (output_a / filename).read_bytes(),
                    (output_b / filename).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()

