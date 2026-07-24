"""Validate the GSE194040 BCO against the vendored IEEE 2791 v1.4 schemas."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry, Resource


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BCO = PROJECT_ROOT / "bco" / "gse194040_pcr_pipeline_bco_v1.json"
DEFAULT_SCHEMA_DIR = PROJECT_ROOT / "schemas" / "ieee-2791-v1.4"
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "results"
    / "validation"
    / "gse194040_bco_validation_v1_20260719.json"
)


def portable_package_path(path: Path) -> str:
    """Return a POSIX path relative to the package root."""
    try:
        relative = os.path.relpath(path.resolve(), PROJECT_ROOT.resolve())
    except ValueError:
        return path.name
    return Path(relative).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_registry(schema_dir: Path) -> Registry:
    registry = Registry()
    for schema_path in sorted(schema_dir.glob("*.json")):
        resource = Resource.from_contents(
            json.loads(schema_path.read_text(encoding="utf-8"))
        )
        resource_id = resource.id()
        if resource_id is None:
            raise ValueError(f"Schema has no $id: {schema_path}")
        registry = registry.with_resource(resource_id, resource)
    return registry


def validate_bco(bco_path: Path, schema_dir: Path) -> list[dict[str, str]]:
    schema_path = schema_dir / "2791object.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    instance = json.loads(bco_path.read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)
    validator = Draft7Validator(
        schema,
        registry=build_registry(schema_dir),
        format_checker=FormatChecker(),
    )
    return [
        {
            "instance_path": "/".join(map(str, error.absolute_path)),
            "schema_path": "/".join(map(str, error.absolute_schema_path)),
            "message": error.message,
        }
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bco", type=Path, default=DEFAULT_BCO)
    parser.add_argument("--schema-dir", type=Path, default=DEFAULT_SCHEMA_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    errors = validate_bco(args.bco, args.schema_dir)
    schema_path = args.schema_dir / "2791object.json"
    result = {
        "validation_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "valid" if not errors else "invalid",
        "validator": f"jsonschema {importlib.metadata.version('jsonschema')}",
        "python": sys.version,
        "operating_system": platform.platform(),
        "bco_path": portable_package_path(args.bco),
        "bco_sha256": sha256(args.bco),
        "schema_path": portable_package_path(schema_path),
        "schema_id": "https://w3id.org/ieee/ieee-2791-schema/2791object.json",
        "schema_sha256": sha256(schema_path),
        "schema_version": "IEEE 2791 v1.4 JSON Schema (Draft 7)",
        "error_count": len(errors),
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
