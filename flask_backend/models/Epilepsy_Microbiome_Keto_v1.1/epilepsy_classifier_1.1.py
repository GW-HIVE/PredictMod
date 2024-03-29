import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load your data
file_path = "epilepsy_keto_data_500.xlsx"
df = pd.read_excel(file_path)

# Extract features (X) and labels (y)
feature_names = df.columns[3:] 
X_dat = df.iloc[:, 2:]  # Assuming your features start from the 3rd column
y_str = df.iloc[:, 1]   # Assuming your labels are in the 2nd column


# Convert labels to numerical values using LabelEncoder
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_str)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_dat, y, test_size=0.2)
# Standardize the features (optional but often recommended)
scaler = StandardScaler()
#X_train = scaler.fit_transform(X_train)
#X_test = scaler.transform(X_test)

# Create a Logistic Regression classifier
classifier = LogisticRegression()

# Train the classifier
classifier.fit(X_train, y_train)

# Save the classifier and feature names
data = {'classifier': classifier, 'feature_names': list(X_dat.columns),'encoder': label_encoder}
# Save the dictionary to a pickle file
joblib.dump(data, 'Epilepsy_keto_classifier_and_features.pickle')

# Make predictions on the test set
y_pred = classifier.predict(X_test)

# Convert predicted labels back to original form
y_pred_str = label_encoder.inverse_transform(y_pred)

# Evaluate the performance of the classifier
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print(f'Confusion Matrix:\n{conf_matrix}')
print(f'Classification Report:\n{classification_rep}')
