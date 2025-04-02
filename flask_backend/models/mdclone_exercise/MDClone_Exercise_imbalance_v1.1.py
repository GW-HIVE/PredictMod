from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, mean_absolute_error, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
import joblib
import pandas as pd 
import numpy as np

def prepare_training():
    df = pd.read_excel('Exercise_synthetic_curate.xlsx')
    # Extract features (X) and labels (y)
    feature_names = df.columns[:-1]  # Exclude the last column for Y_data
    X_data = df.iloc[:, :-1]  # All columns except the last one for features
    Y_data = df.iloc[:, -1]   # Last column for labels
    print(X_data)
    return X_data, Y_data, feature_names

def train(X_dat, Y_dat):
    # Balance the classes using RandomOverSampler
    ros = RandomOverSampler(random_state=10)
    X_balanced, Y_balanced = ros.fit_resample(X_dat, Y_dat)
    
    # Normalize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_balanced)
    
    # Split the data into training and testing sets
    Xtrain, Xtest, ytrain, ytest = train_test_split(X_scaled, Y_balanced, test_size=0.4, random_state=10)

    # Create a decision tree classifier
    classifier = DecisionTreeClassifier(random_state=42)
    classifier_type_string = type(classifier).__name__

    # Train the classifier on the training data
    classifier.fit(Xtrain, ytrain)

    # Make predictions on the testing data
    y_pred = classifier.predict(Xtest)
    accuracy = accuracy_score(ytest, y_pred)

    # Calculate Mean Absolute Error
    mae = mean_absolute_error(ytest, y_pred)

    # Compute Confusion Matrix
    conf_matrix = confusion_matrix(ytest, y_pred)

    return classifier, accuracy, mae, classifier_type_string, scaler, conf_matrix

def feature_importance(classifier, feature_names):
    importances = classifier.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    return feature_importance_df

if __name__ == "__main__":
    # Perform Training on Model
    X_data, Y_data, feature_names = prepare_training()
    classifier, acc_score, mae, classifier_type_string, scaler, conf_matrix = train(X_data, Y_data)
    
    # Create a dictionary to store the classifier, scaler, and feature names
    data = {'classifier': classifier, 'scaler': scaler, 'feature_names': list(X_data.columns)}
    
    # Save the dictionary to a pickle file
    joblib.dump(data, 'Diabetes_EHR_classifier_and_features.pickle')
    
    # Display feature importances
    feature_importance_df = feature_importance(classifier, feature_names)
    print("Feature importances:")
    print(feature_importance_df)
    
    # Print the Confusion Matrix
    print("Confusion Matrix:")
    print(conf_matrix)
    
    print(f"Patient train data has been predicted with an accuracy of: {acc_score} and MAE of: {mae} using {classifier_type_string}")
