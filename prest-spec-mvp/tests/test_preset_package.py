from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = PACKAGE_ROOT / "scripts" / "validate_package.py"


class BioSpecMvpPresetTests(unittest.TestCase):
    def test_package_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--package", str(PACKAGE_ROOT)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["errors"], [])

    def test_manifest_uses_only_official_item_types(self) -> None:
        manifest = yaml.safe_load((PACKAGE_ROOT / "preset.yml").read_text(encoding="utf-8"))
        entries = manifest["provides"]["templates"]
        self.assertEqual(
            {entry["type"] for entry in entries},
            {"template", "command"},
        )
        self.assertNotIn("contract", {entry["type"] for entry in entries})
        self.assertEqual(set(manifest["provides"]), {"templates"})

    def test_all_referenced_files_exist(self) -> None:
        manifest = yaml.safe_load((PACKAGE_ROOT / "preset.yml").read_text(encoding="utf-8"))
        for entry in manifest["provides"]["templates"]:
            referenced = PACKAGE_ROOT / Path(entry["file"])
            self.assertTrue(referenced.is_file(), entry["file"])

    def test_core_template_anchors_are_preserved(self) -> None:
        expected = {
            "spec-template.md": ["## User Scenarios & Testing", "## Requirements", "## Success Criteria"],
            "plan-template.md": [
                "## Technical Context",
                "## Capability Bindings",
                "required_capabilities:",
                "skill_id:",
                "## Constitution Check",
                "## Project Structure",
            ],
            "tasks-template.md": ["## Phase 3: User Story 1", "## Dependencies and Execution Order"],
            "constitution-template.md": ["## Core Principles", "## Governance"],
            "checklist-template.md": ["## Research Framing", "## Requirement Quality"],
        }
        for filename, anchors in expected.items():
            content = (PACKAGE_ROOT / "templates" / filename).read_text(encoding="utf-8")
            for anchor in anchors:
                self.assertIn(anchor, content, f"{filename}: {anchor}")

    def test_runtime_and_nested_package_boundaries_are_absent(self) -> None:
        for name in ("artifacts", "run-working", "workflow.yml"):
            self.assertFalse((PACKAGE_ROOT / name).exists(), name)
        self.assertFalse((PACKAGE_ROOT / "presets").exists())
        self.assertFalse((PACKAGE_ROOT / "workflows").exists())
        self.assertFalse((PACKAGE_ROOT / "research-evidence-kernel").exists())


if __name__ == "__main__":
    unittest.main()
