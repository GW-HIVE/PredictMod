"""Capture the installed environment, canonical hashes, and model convergence status."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "results"
    / "reproducibility"
    / "gse194040_reproducibility_manifest_v1_20260719.json"
)
CANONICAL_HASHES = {
    "results/tables/gse194040_train_test_split.csv": "9fe0dcc93812713add7c993516061a52d755038879171cf96ce5d5ca87c50906",
    "models/gse194040_best_model.joblib": "e3bbccac97c4495dbb8e8c66a8f35921ca6ff20cbb9e0b0671aaf0a00504f9d4",
    "models/gse194040_best_model_metadata.json": "4b1e8633bc76d254bd6c9c541a2545bdf7ab08ed8df9df15b71297e605c11781",
    "results/tables/gse194040_cv_model_comparison.csv": "b2ed30e6a01806793814da5a37b3ec2569c20431f1ad9a32c7ca45f21ce6cc14",
    "results/tables/gse194040_final_test_metrics.csv": "e37a940e836b9f69575bc6913c8be8926bfc03eba8fafda83092ad4ec8b7a82c",
    "results/figures/gse194040_final_roc_curve.png": "96a79a1c215b63e7486ac20951cdc42c16f09b8eebb67bc78f08d494e25be44f",
    "results/figures/gse194040_final_confusion_matrix.png": "759d3df850f4d3a245cae1b571d363b2928f8b4e3dd11d2eb57bb779d319778f",
}
EXCLUDED_RECREATABLE_ARTIFACTS = [
    {
        "path": "data_processed/gse194040_ml_ready_pcr_expression.csv",
        "included_in_submission": False,
        "expected_sha1": "714aacadbdbfecbc882662ad36f578afc398201c",
        "expected_sha256": "4f00b3fdf4006129ed31835763dfc906245da1c6d383546a7fe354d5069de78a",
        "rows": 987,
        "columns": 19143,
        "expression_features": 19134,
        "recreated_by": "scripts/preprocess_gse194040.py",
    },
    {
        "path": "GSE194040/GSE194040_ISPY2ResID_AgilentGeneExp_990_FrshFrzn_meanCol_geneLevel_n988.txt.gz",
        "included_in_submission": False,
        "expected_sha1": "f84873f85a5ba8ca4a357a414e0b847532ed74d6",
        "download_url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194040/suppl/GSE194040_ISPY2ResID_AgilentGeneExp_990_FrshFrzn_meanCol_geneLevel_n988.txt.gz",
    },
    {
        "path": "GSE194040/GSE194040-GPL20078_series_matrix.txt.gz",
        "included_in_submission": False,
        "expected_sha1": "6fdf48178aeb1a1394ae5718b1e13d026987ed86",
        "download_url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194040/matrix/GSE194040-GPL20078_series_matrix.txt.gz",
    },
    {
        "path": "GSE194040/GSE194040-GPL30493_series_matrix.txt.gz",
        "included_in_submission": False,
        "expected_sha1": "27a7ad81e2e7ffa42b9f9382928f43ff39312069",
        "download_url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194040/matrix/GSE194040-GPL30493_series_matrix.txt.gz",
    },
]
MAJOR_PACKAGES = [
    "numpy",
    "pandas",
    "scipy",
    "scikit-learn",
    "joblib",
    "matplotlib",
    "pytest",
    "jsonschema",
    "referencing",
]


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


def pinned_versions(path: Path) -> dict[str, str]:
    versions = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            name, version = stripped.split("==", maxsplit=1)
            versions[name.lower()] = version
    return versions


def selected_model_convergence() -> dict[str, object]:
    model_path = PROJECT_ROOT / "models" / "gse194040_best_model.joblib"
    model = joblib.load(model_path)
    classifier = model.named_steps["classifier"]
    iterations = np.asarray(classifier.n_iter_, dtype=int).ravel()
    observed_max = int(iterations.max())
    configured_max = int(classifier.max_iter)
    return {
        "model_path": portable_package_path(model_path),
        "model_sha256": sha256(model_path),
        "classifier_class": type(classifier).__name__,
        "solver": classifier.solver,
        "n_iter": iterations.tolist(),
        "observed_max_iter": observed_max,
        "configured_max_iter": configured_max,
        "status": (
            "converged_before_max_iter"
            if observed_max < configured_max
            else "reached_max_iter_review_original_training_log"
        ),
        "note": "Status is read from the frozen fitted estimator; the model was not refit.",
    }


def additional_model_convergence() -> list[dict[str, object]]:
    directory = (
        PROJECT_ROOT
        / "results"
        / "evaluation"
        / "gse194040_clinical_expression_comparison_v1_20260719"
    )
    records = []
    for model_path in sorted(directory.glob("*.joblib")):
        model = joblib.load(model_path)
        classifier = model.named_steps["classifier"]
        iterations = np.asarray(classifier.n_iter_, dtype=int).ravel()
        observed_max = int(iterations.max())
        configured_max = int(classifier.max_iter)
        records.append(
            {
                "model_path": portable_package_path(model_path),
                "model_sha256": sha256(model_path),
                "classifier_class": type(classifier).__name__,
                "n_iter": iterations.tolist(),
                "observed_max_iter": observed_max,
                "configured_max_iter": configured_max,
                "status": (
                    "converged_before_max_iter"
                    if observed_max < configured_max
                    else "reached_max_iter_review_original_training_log"
                ),
                "note": "Status is read from the frozen fitted estimator; the model was not refit.",
            }
        )
    return records


def main() -> None:
    output = DEFAULT_OUTPUT
    lock_path = PROJECT_ROOT / "requirements-lock.txt"
    locked_versions = pinned_versions(lock_path)
    historical_session_path = PROJECT_ROOT / "logs" / "gse194040_session_info.json"
    historical_session = json.loads(
        historical_session_path.read_text(encoding="utf-8")
    )
    canonical = []
    for relative_path, expected in CANONICAL_HASHES.items():
        actual = sha256(PROJECT_ROOT / relative_path)
        canonical.append(
            {
                "path": relative_path,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "matches": actual == expected,
            }
        )
    manifest = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": {
            "version": platform.python_version(),
            "distribution": platform.python_implementation(),
        },
        "operating_system": {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "logical_cpu_count": os.cpu_count(),
        },
        "major_libraries": {
            name: importlib.metadata.version(name) for name in MAJOR_PACKAGES
        },
        "dependency_provenance": {
            "existing_processed_dataset": {
                "artifact": "data_processed/gse194040_ml_ready_pcr_expression.csv",
                "environment_role": "historical preprocessing environment that produced the intentionally excluded artifact",
                "session_record": portable_package_path(historical_session_path),
                "python": historical_session["python"],
                "platform": historical_session["platform"],
                "pandas": historical_session["pandas"],
                "numpy": historical_session["numpy"],
                "regenerated_under_current_lock": False,
                "included_in_submission": False,
                "recreated_by": "scripts/preprocess_gse194040.py",
            },
            "current_prediction_testing": {
                "environment_role": "supported environment for frozen-model prediction, BCO validation, and automated testing",
                "dependency_source": "requirements-lock.txt",
                "python": platform.python_version(),
                "distribution": platform.python_implementation(),
                "pandas": locked_versions["pandas"],
                "numpy": locked_versions["numpy"],
                "referencing": locked_versions["referencing"],
                "historical_dataset_producer": False,
            },
        },
        "lockfile": {
            "path": "requirements-lock.txt",
            "sha256": sha256(lock_path),
            "all_entries_exactly_pinned": all(
                "==" in line
                for line in lock_path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            ),
        },
        "python_packages_on_sys_path": any(
            Path(entry).name == "python_packages" for entry in sys.path if entry
        ),
        "canonical_artifacts": canonical,
        "all_canonical_hashes_match": all(row["matches"] for row in canonical),
        "excluded_recreatable_artifacts": EXCLUDED_RECREATABLE_ARTIFACTS,
        "selected_model_convergence": selected_model_convergence(),
        "additional_frozen_model_convergence": additional_model_convergence(),
        "cpu_policy": {
            "training_cli_parameter": "--n-jobs",
            "accepted_values": "-1 or a positive integer; zero and values below -1 are rejected",
            "grid_search_owns_parallelism": True,
            "nested_random_forest_jobs": 1,
        },
        "methodology_changed": False,
        "model_refit": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    if not manifest["all_canonical_hashes_match"]:
        raise SystemExit("One or more canonical artifacts changed.")


if __name__ == "__main__":
    main()
