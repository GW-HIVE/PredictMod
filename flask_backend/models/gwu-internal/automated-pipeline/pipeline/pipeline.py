import numpy as np
import pandas as pd
import sklearn as skl
import time

from sklearn.linear_model import LogisticRegression


def regressions(data): ...


def binary_classifiers(data): ...


def multiclass_classifiers(data): ...


class Pipeline:
    def __init__(self):
        pass

    def train_models(self, outcome_type, raw_data):

        print(f"===> Automated Pipeline - Got a request! <===")

        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)

        match outcome_type:
            case "binary":
                binary_classifiers(df)
            case "multiclass":
                multiclass_classifiers(df)
            case "regression":
                regressions(df)
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

        return {
            "result": f"Prediction based on tumor N-glycoproteomic profile: {outcome}"
        }
