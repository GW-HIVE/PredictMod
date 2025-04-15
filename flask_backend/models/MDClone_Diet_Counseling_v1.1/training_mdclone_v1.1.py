#%%
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

print(f"Train Score: {model.score(X_train, y_train)}")
print(f"Test Score:  {model.score(X_test, y_test)}")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

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
top_n = 10
top_indices = indices[:top_n]

# Print top 10
print("\nTop 10 Permutation Feature Importances:")
for idx in top_indices:
    print(f"{feature_names[idx]}: {importances[idx]:.4f}")

# Plot top 10
plt.figure(figsize=(10, 6))
plt.title("Top 10 Permutation Feature Importances")
plt.bar(range(top_n), importances[top_indices], align='center')
plt.xticks(range(top_n), feature_names[top_indices], rotation=45, ha='right')
plt.tight_layout()
plt.show()
#%%
#Convert model into pickle 
#Filename should be as follows: [resource]_[version #].pkl 
# model = DTC
# filename = "mdclone_v1.1.pkl"
# with open(filename, "wb") as fp:
#     pickle.dump(model, fp)
# fp.close()
#%%
