#!/usr/bin/env python3
"""Cross-field validation for the bounded Research Core contracts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from typing import Any, Callable

from jsonschema import Draft202012Validator, FormatChecker


HEX256 = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
REQUIRED_RUN_FIELDS = {
    "repository",
    "input_manifest",
    "artifact_manifest",
    "command",
    "executable",
    "parameters",
    "environment",
    "reference_snapshots",
    "verifier",
}


class ContractValidationError(ValueError):
    """A deterministic contract or evidence validation failure."""


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractValidationError(f"cannot read JSON object {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractValidationError(f"JSON root is not an object: {path}")
    return value


def schema_errors(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = load_json_object(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    return [
        f"{schema_path.name} at {'.'.join(map(str, error.absolute_path)) or '<root>'}: "
        f"{error.message}"
        for error in errors
    ]


def ensure_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or HEX256.fullmatch(value) is None:
        raise ContractValidationError(f"{label} must be a lowercase SHA-256 digest")
    return value


def resolve_repository_path(value: Any, repo_root: Path, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ContractValidationError(f"{label} must be a non-empty path")
    if WINDOWS_ABSOLUTE.match(value) or value.startswith(("/", "\\")):
        raise ContractValidationError(f"{label} must be repository-relative: {value!r}")
    if "\\" in value:
        raise ContractValidationError(
            f"{label} must use POSIX separators for a portable evidence record: {value!r}"
        )
    relative = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in relative.parts):
        raise ContractValidationError(
            f"{label} must not contain '.', '..', or empty path components: {value!r}"
        )
    root = repo_root.resolve()
    resolved = (root / Path(*relative.parts)).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ContractValidationError(
            f"{label} resolves outside the repository: {value!r}"
        ) from exc
    return resolved


def resolve_run_path(value: Any, run_root: Path, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ContractValidationError(f"{label} must be a non-empty run-relative path")
    if WINDOWS_ABSOLUTE.match(value) or value.startswith(("/", "\\")) or "\\" in value:
        raise ContractValidationError(f"{label} must be run-relative and portable: {value!r}")
    relative = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in relative.parts):
        raise ContractValidationError(
            f"{label} must not contain '.', '..', or empty path components: {value!r}"
        )
    root = run_root.resolve()
    resolved = (root / Path(*relative.parts)).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ContractValidationError(f"{label} resolves outside the run root") from exc
    return resolved


def require_unique(values: list[Any], label: str) -> None:
    if len(values) != len(set(values)):
        raise ContractValidationError(f"{label} must contain unique values")


def validate_node_data(
    node: dict[str, Any],
    node_path: Path,
    repo_root: Path,
    node_schema: Path,
    seen_paths: set[Path] | None = None,
) -> None:
    errors = schema_errors(node, node_schema)
    if errors:
        raise ContractValidationError("; ".join(errors))
    if "status" in node:
        raise ContractValidationError(
            "static node capability contracts must not contain run status"
        )

    seen = seen_paths if seen_paths is not None else set()
    resolved_node_path = node_path.resolve()
    if resolved_node_path in seen:
        return
    seen.add(resolved_node_path)

    ports = node["ports"]
    port_ids = [port["port_id"] for port in ports]
    require_unique(port_ids, "ports.port_id")
    port_by_id = {port["port_id"]: port for port in ports}

    interface = node["public_interface"]
    for field, expected_direction in (("takes", "input"), ("emits", "output")):
        values = interface[field]
        require_unique(values, f"public_interface.{field}")
        for port_id in values:
            port = port_by_id.get(port_id)
            if port is None:
                raise ContractValidationError(
                    f"public_interface.{field} references unknown port {port_id!r}"
                )
            if port["direction"] != expected_direction:
                raise ContractValidationError(
                    f"public_interface.{field} references {port_id!r} with "
                    f"direction {port['direction']!r}, expected {expected_direction!r}"
                )
        expected_ports = {
            port["port_id"]
            for port in ports
            if port["direction"] == expected_direction
        }
        if set(values) != expected_ports:
            raise ContractValidationError(
                f"public_interface.{field} must expose exactly all "
                f"{expected_direction} ports"
            )

    named_outputs = node["named_outputs"]
    require_unique(
        [item["name"] for item in named_outputs],
        "named_outputs.name",
    )
    require_unique(
        [item["port_id"] for item in named_outputs],
        "named_outputs.port_id",
    )
    for item in named_outputs:
        port = port_by_id.get(item["port_id"])
        if port is None or port["direction"] != "output":
            raise ContractValidationError(
                f"named_outputs.port_id must reference an output port: {item['port_id']!r}"
            )
        if item["port_id"] not in interface["emits"]:
            raise ContractValidationError(
                f"named_outputs.port_id must be exposed by public_interface.emits: "
                f"{item['port_id']!r}"
            )

    require_unique([route["route_id"] for route in node["routes"]], "routes.route_id")
    require_unique([gate["gate_id"] for gate in node["gates"]], "gates.gate_id")

    identity = node["identity"]
    key_definitions = identity["key_definitions"]
    identity_keys = [definition["key"] for definition in key_definitions]
    require_unique(identity_keys, "identity.key_definitions.key")
    key_by_name = {definition["key"]: definition for definition in key_definitions}
    for port in ports:
        for key in port["identity_keys"]:
            definition = key_by_name.get(key)
            if definition is None:
                raise ContractValidationError(
                    f"port {port['port_id']!r} references undefined identity key {key!r}"
                )
            if not definition["required"]:
                raise ContractValidationError(
                    f"port {port['port_id']!r} uses identity key {key!r} "
                    "that is not marked required"
                )

    provenance = node["provenance"]
    if not REQUIRED_RUN_FIELDS.issubset(set(provenance["required_run_fields"])):
        missing = sorted(REQUIRED_RUN_FIELDS - set(provenance["required_run_fields"]))
        raise ContractValidationError(
            f"provenance.required_run_fields is missing {missing!r}"
        )
    run_schema_path = resolve_repository_path(
        provenance["run_record_schema"],
        repo_root,
        "provenance.run_record_schema",
    )
    if not run_schema_path.is_file():
        raise ContractValidationError(
            f"provenance.run_record_schema does not exist: {provenance['run_record_schema']!r}"
        )
    for index, source_ref in enumerate(provenance["source_refs"]):
        if source_ref.startswith(("http://", "https://")):
            continue
        source_path = resolve_repository_path(
            source_ref,
            repo_root,
            f"provenance.source_refs[{index}]",
        )
        if not source_path.exists():
            raise ContractValidationError(
                f"provenance.source_refs[{index}] does not exist: {source_ref!r}"
            )
    if "recorded in" in json.dumps(provenance, ensure_ascii=False).lower():
        raise ContractValidationError(
            "static provenance must not use a run-time placeholder value"
        )
    for index, evidence in enumerate(node["evidence"]):
        evidence_ref = evidence["ref"]
        if evidence_ref.startswith(("http://", "https://")):
            continue
        evidence_path = resolve_repository_path(
            evidence_ref,
            repo_root,
            f"evidence[{index}].ref",
        )
        if not evidence_path.exists():
            raise ContractValidationError(
                f"evidence[{index}].ref does not exist: {evidence_ref!r}"
            )

    module_refs = node.get("module_refs", [])
    if node["kind"] != "facade":
        if module_refs:
            raise ContractValidationError(
                "module_refs are only valid on a facade contract"
            )
        return
    if not module_refs:
        raise ContractValidationError(
            "a facade contract must declare at least one atomic module reference"
        )

    module_ids: list[str] = []
    exposed_facade_ports: list[str] = []
    for reference in module_refs:
        module_id = reference["component_id"]
        module_ids.append(module_id)
        module_path = resolve_repository_path(
            reference["contract_path"],
            repo_root,
            f"module_refs[{module_id}].contract_path",
        )
        if not module_path.is_file():
            raise ContractValidationError(
                f"module contract does not exist: {reference['contract_path']!r}"
            )
        module = load_json_object(module_path)
        if module.get("component_id") != module_id:
            raise ContractValidationError(
                f"module reference {module_id!r} does not match its contract component_id"
            )
        if module.get("schema_version") != reference["schema_version"]:
            raise ContractValidationError(
                f"module reference {module_id!r} has a schema-version mismatch"
            )
        if module.get("kind") != "module":
            raise ContractValidationError(
                f"facade reference {module_id!r} must point to kind=module"
            )
        validate_node_data(module, module_path, repo_root, node_schema, seen)
        module_ports = {port["port_id"]: port for port in module["ports"]}
        binding_pairs = [
            (binding["module_port_id"], binding["facade_port_id"])
            for binding in reference["port_bindings"]
        ]
        require_unique(binding_pairs, f"module_refs[{module_id}].port_bindings")
        require_unique(
            [pair[0] for pair in binding_pairs],
            f"module_refs[{module_id}].module_port_bindings",
        )
        require_unique(
            [pair[1] for pair in binding_pairs],
            f"module_refs[{module_id}].facade_port_bindings",
        )
        for module_port_id, facade_port_id in binding_pairs:
            module_port = module_ports.get(module_port_id)
            facade_port = port_by_id.get(facade_port_id)
            if module_port is None:
                raise ContractValidationError(
                    f"module {module_id!r} binding references unknown port "
                    f"{module_port_id!r}"
                )
            if facade_port is None:
                raise ContractValidationError(
                    f"facade binding references unknown port {facade_port_id!r}"
                )
            if facade_port_id not in interface["takes"] + interface["emits"]:
                raise ContractValidationError(
                    f"facade binding must expose facade port {facade_port_id!r}"
                )
            for field in ("direction", "channel_semantics", "shape", "cardinality"):
                if module_port[field] != facade_port[field]:
                    raise ContractValidationError(
                        f"binding {module_id}:{module_port_id} -> {facade_port_id} "
                        f"has incompatible {field}"
                    )
            exposed_facade_ports.append(facade_port_id)

    require_unique(module_ids, "module_refs.component_id")
    require_unique(exposed_facade_ports, "facade exposed port bindings")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_input_manifest(
    manifest: dict[str, Any],
    manifest_path: Path,
    repo_root: Path,
    schema_path: Path,
) -> None:
    errors = schema_errors(manifest, schema_path)
    if errors:
        raise ContractValidationError("; ".join(errors))
    input_root = resolve_repository_path(
        manifest["input_root"],
        repo_root,
        "input-manifest.input_root",
    )
    if not input_root.is_dir():
        raise ContractValidationError(
            f"input manifest input_root is not a directory: {manifest['input_root']!r}"
        )
    require_unique(
        [record["path"] for record in manifest["files"]],
        "input-manifest.files.path",
    )
    records: list[dict[str, Any]] = []
    for index, record in enumerate(manifest["files"]):
        path = resolve_repository_path(
            record["path"],
            repo_root,
            f"input-manifest.files[{index}].path",
        )
        try:
            relative_to_input = path.relative_to(input_root).as_posix()
        except ValueError as exc:
            raise ContractValidationError(
                f"input manifest file is outside input_root: {record['path']!r}"
            ) from exc
        if not path.is_file():
            raise ContractValidationError(f"input manifest file is missing: {record['path']!r}")
        if path.stat().st_size != record["size"]:
            raise ContractValidationError(f"input manifest size mismatch: {record['path']!r}")
        if file_sha256(path) != ensure_sha256(record["sha256"], f"input file {record['path']}"):
            raise ContractValidationError(f"input manifest hash mismatch: {record['path']!r}")
        records.append(
            {
                "path": relative_to_input,
                "size": record["size"],
                "sha256": record["sha256"],
            }
        )
    calculated_aggregate = hashlib.sha256(
        json.dumps(records, sort_keys=True).encode("utf-8")
    ).hexdigest()
    if manifest["sha256"] != calculated_aggregate:
        raise ContractValidationError("input manifest aggregate hash mismatch")
    if manifest_path.resolve().parent.name != manifest["run_id"]:
        raise ContractValidationError("input manifest parent does not match run_id")


def validate_artifact_manifest(
    manifest: dict[str, Any],
    manifest_path: Path,
    repo_root: Path,
    run_root: Path,
    schema_path: Path,
) -> None:
    errors = schema_errors(manifest, schema_path)
    if errors:
        raise ContractValidationError("; ".join(errors))
    declared_run_root = resolve_repository_path(
        manifest["run_root"],
        repo_root,
        "artifact-manifest.run_root",
    )
    if declared_run_root != run_root.resolve():
        raise ContractValidationError("artifact manifest run_root does not match status run")
    require_unique(
        [record["path"] for record in manifest["artifacts"]],
        "artifact-manifest.artifacts.path",
    )
    for index, record in enumerate(manifest["artifacts"]):
        path = resolve_repository_path(
            record["path"],
            repo_root,
            f"artifact-manifest.artifacts[{index}].path",
        )
        try:
            path.relative_to(run_root.resolve())
        except ValueError as exc:
            raise ContractValidationError(
                f"artifact is outside the declared run root: {record['path']!r}"
            ) from exc
        if record["exists"] is not True or not path.is_file():
            raise ContractValidationError(f"artifact is not present: {record['path']!r}")
        if path.stat().st_size != record["size"]:
            raise ContractValidationError(f"artifact size mismatch: {record['path']!r}")
        if file_sha256(path) != ensure_sha256(
            record["sha256"],
            f"artifact {record['path']}",
        ):
            raise ContractValidationError(f"artifact hash mismatch: {record['path']!r}")
    if manifest_path.resolve().parent.name != manifest["run_id"]:
        raise ContractValidationError("artifact manifest parent does not match run_id")


def validate_run_status(
    status_path: Path,
    repo_root: Path,
    run_schema: Path,
    node_schema: Path,
    input_schema: Path,
    artifact_schema: Path,
) -> None:
    status = load_json_object(status_path)
    errors = schema_errors(status, run_schema)
    if errors:
        raise ContractValidationError("; ".join(errors))
    run_root = status_path.resolve().parent
    contract_path = resolve_repository_path(
        status["contract_ref"],
        repo_root,
        "run status contract_ref",
    )
    if not contract_path.is_file():
        raise ContractValidationError("run status contract_ref does not exist")
    node = load_json_object(contract_path)
    validate_node_data(node, contract_path, repo_root, node_schema)
    if node.get("component_id") != status["component_id"]:
        raise ContractValidationError("run status component_id does not match node contract")
    if node.get("schema_version") != status["contract_schema_version"]:
        raise ContractValidationError("run status contract schema version does not match node")
    if "status" in node:
        raise ContractValidationError("run status must not be copied into the node contract")
    verifier_path = resolve_repository_path(
        status["verifier_ref"],
        repo_root,
        "run status verifier_ref",
    )
    if not verifier_path.is_file():
        raise ContractValidationError("run status verifier_ref does not exist")
    source_verdict = resolve_run_path(
        status["source_verdict"],
        run_root,
        "run status source_verdict",
    )
    review_record = resolve_run_path(
        status["review_record"],
        run_root,
        "run status review_record",
    )
    if not source_verdict.is_file() or not review_record.is_file():
        raise ContractValidationError("run status verdict/review references are not readable")

    provenance = status["provenance"]
    input_ref = provenance["input_manifest"]
    artifact_ref = provenance["artifact_manifest"]
    input_manifest_path = resolve_run_path(
        input_ref["path"],
        run_root,
        "run provenance input_manifest.path",
    )
    artifact_manifest_path = resolve_run_path(
        artifact_ref["path"],
        run_root,
        "run provenance artifact_manifest.path",
    )
    if not input_manifest_path.is_file() or not artifact_manifest_path.is_file():
        raise ContractValidationError(
            "run provenance manifest paths must point to readable files"
        )
    if file_sha256(input_manifest_path) != ensure_sha256(
        input_ref["sha256"],
        "run provenance input_manifest.sha256",
    ):
        raise ContractValidationError("run provenance input manifest hash mismatch")
    if file_sha256(artifact_manifest_path) != ensure_sha256(
        artifact_ref["sha256"],
        "run provenance artifact_manifest.sha256",
    ):
        raise ContractValidationError("run provenance artifact manifest hash mismatch")

    input_manifest = load_json_object(input_manifest_path)
    artifact_manifest = load_json_object(artifact_manifest_path)
    if input_manifest.get("run_id") != status["run_id"]:
        raise ContractValidationError("input manifest run_id does not match run status")
    if artifact_manifest.get("run_id") != status["run_id"]:
        raise ContractValidationError("artifact manifest run_id does not match run status")
    validate_input_manifest(input_manifest, input_manifest_path, repo_root, input_schema)
    validate_artifact_manifest(
        artifact_manifest,
        artifact_manifest_path,
        repo_root,
        run_root,
        artifact_schema,
    )
    for index, argument in enumerate(provenance["command"]):
        if WINDOWS_ABSOLUTE.match(argument) or argument.startswith(("/", "\\")):
            raise ContractValidationError(
                f"run provenance command[{index}] must not contain an absolute path"
            )
    executable_path = provenance["executable"].get("path")
    if executable_path is not None:
        executable_file = resolve_repository_path(
            executable_path,
            repo_root,
            "run provenance executable.path",
        )
        if not executable_file.is_file():
            raise ContractValidationError(
                f"run provenance executable.path does not exist: {executable_path!r}"
            )


def expect_failure(action: Callable[[], None], label: str) -> None:
    try:
        action()
    except ContractValidationError:
        return
    raise ContractValidationError(f"self-test expected failure was not detected: {label}")


def run_self_test(
    node_path: Path,
    repo_root: Path,
    node_schema: Path,
) -> None:
    node = load_json_object(node_path)

    invalid_port = copy.deepcopy(node)
    invalid_port["public_interface"]["takes"] = ["unknown_port"]
    expect_failure(
        lambda: validate_node_data(
            invalid_port,
            node_path,
            repo_root,
            node_schema,
        ),
        "unknown public port",
    )

    invalid_direction = copy.deepcopy(node)
    invalid_direction["public_interface"]["emits"] = ["qc_input"]
    expect_failure(
        lambda: validate_node_data(
            invalid_direction,
            node_path,
            repo_root,
            node_schema,
        ),
        "public input exposed as output",
    )

    invalid_duplicate_port = copy.deepcopy(node)
    invalid_duplicate_port["ports"].append(copy.deepcopy(node["ports"][0]))
    expect_failure(
        lambda: validate_node_data(
            invalid_duplicate_port,
            node_path,
            repo_root,
            node_schema,
        ),
        "duplicate port id",
    )

    invalid_runtime_placeholder = copy.deepcopy(node)
    invalid_runtime_placeholder["provenance"]["input_hashes"] = ["recorded in run"]
    expect_failure(
        lambda: validate_node_data(
            invalid_runtime_placeholder,
            node_path,
            repo_root,
            node_schema,
        ),
        "runtime provenance placeholder",
    )

    invalid_status = copy.deepcopy(node)
    invalid_status["status"] = {
        "execution": "passed",
        "scientific": "not-verified",
        "release": "pending",
    }
    expect_failure(
        lambda: validate_node_data(
            invalid_status,
            node_path,
            repo_root,
            node_schema,
        ),
        "run status copied into static node",
    )

    invalid_output = copy.deepcopy(node)
    invalid_output["named_outputs"][0]["port_id"] = "qc_input"
    expect_failure(
        lambda: validate_node_data(
            invalid_output,
            node_path,
            repo_root,
            node_schema,
        ),
        "named output points to input",
    )

    invalid_identity = copy.deepcopy(node)
    invalid_identity["ports"][0]["identity_keys"] = ["undefined_key"]
    expect_failure(
        lambda: validate_node_data(
            invalid_identity,
            node_path,
            repo_root,
            node_schema,
        ),
        "undefined identity key",
    )

    with TemporaryDirectory(prefix=".research-core-contract-", dir=repo_root) as directory:
        temp_root = Path(directory)
        module_path = temp_root / "atomic-demo.node.contract.json"
        module = copy.deepcopy(node)
        module["component_id"] = "atomic-demo"
        module["kind"] = "module"
        module_path.write_text(
            json.dumps(module, indent=2) + "\n",
            encoding="utf-8",
        )
        facade = copy.deepcopy(node)
        facade["component_id"] = "demo-facade"
        facade["kind"] = "facade"
        facade["module_refs"] = [
            {
                "component_id": "atomic-demo",
                "contract_path": module_path.relative_to(repo_root).as_posix(),
                "schema_version": module["schema_version"],
                "port_bindings": [
                    {
                        "module_port_id": "qc_input",
                        "facade_port_id": "qc_input",
                    }
                ],
            }
        ]
        facade_path = temp_root / "facade.node.contract.json"
        facade_path.write_text(
            json.dumps(facade, indent=2) + "\n",
            encoding="utf-8",
        )
        invalid_facade = copy.deepcopy(facade)
        invalid_facade["module_refs"][0]["port_bindings"][0]["module_port_id"] = "missing"
        expect_failure(
            lambda: validate_node_data(
                invalid_facade,
                facade_path,
                repo_root,
                node_schema,
            ),
            "facade binding references unknown module port",
        )
        validate_node_data(facade, facade_path, repo_root, node_schema)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--node", type=Path, required=True)
    parser.add_argument("--run-status", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    node_path = args.node.resolve()
    contracts_root = node_path.parent.parent
    node_schema = contracts_root / "node-contract.schema.json"
    run_schema = contracts_root / "run-status.schema.json"
    input_schema = contracts_root / "input-manifest.schema.json"
    artifact_schema = contracts_root / "artifact-manifest.schema.json"

    try:
        node = load_json_object(node_path)
        validate_node_data(node, node_path, repo_root, node_schema)
        print(f"PASS node cross-field contract: {node_path}")
        if args.run_status is not None:
            validate_run_status(
                args.run_status.resolve(),
                repo_root,
                run_schema,
                node_schema,
                input_schema,
                artifact_schema,
            )
            print(f"PASS run status and evidence manifests: {args.run_status.resolve()}")
        if args.self_test:
            run_self_test(node_path, repo_root, node_schema)
            print("PASS cross-field regression self-tests")
    except ContractValidationError as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
