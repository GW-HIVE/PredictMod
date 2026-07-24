from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "predict_gse194040_single_patient.py"
EXAMPLE_INPUT = PROJECT_ROOT / "examples" / "gse194040_single_patient_input_example.csv"
CURRENT_EXAMPLE_OUTPUT = (
    PROJECT_ROOT
    / "results"
    / "tables"
    / "gse194040_single_patient_prediction_example_v2_uncalibrated_score.csv"
)


def read_single_row_csv(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return next(csv.DictReader(handle))


def write_single_row_csv(path: Path, fieldnames: list[str], row: dict[str, str]) -> None:
    write_csv_rows(path, fieldnames, [row])


def write_csv_rows(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class SinglePatientPredictionCliTests(unittest.TestCase):
    def run_predictor(self, input_path: Path, output_path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(input_path), str(output_path)],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_example_input_produces_prediction_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "prediction.csv"
            result = self.run_predictor(EXAMPLE_INPUT, output_path)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue(output_path.exists())

            output = read_single_row_csv(output_path)
            self.assertEqual(
                list(output),
                [
                    "sample_id",
                    "patient_id",
                    "predicted_pCR_class",
                    "predicted_pCR_score",
                    "predicted_non_pCR_score",
                ],
            )
            self.assertIn(output["predicted_pCR_class"], {"0", "1"})
            pcr_score = float(output["predicted_pCR_score"])
            non_pcr_score = float(output["predicted_non_pCR_score"])
            self.assertGreaterEqual(pcr_score, 0.0)
            self.assertLessEqual(pcr_score, 1.0)
            self.assertAlmostEqual(pcr_score + non_pcr_score, 1.0, places=6)

            current = read_single_row_csv(CURRENT_EXAMPLE_OUTPUT)
            self.assertEqual(output["predicted_pCR_class"], current["predicted_pCR_class"])
            self.assertAlmostEqual(
                pcr_score,
                float(current["predicted_pCR_score"]),
                places=12,
            )
            self.assertAlmostEqual(
                non_pcr_score,
                float(current["predicted_non_pCR_score"]),
                places=12,
            )

    def test_zero_patient_rows_fails_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            input_path = tmpdir_path / "zero_rows.csv"
            output_path = tmpdir_path / "prediction.csv"
            row = read_single_row_csv(EXAMPLE_INPUT)
            write_csv_rows(input_path, list(row), [])

            result = self.run_predictor(input_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("Expected exactly one patient/sample row, but found 0 rows", result.stderr)

    def test_multiple_patient_rows_fails_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            input_path = tmpdir_path / "multiple_rows.csv"
            output_path = tmpdir_path / "prediction.csv"
            row = read_single_row_csv(EXAMPLE_INPUT)
            write_csv_rows(input_path, list(row), [row, row])

            result = self.run_predictor(input_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("Expected exactly one patient/sample row, but found 2 rows", result.stderr)

    def test_duplicate_columns_fail_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            input_path = tmpdir_path / "duplicate_columns.csv"
            output_path = tmpdir_path / "prediction.csv"
            row = read_single_row_csv(EXAMPLE_INPUT)
            duplicated_gene = next(name for name in row if name.startswith("expr_"))
            write_single_row_csv(input_path, list(row) + [duplicated_gene], row)

            result = self.run_predictor(input_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("Input CSV contains duplicate columns", result.stderr)
            self.assertIn(duplicated_gene, result.stderr)

    def test_nonnumeric_gene_value_fails_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            input_path = tmpdir_path / "nonnumeric.csv"
            output_path = tmpdir_path / "prediction.csv"
            row = read_single_row_csv(EXAMPLE_INPUT)
            invalid_gene = next(name for name in row if name.startswith("expr_"))
            row[invalid_gene] = "not-a-number"
            write_single_row_csv(input_path, list(row), row)

            result = self.run_predictor(input_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("nonnumeric gene-expression values", result.stderr)
            self.assertIn(invalid_gene, result.stderr)

    def test_infinite_gene_value_fails_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            input_path = tmpdir_path / "infinite.csv"
            output_path = tmpdir_path / "prediction.csv"
            row = read_single_row_csv(EXAMPLE_INPUT)
            invalid_gene = next(name for name in row if name.startswith("expr_"))
            row[invalid_gene] = "inf"
            write_single_row_csv(input_path, list(row), row)

            result = self.run_predictor(input_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("infinite gene-expression values", result.stderr)
            self.assertIn(invalid_gene, result.stderr)

    def test_all_missing_gene_values_fail_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            input_path = tmpdir_path / "all_missing.csv"
            output_path = tmpdir_path / "prediction.csv"
            row = read_single_row_csv(EXAMPLE_INPUT)
            for name in row:
                if name.startswith("expr_"):
                    row[name] = ""
            write_single_row_csv(input_path, list(row), row)

            result = self.run_predictor(input_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("All required gene-expression values are missing", result.stderr)

    def test_excessive_missing_gene_values_fail_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            input_path = tmpdir_path / "excessive_missing.csv"
            output_path = tmpdir_path / "prediction.csv"
            row = read_single_row_csv(EXAMPLE_INPUT)
            gene_columns = [name for name in row if name.startswith("expr_")]
            missing_count = len(gene_columns) // 5 + 1
            for name in gene_columns[:missing_count]:
                row[name] = ""
            write_single_row_csv(input_path, list(row), row)

            result = self.run_predictor(input_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("excessive missing gene-expression values", result.stderr)
            self.assertIn("maximum allowed is 20%", result.stderr)

    def test_unsupported_input_format_fails_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            input_path = tmpdir_path / "patient.json"
            output_path = tmpdir_path / "prediction.csv"
            row = read_single_row_csv(EXAMPLE_INPUT)
            write_single_row_csv(input_path, list(row), row)

            result = self.run_predictor(input_path, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("Unsupported input format '.json'", result.stderr)

    def test_missing_required_gene_column_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            malformed_input = tmpdir_path / "missing_gene.csv"
            output_path = tmpdir_path / "prediction.csv"

            row = read_single_row_csv(EXAMPLE_INPUT)
            fieldnames = list(row)
            missing_gene = next(name for name in fieldnames if name.startswith("expr_"))
            fieldnames.remove(missing_gene)
            row.pop(missing_gene)
            write_single_row_csv(malformed_input, fieldnames, row)

            result = self.run_predictor(malformed_input, output_path)

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
            self.assertIn("ERROR: Input CSV is missing required gene-expression columns", result.stderr)
            self.assertIn(missing_gene, result.stderr)

    def test_extra_non_feature_columns_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            baseline_output = tmpdir_path / "baseline_prediction.csv"
            extra_input = tmpdir_path / "extra_column_input.csv"
            extra_output = tmpdir_path / "extra_prediction.csv"

            baseline = self.run_predictor(EXAMPLE_INPUT, baseline_output)
            self.assertEqual(baseline.returncode, 0, msg=baseline.stderr)

            row = read_single_row_csv(EXAMPLE_INPUT)
            fieldnames = list(row) + ["extra_note"]
            row["extra_note"] = "ignored by prediction script"
            write_single_row_csv(extra_input, fieldnames, row)

            result = self.run_predictor(extra_input, extra_output)
            self.assertEqual(result.returncode, 0, msg=result.stderr)

            baseline_row = read_single_row_csv(baseline_output)
            extra_row = read_single_row_csv(extra_output)
            self.assertEqual(
                baseline_row["predicted_pCR_class"],
                extra_row["predicted_pCR_class"],
            )
            self.assertAlmostEqual(
                float(baseline_row["predicted_pCR_score"]),
                float(extra_row["predicted_pCR_score"]),
                places=12,
            )
            self.assertAlmostEqual(
                float(baseline_row["predicted_non_pCR_score"]),
                float(extra_row["predicted_non_pCR_score"]),
                places=12,
            )


if __name__ == "__main__":
    unittest.main()
