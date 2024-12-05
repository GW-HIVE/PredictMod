from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)


class DecisionTreeClassifierHandler:

    def __init__(self, labels, samples):
        self.labels = labels
        self.samples = samples

    def train_model(self):
        X, X_test, Y, Y_test = train_test_split(
            self.samples, self.labels, test_size=0.2
        )
        classifier = DecisionTreeClassifier()
        classifier.fit(X, Y)
        predictions = classifier.predict(X_test)

        accuracy = accuracy_score(Y_test, predictions)
        mae = mean_absolute_error(Y_test, predictions)
        train_predictions = classifier.predict(self.samples)
        report = classification_report(self.labels, train_predictions)
        cm = confusion_matrix(self.labels, train_predictions)

        return {
            "Method": "Decision Tree (Classifier)",
            "Accuracy": accuracy,
            "Mean Absolute Error": mae,
            "Classification Report": report,
            "Confusion Matrix": cm,
        }

    def sample_prediction(self):
        raise NotImplementedError

    def save_model(self):
        raise NotImplementedError
