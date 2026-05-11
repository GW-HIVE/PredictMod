#Imported packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Importing necessary modules from sklearn
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
print("Ready to Go")

#Importing Dataset GSE74777_series_matrix.txt.gz
# Tab-separated file
train_table = pd.read_csv(r"C:\Users\cpkbh\OneDrive\Desktop\PredictMod\GSE74777_series_matrix.csv"
)  
# ignores lines starting with !
print("Table Loaded")
print(train_table.head())

# set gene IDs as index
train_table = train_table.set_index("ID_REF")

# transpose so rows = samples and columns = genes
train_table = train_table.T

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# temporary labels (still random for now)
train_table["Responder"] = np.random.randint(0,2,len(train_table))

X = train_table.drop(["Responder"], axis=1)
y = train_table["Responder"]

# ---- Scale features ----
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---- Reduce dimensionality ----
pca = PCA(n_components=20)  # try 10–50 depending on performance
X_pca = pca.fit_transform(X_scaled)

# ---- Train-test split ----
X_train, X_test, y_train, y_test = train_test_split(
    X_pca, y,
    test_size=0.25,
    random_state=123
)

print("Ready to Go")

#Viewing performance metrics of Random Forest Classifier

RF = RandomForestClassifier(random_state=123)
RF.fit(X_train,y_train)
print(f'RandomForestClassifier train score: {RF.score(X_train,y_train)}')
print(f'RandomForestClassifier test score:  {RF.score(X_test,y_test)}')
print(confusion_matrix(y_test, RF.predict(X_test)))
print(classification_report(y_test, RF.predict(X_test)))
from sklearn.metrics import ConfusionMatrixDisplay

# Get predictions ONCE (cleaner)
y_pred = RF.predict(X_test)

# Plot confusion matrix
ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    display_labels=["Non-Responder", "Responder"],  # you can rename later
    cmap="Blues",
    values_format="d"
)

plt.title("Random Forest Confusion Matrix")
plt.show()


from sklearn.metrics import roc_curve, auc

# Get probability predictions (NOT just 0/1 labels)
y_probs = RF.predict_proba(X_test)[:, 1]

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