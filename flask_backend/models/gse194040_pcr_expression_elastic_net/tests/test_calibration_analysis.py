from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "analyze_gse194040_calibration.py"
SPEC = importlib.util.spec_from_file_location("calibration_analysis", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load calibration analysis module from {SCRIPT}")
CALIBRATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CALIBRATION)


class CalibrationAnalysisTests(unittest.TestCase):
    def test_brier_score_known_values(self) -> None:
        observed = np.array([0, 0, 1, 1])
        scores = np.array([0.1, 0.4, 0.6, 0.9])

        result = CALIBRATION.brier_score_loss(observed, scores)

        self.assertAlmostEqual(result, 0.085, places=12)

    def test_calibration_intercept_and_slope_for_calibrated_groups(self) -> None:
        low_scores = np.full(100, 0.2)
        high_scores = np.full(100, 0.8)
        scores = np.concatenate([low_scores, high_scores])
        observed = np.concatenate(
            [
                np.ones(20, dtype=int),
                np.zeros(80, dtype=int),
                np.ones(80, dtype=int),
                np.zeros(20, dtype=int),
            ]
        )

        intercept, slope = CALIBRATION.calibration_intercept_slope(observed, scores)

        self.assertAlmostEqual(intercept, 0.0, places=5)
        self.assertAlmostEqual(slope, 1.0, places=5)

    def test_calibration_curve_preserves_all_rows(self) -> None:
        observed = np.array([0, 0, 0, 1, 1, 1])
        scores = np.array([0.05, 0.10, 0.20, 0.70, 0.80, 0.95])

        curve = CALIBRATION.build_calibration_curve_data(observed, scores, n_bins=3)

        self.assertEqual(int(curve["n"].sum()), len(observed))
        self.assertEqual(int(curve["observed_pCR_count"].sum()), int(observed.sum()))
        self.assertEqual(list(curve["bin"]), [1, 2, 3])

    def test_observed_vs_predicted_includes_overall_rates(self) -> None:
        observed = np.array([0, 0, 1, 1])
        scores = np.array([0.1, 0.3, 0.7, 0.9])
        curve = CALIBRATION.build_calibration_curve_data(observed, scores, n_bins=2)

        rates = CALIBRATION.build_observed_vs_predicted_rates(
            observed, scores, curve
        )

        overall = rates.iloc[0]
        self.assertEqual(overall["scope"], "overall_heldout_test")
        self.assertEqual(int(overall["n"]), 4)
        self.assertAlmostEqual(float(overall["observed_pCR_rate"]), 0.5)
        self.assertAlmostEqual(float(overall["mean_predicted_pCR_score"]), 0.5)
        self.assertAlmostEqual(float(overall["observed_minus_predicted"]), 0.0)

    def test_nonempty_output_directory_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            marker = output_dir / "existing-result.txt"
            marker.write_text("preserve", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                CALIBRATION.ensure_new_output_directory(output_dir)

            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")

    def test_point_metrics_include_average_precision_pr_auc(self) -> None:
        observed = np.array([0, 0, 1, 1])
        classes = np.array([0, 1, 1, 1])
        scores = np.array([0.1, 0.4, 0.8, 0.9])

        metrics = CALIBRATION.calculate_point_metrics(observed, classes, scores)

        self.assertAlmostEqual(metrics["roc_auc"], 1.0)
        self.assertAlmostEqual(metrics["pr_auc_average_precision"], 1.0)
        self.assertAlmostEqual(metrics["accuracy"], 0.75)
        self.assertAlmostEqual(metrics["sensitivity"], 1.0)
        self.assertAlmostEqual(metrics["specificity"], 0.5)
        self.assertAlmostEqual(metrics["precision"], 2 / 3)
        self.assertAlmostEqual(metrics["f1"], 0.8)

    def test_bootstrap_confidence_intervals_are_reproducible(self) -> None:
        observed = np.array([0, 0, 0, 0, 1, 1, 1, 1])
        classes = np.array([0, 0, 1, 0, 1, 1, 0, 1])
        scores = np.array([0.05, 0.15, 0.60, 0.30, 0.90, 0.75, 0.35, 0.80])
        point = CALIBRATION.calculate_point_metrics(observed, classes, scores)

        first = CALIBRATION.bootstrap_confidence_intervals(
            observed, classes, scores, point, iterations=250, random_seed=12345
        )
        second = CALIBRATION.bootstrap_confidence_intervals(
            observed, classes, scores, point, iterations=250, random_seed=12345
        )

        self.assertTrue(first.equals(second))
        self.assertEqual(list(first["metric"]), list(CALIBRATION.BOOTSTRAP_METRICS))
        self.assertTrue((first["ci_lower_95"] <= first["ci_upper_95"]).all())
        self.assertTrue((first["valid_replicates"] <= 250).all())
        self.assertTrue((first["valid_replicates"] > 0).all())
        self.assertTrue((first["random_seed"] == 12345).all())

    def test_locked_metric_verification_rejects_mismatch(self) -> None:
        point = {
            "roc_auc": 0.8,
            "accuracy": 0.7,
            "sensitivity": 0.6,
            "specificity": 0.7,
            "precision": 0.5,
            "f1": 0.55,
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_path = Path(tmpdir) / "metrics.csv"
            metrics_path.write_text(
                "roc_auc,accuracy,sensitivity,specificity,precision,f1\n"
                "0.81,0.7,0.6,0.7,0.5,0.55\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "verification failed"):
                CALIBRATION.verify_locked_point_metrics(point, metrics_path)


if __name__ == "__main__":
    unittest.main()
