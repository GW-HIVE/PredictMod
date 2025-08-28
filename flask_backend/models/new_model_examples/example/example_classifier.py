from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd

def train(X_data, Y_data):
    # Split the data into training and testing sets
    Xtrain, Xtest, ytrain, ytest = train_test_split(X_data, Y_data, test_size=0.2,random_state=42)

    # Create a decision tree classifier
    classifier = DecisionTreeClassifier()
    # Train the classifier on the training data
    classifier.fit(Xtrain, ytrain)

    # Make predictions on the testing data
    y_pred = classifier.predict(Xtest)

    accuracy = accuracy_score(ytest, y_pred)
    #print(f"Accuracy of classifier: {accuracy}")

    # Calculate Mean Absolute Error
    mae = mean_absolute_error(ytest, y_pred)

    return classifier, accuracy, mae

if __name__ == "__main__":
    df = pd.read_csv("example_feature_data.csv")

    encoder = LabelEncoder()
    Y_data = encoder.fit_transform(df["Status"])
    X_data = df.drop(columns=["Status"])

    # print(Y_data)
    # print(X_data.columns)

    # Perform Training on Model
    classifier, acc_score, mae = train(X_data, Y_data)

    # Save the classifier to a pickle file
    with open("example_classifier.pkl", "wb") as fp:
        pickle.dump(classifier, fp)
    print(f"Example data has been predicted with an accuracy of: {acc_score} and MAE of: {mae}")

