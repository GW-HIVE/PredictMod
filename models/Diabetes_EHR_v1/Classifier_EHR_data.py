from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
def run_training():
    train_data = pd.read_excel("C:\\Users\\17038\\a_Fall_2023\\work\\Classifier\\data.xlsx")
    train_labels = pd.read_excel("C:\\Users\\17038\\a_Fall_2023\\work\\Classifier\\label.xlsx")
    # test_data = pd.read_excel("C:\\Users\\17038\\a_Fall_2023\\work\\Classifier\\sample_synthetic_EHR_data_1000patients.xlsx")
    test_data = pd.read_excel("C:\\Users\\17038\\a_Fall_2023\\work\\Classifier\\single_patient_input.xlsx")
    test_data = test_data.to_numpy()
    test_data = test_data[:,0:]
    X_train = train_data.to_numpy()
    X_train = X_train[:,1:] #221:
    Y_train = train_labels.to_numpy()
    Y_train = Y_train[:] #221:
    return X_train,Y_train

def train(X_train,Y_train):
    # Split the data into training and testing sets
    Xtrain, Xtest, ytrain, ytest = train_test_split(X_train, Y_train, test_size=0.2)#, random_state=42)

    # Create a decision tree classifier
    classifier = DecisionTreeClassifier()
    classifier_type_string = type(classifier).__name__
    # Train the classifier on the training data
    classifier.fit(Xtrain, ytrain)

    # Make predictions on the testing data
    y_pred = classifier.predict(Xtest)
    accuracy = accuracy_score(ytest, y_pred)
    #print(f"Accuracy of classifier: {accuracy}")
    return classifier, accuracy, classifier_type_string

if __name__ == "__main__":
    # Load your trained classifier, scaler, and label_encoder

    # Get user input for the file path
    file_path = input('Enter the file path for single patient input (e.g., C:\\Users\\17038\\a_Fall_2023\\work\\Classifier\\single_patient_input.xlsx): ')

    # Read the Excel file
    try:
        test_data = pd.read_excel(file_path)
    except Exception as e:
        print(f'Error reading the file: {e}')
        exit()

    # Extract features (X) from the test_data DataFrame
    X_patient_input = test_data.iloc[:, 3:].values  # Assuming your features start from the 4th column

    # Process single patient input
    [X_train,Y_train] = run_training()
    [classifier,acc,classifier_type_string] = train(X_train,Y_train)

    patient_data = test_data.to_numpy()
    reshaped_patient = patient_data.reshape((1, 6))
    y_hat = classifier.predict(reshaped_patient)
    if int(y_hat) == 1:
        outcome = 'Non-Responsive'
    else:
        outcome = 'Responsive'
    print(f"Patient input data has been predicted to be {outcome} with an accuracy of: {acc} using {classifier_type_string}")
