from fastapi import FastAPI, HTTPException
import os
import pandas as pd
import joblib
from pathlib import Path


script_dir = Path(__file__).parent

# Absolute path inside the container
MODEL_PATH = f"{script_dir}/LungCancer_classifier_and_features.pickle"


def load_model():
    #if not MODEL_PATH.exists():
    #    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    with open(MODEL_PATH, "rb") as f:
        return joblib.load(f)

#model = 
# ---------------------------------------------------------
# Load saved artifacts once when the service starts
# ---------------------------------------------------------
#model_file = "../../LungCancer_classifier_and_features.pickle"

saved_pipeline = load_model()

rf_model = saved_pipeline["classifier"]
pca_transformer = saved_pipeline["pca"]
expected_features = saved_pipeline["features"]

print(f"Loaded model. Expecting {len(expected_features)} gene features.")


# ---------------------------------------------------------
# Label mapping
# ---------------------------------------------------------
label_map = {
    0: "Alive",
    1: "Dead"
}


# ---------------------------------------------------------
# Prediction function
# ---------------------------------------------------------
def predict(file_path):
    """
    Predict lung-cancer outcome from a CSV file.

    Parameters
    ----------
    file_path : str
        Full path to the CSV file.

    Returns
    -------
    list of dict
        Prediction results.
    """
    # Extract the filename from the Windows path: "gene_expression_data_new.csv"
    filename = Path(file_path).name

    # Construct path inside container: /app/data/gene_expression_data_new.csv
    #container_path = Path("/app/data") / filename
    container_path = file_path

    #if not container_path.exists():
    #    raise HTTPException(
    #        status_code=404, 
    #        detail=f"File not found inside container at: {container_path}"
    #    )
        
    #df = pd.read_csv(container_path)

    # -----------------------------------------------------
    # Load raw expression data
    # -----------------------------------------------------
    new_raw_data = pd.read_csv(
        container_path,
        index_col=0
    )

    print(f"Raw Input Shape: {new_raw_data.shape}")

    # -----------------------------------------------------
    # Match training features
    # -----------------------------------------------------
    X_new = new_raw_data.reindex(
        columns=expected_features,
        fill_value=0
    )

    print(f"Reindexed Input Shape: {X_new.shape}")

    # -----------------------------------------------------
    # Apply saved PCA
    # -----------------------------------------------------
    X_new_pca = pca_transformer.transform(X_new)

    print(f"PCA Transformed Shape: {X_new_pca.shape}")

    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------
    predictions = rf_model.predict(X_new_pca)
    probabilities = rf_model.predict_proba(X_new_pca)

    # -----------------------------------------------------
    # Build results
    # -----------------------------------------------------
    results = []

    for sample_id, prediction, probability in zip(
        X_new.index,
        predictions,
        probabilities
    ):

        results.append({
            "Sample_ID": str(sample_id),
            "Predicted_Class": label_map[int(prediction)],
            "Prob_Alive": float(probability[0]),
            "Prob_Dead": float(probability[1])
        })

    return results
