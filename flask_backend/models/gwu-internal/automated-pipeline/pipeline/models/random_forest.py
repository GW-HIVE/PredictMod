from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)


class RandomForestClassifierHandler:

    def __init__(self, labels, data):
        self.labels = labels
        self.data = data
        self.classifier = None

    def train_model(self):
        X, X_test, Y, Y_test = train_test_split(
            self.data, self.labels, test_size=0.20, random_state=42
        )

        classifier = RandomForestClassifier(random_state=42)
        classifier.fit(X, Y)

        predictions = classifier.predict(X_test)
        accuracy = accuracy_score(Y_test, predictions)
        mae = mean_absolute_error(Y_test, predictions)
        train_predictions = classifier.predict(self.data)
        report = classification_report(self.labels, train_predictions)
        cm = confusion_matrix(self.labels, train_predictions)

        self.classifier = classifier

        return {
            "Method": "Random Forest",
            "Accuracy": accuracy,
            "Mean Absolute Error": mae,
            "Classification Report": report,
            "Confusion Matrix": cm,
        }

    def sample_prediction(self):
        raise NotImplementedError

    def save_model(self):
        raise NotImplementedError
