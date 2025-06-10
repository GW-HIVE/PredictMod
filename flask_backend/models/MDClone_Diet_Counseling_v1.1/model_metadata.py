#%%
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import io
import json

#%%
df = pd.read_csv("clean_mdclone_v1.1.csv")

X = df.drop(["response"], axis=1)
y = df["response"]

# HistGradientBoostingClassifier supports missing values natively, 
# but to be safe, convert to numeric types (if not already)
X = X.apply(pd.to_numeric, errors='coerce')

# No imputation needed unless you want to fill missing manually

#%%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=123)

model = HistGradientBoostingClassifier(
    max_iter=100,
    learning_rate=0.1,
    max_depth=5,
    class_weight={0: 1, 1: 3},
    random_state=123
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

print(f"Train Score: {model.score(X_train, y_train)}")
print(f"Test Score:  {model.score(X_test, y_test)}")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

from base64 import b64encode

def CMtoCMDisplay(cm, labels=None):
    buf = io.BytesIO()
    if labels is not None:
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        plt.savefig(buf, format="png", bbox_inches="tight")
        return b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot()
    plt.savefig(buf, format="png", bbox_inches="tight")
    return b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")

cm_plot = CMtoCMDisplay(cm)

#%%
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import numpy as np

# Compute permutation importances
result = permutation_importance(
    model, X_test, y_test,
    n_repeats=10,
    random_state=42,
    n_jobs=-1
)

importances = result.importances_mean
indices = np.argsort(importances)[::-1]
feature_names = X.columns

# Select top 10 features
top_n = 5
top_indices = list(indices[:top_n])
bottom_indicies = list(indices[-top_n:])
top_indices.extend(bottom_indicies)
print(top_indices)
# Print top 10
print("\nTop 10 Permutation Feature Importances:")
feature_importance = []
for idx in top_indices:
    # print(f"{feature_names[idx]}: {importances[idx]:.4f}")
    feature_importance.append((feature_names[idx], f"{importances[idx]:.4f}"))

with open("metadata.json", "w") as fp:
    json.dump({
        "feature_importance": feature_importance,
        "confusion_matrix": cm_plot,
    },
    fp, indent=2)
