"""
predict_single_patient.py

This is the "single-patient prediction script" required by the volunteership
completion criteria: a small, standalone tool that takes one patient's clinical
and genomic information and returns a disease-free survival (DFS) recurrence
risk prediction, using the model that train_model.py already trained and
saved to model/dfs_model.joblib.

The point of keeping this separate from the training script is that, in a real
BioCompute-style submission package, someone should be able to run a single
prediction without needing to retrain anything or understand the notebook.
They just need the saved model file, this script, and one patient's data.

How to run it:

    Using the built-in example patient:
        python predict_single_patient.py --example

    Using your own patient, from a JSON file:
        python predict_single_patient.py --input my_patient.json

    See example_patient.json in this folder for the exact fields expected.

What you get back:
    - the predicted probability of recurrence/progression (a number from 0 to 1)
    - a plain-language risk classification at two different decision
      thresholds saved by train_model.py: a "screening" threshold (more
      sensitive, flags more patients) and a "balanced" threshold (fewer false
      alarms, but also catches fewer true recurrences)
"""

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "model" / "dfs_model.joblib"
METADATA_PATH = PROJECT_DIR / "model" / "model_metadata.json"
EXAMPLE_PATIENT_PATH = PROJECT_DIR / "example_patient.json"


def load_model_and_metadata():
    """Load the fitted pipeline and the metadata that describes how to use it.

    Loading both together matters because the metadata file is what tells us
    which columns the model expects and which decision thresholds to apply.
    Without it, we would have to hard-code those values here and they could
    silently drift out of sync with whatever train_model.py actually saved.
    """
    if not MODEL_PATH.exists():
        sys.exit(
            f"Could not find a trained model at {MODEL_PATH}.\n"
            "Run 'python train_model.py' first to train and save the model."
        )

    model = joblib.load(MODEL_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return model, metadata


def load_patient_record(input_path: Path | None, use_example: bool) -> dict:
    """Read one patient's feature values from either a JSON file or the
    bundled example patient.
    """
    if use_example:
        source_path = EXAMPLE_PATIENT_PATH
    elif input_path is not None:
        source_path = input_path
    else:
        sys.exit(
            "Please provide either --input <path-to-patient.json> or --example."
        )

    if not source_path.exists():
        sys.exit(f"Patient file not found: {source_path}")

    with open(source_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_patient_record(patient: dict, metadata: dict) -> None:
    """Check that the patient record has every column the model expects.

    We check this ourselves, instead of just letting the pipeline fail with a
    confusing internal error, so that anyone using this script (who might not
    know scikit-learn) gets a clear message about exactly what is missing.
    """
    expected_columns = metadata["numeric_features"] + metadata["categorical_features"]
    missing = [col for col in expected_columns if col not in patient]

    if missing:
        sys.exit(
            "The patient record is missing the following required fields:\n"
            + "\n".join(f"  - {col}" for col in missing)
            + f"\n\nSee {EXAMPLE_PATIENT_PATH.name} for a complete example."
        )


def predict(model, metadata: dict, patient: dict) -> dict:
    """Run the pipeline on a single patient and translate the raw probability
    into something a human can act on.
    """
    # The pipeline expects a DataFrame with the same column layout it was
    # trained on, even though we are only scoring one row. Wrapping the single
    # patient dict in a list gives us a one-row DataFrame.
    expected_columns = metadata["numeric_features"] + metadata["categorical_features"]
    patient_df = pd.DataFrame([patient])[expected_columns]

    probability = float(model.predict_proba(patient_df)[0, 1])

    screening_threshold = metadata["decision_thresholds"]["screening"]["value"]
    balanced_threshold = metadata["decision_thresholds"]["balanced"]["value"]

    return {
        "recurrence_probability": round(probability, 4),
        "screening_flag": (
            "AT-RISK (recurrence flagged)"
            if probability >= screening_threshold
            else "Not flagged"
        ),
        "balanced_flag": (
            "AT-RISK (recurrence flagged)"
            if probability >= balanced_threshold
            else "Not flagged"
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Predict DFS recurrence risk for a single patient."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to a JSON file describing one patient's features.",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run the prediction on the bundled example patient instead of a file.",
    )
    args = parser.parse_args()

    model, metadata = load_model_and_metadata()
    patient = load_patient_record(args.input, args.example)
    validate_patient_record(patient, metadata)
    result = predict(model, metadata, patient)

    print("=" * 60)
    print("DFS RECURRENCE RISK PREDICTION")
    print("=" * 60)
    print(f"Predicted probability of recurrence/progression: {result['recurrence_probability']:.1%}")
    print()
    print(f"Screening threshold (>= {metadata['decision_thresholds']['screening']['value']:.2f}): {result['screening_flag']}")
    print(f"Balanced threshold  (>= {metadata['decision_thresholds']['balanced']['value']:.2f}): {result['balanced_flag']}")
    print()
    print(
        "Reminder: this model is a research and educational artifact trained on "
        "895 TCGA-BRCA patients. It has not been clinically validated and should "
        "not be used to make real treatment decisions."
    )


if __name__ == "__main__":
    main()
