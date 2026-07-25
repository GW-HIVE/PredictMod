from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import unittest
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRAIN_SCRIPT = PROJECT_ROOT / "scripts" / "train_gse194040_models.py"
SPEC = importlib.util.spec_from_file_location("gse194040_training", TRAIN_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load training module from {TRAIN_SCRIPT}")
TRAINING = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRAINING)


class ReproducibilityTests(unittest.TestCase):
    def test_frozen_model_matches_declared_metadata(self) -> None:
        model_path = PROJECT_ROOT / "models" / "gse194040_best_model.joblib"
        metadata = json.loads(
            (
                PROJECT_ROOT / "models" / "gse194040_best_model_metadata.json"
            ).read_text(encoding="utf-8")
        )
        declared = metadata["frozen_model"]
        model = joblib.load(model_path)

        self.assertEqual(list(model.named_steps), declared["pipeline_steps"])
        self.assertEqual(
            f"{type(model).__module__}.{type(model).__name__}",
            declared["sklearn_object_type"],
        )
        self.assertEqual(int(model.n_features_in_), declared["input_feature_count"])
        self.assertEqual(
            hashlib.sha256(model_path.read_bytes()).hexdigest(),
            declared["sha256"],
        )

    def test_requirements_are_exactly_pinned(self) -> None:
        for filename in ["requirements.txt", "requirements-lock.txt"]:
            lines = (PROJECT_ROOT / filename).read_text(encoding="utf-8").splitlines()
            packages = [line for line in lines if line and not line.startswith("#")]
            self.assertTrue(packages)
            self.assertTrue(all(re.fullmatch(r"[A-Za-z0-9_.-]+==[^=<>~!]+", line) for line in packages))

    def test_direct_requirements_match_lockfile(self) -> None:
        def pinned_versions(filename: str) -> dict[str, str]:
            lines = (PROJECT_ROOT / filename).read_text(encoding="utf-8").splitlines()
            return {
                name.lower(): version
                for line in lines
                if line and not line.startswith("#")
                for name, version in [line.split("==", maxsplit=1)]
            }

        direct = pinned_versions("requirements.txt")
        locked = pinned_versions("requirements-lock.txt")
        self.assertEqual(direct["referencing"], "0.37.0")
        for name, version in direct.items():
            self.assertIn(name, locked)
            self.assertEqual(version, locked[name], name)

    def test_dependency_provenance_distinguishes_environment_roles(self) -> None:
        manifest = json.loads(
            (
                PROJECT_ROOT
                / "results"
                / "reproducibility"
                / "gse194040_reproducibility_manifest_v1_20260719.json"
            ).read_text(encoding="utf-8")
        )
        provenance = manifest["dependency_provenance"]
        historical = provenance["existing_processed_dataset"]
        current = provenance["current_prediction_testing"]
        self.assertEqual(historical["pandas"], "3.0.1")
        self.assertEqual(historical["numpy"], "2.3.5")
        self.assertFalse(historical["regenerated_under_current_lock"])
        self.assertFalse(historical["included_in_submission"])
        self.assertFalse(
            (
                PROJECT_ROOT
                / "data_processed"
                / "gse194040_ml_ready_pcr_expression.csv"
            ).exists()
        )
        self.assertFalse((PROJECT_ROOT / "GSE194040").exists())
        self.assertEqual(current["pandas"], "2.2.2")
        self.assertEqual(current["numpy"], "2.5.1")
        self.assertEqual(current["referencing"], "0.37.0")
        self.assertFalse(current["historical_dataset_producer"])

    def test_scripts_do_not_inject_untracked_packages_or_suppress_warnings(self) -> None:
        for script in (PROJECT_ROOT / "scripts").glob("*.py"):
            source = script.read_text(encoding="utf-8")
            self.assertNotIn('PROJECT_ROOT / "python_packages"', source, script.name)
            self.assertNotIn("filterwarnings", source, script.name)
            self.assertNotIn("n_jobs=-1", source, script.name)

    def test_cli_parallelism_validation_and_random_forest_policy(self) -> None:
        self.assertEqual(TRAINING.validate_n_jobs(1), 1)
        self.assertEqual(TRAINING.validate_n_jobs(-1), -1)
        for value in [0, -2]:
            with self.assertRaises(ValueError):
                TRAINING.validate_n_jobs(value)
        specs = TRAINING.build_model_specs(random_state=42, max_iter=25)
        forest = specs["random_forest"][0].named_steps["classifier"]
        self.assertEqual(forest.n_jobs, 1)

    def test_fitted_convergence_status_is_recorded(self) -> None:
        estimator = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("classifier", LogisticRegression(max_iter=500, random_state=42)),
            ]
        )
        X = np.array([[-2.0], [-1.0], [-0.5], [0.5], [1.0], [2.0]])
        y = np.array([0, 0, 0, 1, 1, 1])
        estimator.fit(X, y)
        records = TRAINING.model_convergence_records("test", estimator)
        self.assertEqual(records[0]["status"], "converged_before_max_iter")
        self.assertLess(records[0]["observed_max_iter"], records[0]["configured_max_iter"])


