#Imported packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
#Importing necessary modules from sklearn
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA

from pathlib import Path

script_dir = Path(__file__).parent
gene_expr_file_path = script_dir / "gene_expression_data.csv"
clinical_data_file_path = script_dir / "valid_clinical_data.csv"

print("Ready to Go")

# ---------------------------------------------------------
# Step 1: Load CSV Files
# ---------------------------------------------------------
expr_df = pd.read_csv(gene_expr_file_path, index_col=0)
valid_clinical = pd.read_csv(clinical_data_file_path, index_col=0)

# Align samples
common_gsm = expr_df.index.intersection(valid_clinical.index)
X = expr_df.loc[common_gsm]
y = valid_clinical.loc[common_gsm, "mortality_target"].astype(int)

print(f"Original Feature Matrix shape: {X.shape}")

# ---------------------------------------------------------
# Step 2: Train/Test Split
# ---------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# ---------------------------------------------------------
# Step 3: Dimensionality Reduction using PCA (20 Components)
# ---------------------------------------------------------
pca = PCA(n_components=20, random_state=42)

# Fit PCA on training set only, then transform both train and test sets
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Check total variance explained by 20 components
explained_var = pca.explained_variance_ratio_.sum()
print(f"\nPCA Reduced Shape: {X_train_pca.shape}")
print(f"Total Explained Variance (20 components): {explained_var * 100:.2f}%")
print("Ready to Go")
print(X_test_pca[0,:])

#Viewing performance metrics of Random Forest Classifier
rf = RandomForestClassifier(random_state=123)
rf.fit(X_train_pca,y_train)
print(f'RandomForestClassifier train score: {rf.score(X_train_pca,y_train)}')
print(f'RandomForestClassifier test score:  {rf.score(X_test_pca,y_test)}')
print(confusion_matrix(y_test, rf.predict(X_test_pca)))
print(classification_report(y_test, rf.predict(X_test_pca)))
from sklearn.metrics import ConfusionMatrixDisplay

# Get predictions ONCE (cleaner)
y_pred = rf.predict(X_test_pca)


data = {
    'classifier': rf,
    'pca': pca,                  # <--- Save PCA object here!
    'features': list(X.columns)
}

# Generate the pickle file in the same directory as this script
joblib.dump(data, f"{script_dir}/LungCancer_classifier_and_features.pickle")
print("Model and PCA pipeline successfully saved!")


# Plot confusion matrix
ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    display_labels=["alive", "dead"],  # you can rename later
    cmap="Blues",
    values_format="d"
)

plt.title("Random Forest Confusion Matrix")
plt.show()


from sklearn.metrics import roc_curve, auc

# Get probability predictions (NOT just 0/1 labels)
y_probs = rf.predict_proba(X_test_pca)[:, 1]

# Compute ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_probs)

# Compute AUC score
roc_auc = auc(fpr, tpr)

# Plot
plt.figure()
plt.plot(fpr, tpr, label=f'Random Forest (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], linestyle='--')  # diagonal line

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve - Random Forest')
plt.legend()
plt.show()