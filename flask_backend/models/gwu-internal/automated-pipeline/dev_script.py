import pandas as pd

# from pipeline import Pipeline

# target_file = "../../MG_Exercise_v1.1/cleaned_literature_mg_v1.1.csv"


# with open(target_file, "r") as fp:
#     data = pd.read_csv(fp)

# # print(data)

# pl = Pipeline()

# label_column = "Status"
# drop_columns = [
#     "Reference",
# ]
# response = pl.train_models(data, label_column, drop_columns, outcome_type="binary")

# print(f"Got response:\n{response}")

from pipeline.models import (
    PCAHandler,
    DecisionTreeClassifierHandler,
    LogisticRegressionHandler,
    RandomForestClassifierHandler,
    SupportVectorMachineHandler,
)

training_file = "../../MG_Exercise_v1.1/cleaned_literature_mg_v1.1.csv"
sample_file = "../../MG_Exercise_v1.1/unknown_response.csv"

label_column = "Status"
drop_columns = [
    "Reference",
]

with open(training_file, "r") as fp:
    data = pd.read_csv(fp)
data = data.drop(columns=drop_columns)
labels = data[label_column]
data = data.drop(columns=[label_column])

with open(sample_file, "r") as fp:
    new_sample = pd.read_csv(fp)
new_sample = new_sample.drop(columns=[label_column])

# PCA direct
pca = PCAHandler(labels, data)
results = pca.train_model()

new_results = pca.sample_prediction(new_sample)

labels = labels.apply(lambda x: 0 if x == "R" else 1)

# Decision Tree
dtc = DecisionTreeClassifierHandler(labels, data)
results = dtc.train_model()
new_results = dtc.sample_prediction(new_sample)
print(f"{'-'*20}{'DTC':^40}{'-'*20}")
print(new_results)
print("-" * 80)

# Logisitic Regression
lrc = LogisticRegressionHandler(labels, data)
results = lrc.train_model()
new_results = lrc.sample_prediction(new_sample)
print(f"{'-'*20}{'LRC':^40}{'-'*20}")
print(new_results)
print("-" * 80)

# Random Forest
rfc = RandomForestClassifierHandler(labels, data)
results = rfc.train_model()
new_results = rfc.sample_prediction(new_sample)
print(f"{'-'*20}{'RFC':^40}{'-'*20}")
print(new_results)
print("-" * 80)

# SVM
svmc = SupportVectorMachineHandler(labels, data)
results = svmc.train_model()
new_results = svmc.sample_prediction(new_sample)
print(f"{'-'*20}{'SVMC':^40}{'-'*20}")
print(new_results)
print("-" * 80)
