from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)

from .utilities import CMtoCMDisplay

import shap
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
        shap_beeswarm = ...  # TODO? c.f. https://stackoverflow.com/a/76083743 for beeswarm example

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

        prediction = self.classifier.predict(new_data)
        # print(f"DTC ---> New sample output is {prediction}")
        output_string = f"The patient is expected to be a {'non-' if prediction == 0 else ''}responder"

        # print(f"Got new data {new_data}\nAttempting to create a SHAP force plot")

        # TODO?
        # explainer = shap.TreeExplainer(self.classifier)
        # explanation = explainer(new_data)

        # image = shap.plots.force(
        #     explainer.expected_value[0],
        #     explanation[0][0,:],
        #     new_data,
        #     matplotlib=True,
        #     )

        # XXX?
        image = "TBD"

        return {"Prediction": output_string, "image": image}

    def save_model(self):
        raise NotImplementedError
