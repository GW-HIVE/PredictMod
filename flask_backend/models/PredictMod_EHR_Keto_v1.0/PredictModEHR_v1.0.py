#%%
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Step 1: Load the pickled model
with open('svm_classifier.pkl', 'rb') as f:
    svm_model = pickle.load(f)

# Step 2: Load the sample data
# You can replace this with your actual sample data file
sample_data = pd.read_csv('test.csv')  # or use any method to load the sample

# For example, using StandardScaler:
scaler = StandardScaler()  # Or use the actual scaler used during training
sample_data_scaled = scaler.fit_transform(sample_data)

# Step 3: Reshape the sample data if it’s a single instance
# If the sample data is a single instance (single row), reshape it to 2D.
if sample_data_scaled.ndim == 1:
    sample_data_scaled = sample_data_scaled.reshape(1, -1)

# Step 5: Make a prediction using the SVM model
prediction = svm_model.predict(sample_data_scaled)
prediction_label = "Non-Responder" if prediction == 1 else "Responder"
# Step 6: Print or return the result
print("Prediction of response to a ketogenic diet:", prediction_label)
