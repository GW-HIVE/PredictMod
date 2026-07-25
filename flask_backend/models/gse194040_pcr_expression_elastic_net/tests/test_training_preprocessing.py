from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "train_gse194040_models.py"
SPEC = importlib.util.spec_from_file_location("training_pipeline", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load training module from {SCRIPT}")
TRAINING = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRAINING)


class TrainingPreprocessingTests(unittest.TestCase):
    def test_missingness_filter_learns_from_fit_rows_only(self) -> None:
        train = pd.DataFrame(
            {
                "keep": [1.0, 2.0, np.nan, 4.0],
                "drop": [1.0, np.nan, np.nan, np.nan],
            }
        )
        test = pd.DataFrame({"keep": [np.nan], "drop": [5.0]})
        transformer = TRAINING.MissingnessFilter(max_missing_rate=0.25)

        transformer.fit(train)
        transformed = transformer.transform(test)

        self.assertEqual(list(transformer.get_feature_names_out()), ["keep"])
        self.assertEqual(transformed.shape, (1, 1))
        self.assertTrue(np.isnan(transformed.iloc[0, 0]))

    def test_all_model_preprocessing_is_inside_pipeline_in_required_order(self) -> None:
        specs = TRAINING.build_model_specs(
            random_state=42,
            max_iter=100,
            max_missing_rate=0.2,
            variance_threshold=1e-8,
        )

        for model_name, (pipeline, _grid) in specs.items():
            steps = list(pipeline.named_steps)
            self.assertLess(steps.index("missingness"), steps.index("imputer"))
            self.assertLess(steps.index("imputer"), steps.index("variance"))
            if "scaler" in steps:
                self.assertLess(steps.index("variance"), steps.index("scaler"))
            if "select" in steps:
                self.assertLess(steps.index("variance"), steps.index("select"))
            if "pca" in steps:
                self.assertLess(steps.index("scaler"), steps.index("pca"))
            self.assertEqual(steps[-1], "classifier", msg=model_name)

    def test_imputation_then_variance_filter_removes_constant_feature(self) -> None:
        frame = pd.DataFrame(
            {
                "variable": [0.0, 1.0, 2.0, np.nan],
                "constant": [5.0, 5.0, np.nan, 5.0],
            }
        )
        pipeline = TRAINING.Pipeline(
            TRAINING.expression_preprocessing_steps(
                max_missing_rate=0.5, variance_threshold=1e-8, scale=False
            )
        )

        transformed = pipeline.fit_transform(frame)

        self.assertEqual(transformed.shape, (4, 1))
        self.assertEqual(
            list(pipeline.get_feature_names_out(frame.columns)), ["variable"]
        )

    def test_nonempty_corrected_output_directory_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            marker = output_dir / "canonical.txt"
            marker.write_text("preserve", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                TRAINING.ensure_new_output_directory(output_dir)

            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")


if __name__ == "__main__":
    unittest.main()