class BioComputeObjectTests(unittest.TestCase):
    def test_bco_is_schema_valid(self) -> None:
        validator_path = PROJECT_ROOT / "scripts" / "validate_gse194040_bco.py"
        spec = importlib.util.spec_from_file_location("bco_validator", validator_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load BCO validator from {validator_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        errors = module.validate_bco(
            PROJECT_ROOT / "bco" / "gse194040_pcr_pipeline_bco_v1.json",
            PROJECT_ROOT / "schemas" / "ieee-2791-v1.4",
        )
        self.assertEqual(errors, [])

    def test_bco_local_file_checksums_match(self) -> None:
        bco = json.loads(
            (PROJECT_ROOT / "bco" / "gse194040_pcr_pipeline_bco_v1.json").read_text(encoding="utf-8")
        )
        github_prefix = (
            "https://github.com/GW-HIVE/PredictMod/blob/main/"
            "flask_backend/models/gse194040_pcr_expression_elastic_net/"
        )

        def walk(value: object) -> None:
            if isinstance(value, dict):
                if "uri" in value and "sha1_checksum" in value and isinstance(value["uri"], str):
                    if value["uri"].startswith(github_prefix):
                        path = PROJECT_ROOT / value["uri"][len(github_prefix):]
                        self.assertTrue(path.is_file(), str(path))
                        actual = hashlib.sha1(path.read_bytes()).hexdigest()
                        self.assertEqual(actual, value["sha1_checksum"], str(path))
                for nested in value.values():
                    walk(nested)
            elif isinstance(value, list):
                for nested in value:
                    walk(nested)

        walk(bco)
        serialized = json.dumps(bco)
        self.assertNotIn("file:///VolunteershipGWU/", serialized)
        excluded = {
            row["path"]: row
            for row in json.loads(
                (
                    PROJECT_ROOT
                    / "results"
                    / "reproducibility"
                    / "gse194040_reproducibility_manifest_v1_20260719.json"
                ).read_text(encoding="utf-8")
            )["excluded_recreatable_artifacts"]
        }
        self.assertEqual(
            excluded[
                "data_processed/gse194040_ml_ready_pcr_expression.csv"
            ]["expected_sha256"],
            "4f00b3fdf4006129ed31835763dfc906245da1c6d383546a7fe354d5069de78a",
        )

    def test_bco_claims_are_explicitly_nonclinical(self) -> None:
        text = (PROJECT_ROOT / "bco" / "gse194040_pcr_pipeline_bco_v1.json").read_text(encoding="utf-8")
        self.assertIn("exploratory pooled", text)
        self.assertIn("not a treatment-selection model", text)
        self.assertIn("does not produce calibrated clinical probabilities", text)


if __name__ == "__main__":
    unittest.main()
