from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
train_data = pd.read_excel("C:\\Users\\17038\\Fall_2023\\work\\Classifier\\data.xlsx")
train_labels = pd.read_excel("C:\\Users\\17038\\Fall_2023\\work\\Classifier\\label.xlsx")
test_data = pd.read_excel("C:\\Users\\17038\\Fall_2023\\work\\Classifier\\sample_synthetic_EHR_data_1000patients.xlsx")
test_data = test_data.to_numpy()
test_data = test_data[:,1:]
X_train = train_data.to_numpy()
X_train = X_train[:,1:]
Y_train = train_labels.to_numpy()
patient_idx = int(input("Provide patient number (1-1000): "))

def train(X_train,Y_train):
    # Split the data into training and testing sets
    Xtrain, Xtest, ytrain, ytest = train_test_split(X_train, Y_train, test_size=0.2)#, random_state=42)

    # Create a decision tree classifier
    classifier = DecisionTreeClassifier()

    # Train the classifier on the training data
    classifier.fit(Xtrain, ytrain)

    # Make predictions on the testing data
    y_pred = classifier.predict(Xtest)
    accuracy = accuracy_score(ytest, y_pred)
    #print(f"Accuracy of classifier: {accuracy}")
    return classifier, accuracy
[classifier,acc] = train(X_train,Y_train)

if patient_idx <= 1000 and patient_idx >= 0:
# X is a 2D array with shape (n_samples, n_features)
# y is a 1D array with shape (n_samples,)
    patient_data = test_data[patient_idx,:]
    reshaped_patient = patient_data.reshape((1, 6))
    y_hat = classifier.predict(reshaped_patient)
    if int(y_hat) == 1:
        outcome = 'Non-Responsive'
    else:
        outcome = 'Responsive'
    print(f"Patient {patient_idx} has been predicted to be {outcome} with an accuracy of: {acc}")