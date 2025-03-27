#%%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score, roc_auc_score
import pickle

# Load dataset
df = pd.read_csv("augmented_baseline_proteomics.csv")

# Define features and target
X = df.drop(columns=["response"])
y = df["response"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Define a pipeline with standard scaling and logistic regression
logreg_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('logreg', LogisticRegression(C=100, penalty='l1', solver='liblinear', max_iter=1000, class_weight="balanced"))
])

# Train the logistic regression model
logreg_pipeline.fit(X_train, y_train)

# Make predictions
y_train_pred = logreg_pipeline.predict(X_train)
y_test_pred = logreg_pipeline.predict(X_test)

# Calculate metrics
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)
f1_train = f1_score(y_train, y_train_pred)
f1_test = f1_score(y_test, y_test_pred)
auc = roc_auc_score(y_test, y_test_pred)

# Print results
print("Logistic Regression Results:")
print("Train Accuracy:", train_accuracy)
print("Test Accuracy:", test_accuracy)
print("F1 Test Score:", f1_test)
print("F1 Train Score:", f1_train)
print("AUC Score:", auc)
print("Classification Report:\n", classification_report(y_test, y_test_pred))

# Pickle the trained model
with open('prediabetes_proteomics_model.pkl', 'wb') as model_file:
    pickle.dump(logreg_pipeline, model_file)

print('Model has been saved as prediabetes_proteomics_model.pkl')
# %%
