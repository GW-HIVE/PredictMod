import numpy as np
import pandas as pd
import sklearn as skl
import time

from .models import (
    PCAHandler,
    DecisionTreeClassifierHandler,
    LogisticRegressionHandler,
    RandomForestClassifierHandler,
    SupportVectorMachineHandler,
)


def regressions(label_data, data):

    pca = PCAHandler(label_data, data)
    pca.train_model()


def binary_classifiers(label_data, data):

    results = []

    pca = PCAHandler(label_data, data)
    results.append(pca.train_model())

    label_data = label_data.apply(lambda x: 0 if x == "R" else 1)

    print("---> LR")
    lr = LogisticRegressionHandler(label_data, data)
    results.append(lr.train_model())

    print("---> DTC")
    dtc = DecisionTreeClassifierHandler(label_data, data)
    results.append(dtc.train_model())

    print("---> RFC")
    rfc = RandomForestClassifierHandler(label_data, data)
    results.append(rfc.train_model())

    print("---> SVM")
    svm = SupportVectorMachineHandler(label_data, data)
    results.append(svm.train_model())

    print("VVV BINARY CLASSIFIER VVV")
    for idx, r in enumerate(results):
        print(f"Result {idx+1}: {r}")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^")


def multiclass_classifiers(label_data, data):

    pca = PCAHandler(label_data, data)
    pca.train_model()


class Pipeline:
    def __init__(self):
        pass

    def train_models(self, raw_data, label_column, outcome_type="binary"):

        print(f"===> Automated Pipeline - Got a request! <===")

        if not isinstance(raw_data, pd.DataFrame):
            headers, data = raw_data[0], np.array([raw_data[1]])
            data = pd.DataFrame(data, columns=headers)
        else:
            data = raw_data

        label_data = data[label_column]
        data = data.drop(columns=[label_column])

        # Hack hack hack
        data = data.drop(columns=["Reference"])

        match outcome_type:
            case "binary":
                binary_classifiers(label_data, data)
            case "multiclass":
                multiclass_classifiers(label_data, data)
            case "regression":
                regressions(label_data, data)
            case _:
                raise NotImplementedError

        # outcome_type: classsifier [binary | multiclass], regression [distribution/etc.]

        # logistic regression

        # decision tree

        # random forest

        # gradient boosting

        # k-nearest neighbors

        # support vector machine

        # extra trees (?)

        # adaboost

        start = time.time()

        return {"result": f"Prediction achieved!!"}
