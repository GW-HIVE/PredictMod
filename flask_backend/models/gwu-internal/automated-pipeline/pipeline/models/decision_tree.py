from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)

from .utilities import CMtoCMDisplay

import time


class DecisionTreeClassifierHandler:

    def __init__(self, labels, samples):
        self.labels = labels
        self.samples = samples

    def train_model(self):
        X, X_test, Y, Y_test = train_test_split(
            self.samples, self.labels, test_size=0.2
        )
        classifier = DecisionTreeClassifier()
        start = time.time()
        classifier.fit(X, Y)
        train_time = time.time() - start
        predictions = classifier.predict(X_test)

        accuracy = accuracy_score(Y_test, predictions)
        mae = mean_absolute_error(Y_test, predictions)
        train_predictions = classifier.predict(self.samples)
        report = classification_report(self.labels, train_predictions)
        cm = confusion_matrix(self.labels, train_predictions)

        image = CMtoCMDisplay(cm)

        self.classifier = classifier

        return {
            "Method": "Decision Tree (Classifier)",
            "Accuracy": accuracy,
            "Mean Absolute Error": mae.tolist(),
            "Classification Report": report,
            "Confusion Matrix": image,
            "Training Time": train_time,
        }

    def sample_prediction(self, new_data):
        return self.classifier.predict(new_data)

    def save_model(self):
        raise NotImplementedError
