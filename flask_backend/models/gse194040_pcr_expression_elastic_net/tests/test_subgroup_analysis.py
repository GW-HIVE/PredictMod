from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "analyze_gse194040_subgroups.py"
SPEC = importlib.util.spec_from_file_location("subgroup_analysis", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load subgroup analysis module from {SCRIPT}")
SUBGROUP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SUBGROUP)


class SubgroupAnalysisTests(unittest.TestCase):
    def test_binary_metrics_known_values(self) -> None:
        observed = np.array([0, 0, 1, 1])
        classes = np.array([0, 1, 1, 1])
        scores = np.array([0.1, 0.4, 0.8, 0.9])

        metrics = SUBGROUP.binary_metrics(observed, classes, scores)

        self.assertAlmostEqual(metrics["roc_auc"], 1.0)
        self.assertAlmostEqual(metrics["sensitivity"], 1.0)
        self.assertAlmostEqual(metrics["specificity"], 0.5)

    def test_bootstrap_intervals_are_reproducible(self) -> None:
        observed = np.array([0, 0, 0, 0, 1, 1, 1, 1])
        classes = np.array([0, 0, 1, 0, 1, 1, 0, 1])
        scores = np.array([0.05, 0.15, 0.60, 0.30, 0.90, 0.75, 0.35, 0.80])

        first = SUBGROUP.bootstrap_metric_intervals(
            observed, classes, scores, iterations=250, random_seed=123
        )
        second = SUBGROUP.bootstrap_metric_intervals(
            observed, classes, scores, iterations=250, random_seed=123
        )

        self.assertEqual(first, second)
        for metric in ("roc_auc", "sensitivity", "specificity"):
            self.assertLessEqual(
                first[f"{metric}_ci_lower_95"], first[f"{metric}_ci_upper_95"]
            )
            self.assertGreater(first[f"{metric}_valid_replicates"], 0)

    def test_treatment_threshold_and_exploratory_labels(self) -> None:
        rows = []
        for arm, n, positives in (
            ("large", 30, 10),
            ("small", 12, 4),
            ("too_small", 9, 4),
        ):
            for index in range(n):
                observed = int(index < positives)
                rows.append(
                    {
                        "sample_id": f"{arm}_{index}",
                        "observed_pCR": observed,
                        "predicted_pCR_class": observed,
                        "predicted_pCR_score": 0.8 if observed else 0.2,
                        "HR": index % 2,
                        "HER2": (index // 2) % 2,
                        "MP": index % 2,
                        "treatment_arm": arm,
                    }
                )
        locked = pd.DataFrame(rows)

        results = SUBGROUP.build_subgroup_results(
            locked,
            bootstrap_iterations=50,
            random_seed=456,
            minimum_treatment_n=10,
            minimum_outcome_count=3,
            exploratory_n=30,
        )
        treatment = results.loc[results["subgroup_family"].eq("treatment_arm")]
        statuses = dict(zip(treatment["subgroup"], treatment["analysis_status"]))

        self.assertEqual(statuses["large"], "reported")
        self.assertEqual(statuses["small"], "exploratory_small_sample")
        self.assertEqual(statuses["too_small"], "not_estimated_insufficient_sample")
        omitted = treatment.loc[treatment["subgroup"].eq("too_small")].iloc[0]
        self.assertTrue(np.isnan(omitted["roc_auc"]))

    def test_group_seed_is_stable_and_group_specific(self) -> None:
        first = SUBGROUP.derived_group_seed(20260719, "MP_status", "MP=0")
        second = SUBGROUP.derived_group_seed(20260719, "MP_status", "MP=0")
        different = SUBGROUP.derived_group_seed(20260719, "MP_status", "MP=1")

        self.assertEqual(first, second)
        self.assertNotEqual(first, different)


if __name__ == "__main__":
    unittest.main()
