import numpy as np
import pandas as pd
import sklearn as skl
import pickle
from base64 import b64encode
import time

from .models import (
    PCAHandler,
    DecisionTreeClassifierHandler,
    LogisticRegressionHandler,
    RandomForestClassifierHandler,
    SupportVectorMachineHandler,
)


def package_for_shipping(name, model_obj):
    return {
        "name": name,
        "encoded_object": b64encode(pickle.dumps(model_obj)).decode("utf-8"),
    }


def regressions(label_data, data):

    pca = PCAHandler(label_data, data)
    pca.train_model()


def binary_classifiers(label_data, data):

    results = []
    pickles = []

    pca = PCAHandler(label_data, data)
    results.append(pca.train_model())
    pickles.append(package_for_shipping("PCA", pca))

    label_data = label_data.apply(lambda x: 0 if x == "R" else 1)

    print("---> LR")
    lr = LogisticRegressionHandler(label_data, data)
    results.append(lr.train_model())
    pickles.append(package_for_shipping("Logistic Regression", lr))

    print("---> DTC")
    dtc = DecisionTreeClassifierHandler(label_data, data)
    results.append(dtc.train_model())
    pickles.append(package_for_shipping("Decision Tree Classifier", dtc))

    print("---> RFC")
    rfc = RandomForestClassifierHandler(label_data, data)
    results.append(rfc.train_model())
    pickles.append(package_for_shipping("Random Forest", rfc))

    print("---> SVM")
    svm = SupportVectorMachineHandler(label_data, data)
    results.append(svm.train_model())
    pickles.append(package_for_shipping("Support Vector Machine", svm))

    return {"results": results, "pickles": pickles}


def multiclass_classifiers(label_data, data):

    pca = PCAHandler(label_data, data)
    pca.train_model()


class Pipeline:
    def __init__(self):
        pass

    def train_models(self, raw_data, label_column, drop_columns, outcome_type="binary"):

        print(f"===> Automated Pipeline - Got a request! <===")

        if not isinstance(raw_data, pd.DataFrame):
            data = pd.DataFrame(raw_data[1:])
            data.columns = raw_data[0]
        else:
            data = raw_data
        label_data = data[label_column]
        if label_column is not None:
            data = data.drop(columns=[label_column])
        if drop_columns is not None:
            data = data.drop(columns=drop_columns)

        match outcome_type:
            case "binary":
                return binary_classifiers(label_data, data)
            case "multiclass":
                return multiclass_classifiers(label_data, data)
            case "regression":
                return regressions(label_data, data)
            case _:
                return {"error": f"Case {outcome_type} is not supported"}

        # outcome_type: classsifier [binary | multiclass], regression [distribution/etc.]
        # From the tutorial ...
        # logistic regression
        # decision tree
        # random forest
        # gradient boosting
        # k-nearest neighbors
        # support vector machine
        # extra trees (?)
        # adaboost
