# BioSpec MVP validation boundary

The package checks are intentionally structural and deterministic:

1. `preset.yml` parses as YAML and has the official top-level metadata;
2. every provided item uses `template`, `command`, or `script`;
3. every referenced file is inside the package and exists;
4. item names are unique and strategies are valid;
5. the five core template anchors and the capability-binding anchors are
   present;
6. the package has no nested preset or workflow manifest;
7. the package has no runtime directory or generated result output.

These checks prove package shape and fail-closed reference resolution. They do
not prove that an agent follows the guidance, that a scientific method is
valid, that a selected Bio Skill is sufficient, or that a generated claim is
true.
