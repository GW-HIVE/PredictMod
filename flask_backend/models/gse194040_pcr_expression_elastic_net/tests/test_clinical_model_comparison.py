from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "train_evaluate_gse194040_clinical_models.py"
SPEC = importlib.util.spec_from_file_location("clinical_model_comparison", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load comparison module from {SCRIPT}")
COMPARISON = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPARISON)


class ClinicalModelComparisonTests(unittest.TestCase):
    def test_model_specs_keep_preprocessing_inside_pipelines(self) -> None:
        specs = COMPARISON.build_model_specs(
            ["expr_A", "expr_B"], random_seed=42, max_iter=100
        )

        self.assertEqual(
            set(specs), {"clinical_baseline", "clinical_plus_expression"}
        )
        for pipeline, parameter_grid in specs.values():
            self.assertIn("preprocessor", pipeline.named_steps)
            self.assertIn("classifier", pipeline.named_steps)
            self.assertTrue(parameter_grid)
        combined = specs["clinical_plus_expression"][0]
        transformers = dict(
            (name, columns)
            for name, transformer, columns in combined.named_steps[
                "preprocessor"
            ].transformers
        )
        self.assertEqual(transformers["expression"], ["expr_A", "expr_B"])
        self.assertEqual(transformers["binary"], ["HR", "HER2", "MP"])
        self.assertEqual(transformers["treatment"], ["treatment_arm"])

    def test_calibration_diagnostics_for_calibrated_groups(self) -> None:
        scores = np.concatenate([np.full(100, 0.2), np.full(100, 0.8)])
        observed = np.concatenate(
            [
                np.ones(20, dtype=int),
                np.zeros(80, dtype=int),
                np.ones(80, dtype=int),
                np.zeros(20, dtype=int),
            ]
        )

        metrics = COMPARISON.evaluate_scores(observed, scores)

        self.assertAlmostEqual(metrics["calibration_intercept"], 0.0, places=5)
        self.assertAlmostEqual(metrics["calibration_slope"], 1.0, places=5)
        self.assertAlmostEqual(metrics["brier_score"], 0.16, places=12)

    def test_bootstrap_confidence_intervals_are_reproducible(self) -> None:
        observed = np.array([0, 0, 0, 0, 1, 1, 1, 1])
        scores = np.array([0.05, 0.15, 0.60, 0.30, 0.90, 0.75, 0.35, 0.80])
        point = COMPARISON.evaluate_scores(observed, scores)

        first = COMPARISON.bootstrap_model_confidence_intervals(
            observed, scores, point, iterations=100, random_seed=1234
        )
        second = COMPARISON.bootstrap_model_confidence_intervals(
            observed, scores, point, iterations=100, random_seed=1234
        )

        self.assertTrue(first.equals(second))
        self.assertEqual(list(first["metric"]), COMPARISON.BOOTSTRAP_METRICS)
        self.assertTrue((first["ci_lower_95"] <= first["ci_upper_95"]).all())

    def test_nonempty_output_directory_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            marker = output_dir / "preserve.txt"
            marker.write_text("preserve", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                COMPARISON.ensure_new_output_directory(output_dir)

            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")


if __name__ == "__main__":
    unittest.main()
