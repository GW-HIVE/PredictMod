#%%
import pandas as pd
from sklearn.model_selection import LeaveOneOut
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
import numpy as np
import pickle

# Load the upsampled dataset
df = pd.read_csv('resampled_dataset.csv')

target_column = 'response'  # Adjust as needed

# Separate features and target
X = df.drop(target_column, axis=1)
y = df[target_column]

# Initialize Leave-One-Out cross-validation
loo = LeaveOneOut()
accuracies = []
f1_scores = []
y_true, y_pred = [], []

# Initialize the Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)

for train_index, test_index in loo.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    # Train the model
    rf.fit(X_train, y_train)
    
    # Make prediction
    y_hat = rf.predict(X_test)
    
    # Store results
    y_true.append(y_test.values[0])
    y_pred.append(y_hat[0])
    
    accuracies.append(accuracy_score([y_test.values[0]], [y_hat[0]]))
    f1_scores.append(f1_score([y_test.values[0]], [y_hat[0]], average='weighted'))

# Calculate overall accuracy and F1 score
overall_accuracy = np.mean(accuracies)
overall_f1 = np.mean(f1_scores)

print(f'Overall Accuracy: {overall_accuracy:.4f}')
print(f'Overall F1 Score: {overall_f1:.4f}')
print('Classification Report:\n', classification_report(y_true, y_pred))

# Pickle the trained model
with open('prediabetes_proteomics_model.pkl', 'wb') as model_file:
    pickle.dump(rf, model_file)

print('Model has been saved as random_forest_model.pkl')
# %%
