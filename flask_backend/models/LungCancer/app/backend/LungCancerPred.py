import pandas as pd
import numpy as np
import joblib

# ---------------------------------------------------------
# Step 1: Load Saved Artifacts (Model, PCA, Features)
# ---------------------------------------------------------
model_file = 'LungCancer_classifier_and_features.pickle'
saved_pipeline = joblib.load(model_file)

rf_model = saved_pipeline['classifier']
pca_transformer = saved_pipeline['pca']
expected_features = saved_pipeline['features']

print(f"Loaded model. Expecting {len(expected_features)} gene features.")

# ---------------------------------------------------------
# Step 2: Load New / Unseen Raw Expression Data
# ---------------------------------------------------------
# Replace with the path to your new sample CSV
# The file should have sample IDs as rows/index and probe IDs as columns
new_raw_data = pd.read_csv("/Users/diyakb/Documents/GitHub/PredictMod/flask_backend/models/LungCancer/app/backend/gene_expression_data_new.csv", index_col=0)

# Reindex to match training feature order (fill missing probes with 0)
X_new = new_raw_data.reindex(columns=expected_features, fill_value=0)

print(f"Raw Input Shape: {X_new.shape}")

# ---------------------------------------------------------
# Step 3: Apply Saved PCA Dimensionality Reduction
# ---------------------------------------------------------
# IMPORTANT: Use .transform(), NOT .fit_transform()
X_new_pca = pca_transformer.transform(X_new)

print(f"PCA Transformed Shape: {X_new_pca.shape}")

# ---------------------------------------------------------
# Step 4: Run Inference & Get Probabilities
# ---------------------------------------------------------
predictions = rf_model.predict(X_new_pca)
probabilities = rf_model.predict_proba(X_new_pca)

print(predictions)

# Label mapping
label_map = {0: "Alive", 1: "Dead"}

# Build Results DataFrame
results_df = pd.DataFrame({
    'Sample_ID': X_new.index,
    'Predicted_Class': [label_map[p] for p in predictions],
    'Prob_Alive': probabilities[:, 0],
    'Prob_Dead': probabilities[:, 1]
}).set_index('Sample_ID')

# Display first few predictions
print("\n=== Prediction Results ===")
print(results_df.head(10))

# Optional: Save predictions to CSV
    # results_df.to_csv("/Users/diyakb/Documents/GitHub/PredictMod/flask_backend/models/LungCancer/app/backend/gene_expression_data_new.csv")