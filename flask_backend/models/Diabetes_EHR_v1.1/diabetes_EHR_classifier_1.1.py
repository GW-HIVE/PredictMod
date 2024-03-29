from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

def run_training():
    df = pd.read_excel("data.xlsx")
    # Extract features (X) and labels (y)
    feature_names = df.columns[1:]
    X_data = df.iloc[:, 1:] # Assuming your features start in 2nd column
    Y_data = df.iloc[:, 0]   # Assuming your labels are in the 1st column
    return X_data,Y_data,feature_names

def train(X_dat,Y_dat):
    # Split the data into training and testing sets
    Xtrain, Xtest, ytrain, ytest = train_test_split(X_dat, Y_dat, test_size=0.2)

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
    # Perform Training on Model
    [X_data,Y_data,feature_names] = run_training()
    [classifier,acc_score,classifier_type_string] = train(X_data,Y_data)
    # Create a dictionary to store the classifier and feature names
    data = {'classifier': classifier, 'feature_names': list(X_data.columns)}
    # Save the dictionary to a pickle file
    joblib.dump(data, 'Diabetes_EHR_classifier_and_features.pickle')
    print(f"Patient train data has been predicted with an accuracy of: {acc_score} using {classifier_type_string}")