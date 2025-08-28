import pandas as pd
import pickle

# Load the classifier from the pickle file
with open("example_classifier.pkl", "rb") as fp:
    classifier = pickle.load(fp)

# Read the single data point file
try:
    sample_data = pd.read_csv("example_sample_point.csv")
except Exception as e:
    print(f'Error reading the file: {e}')
    exit()

ground_truth = sample_data["Status"]
sample_data.drop(columns=["Status"], inplace=True)

print(f"Making prediction, with ground truth established as '{ground_truth[0]}'")

# Make a prediction
prediction = classifier.predict(sample_data)
print(f"===> Got a prediction: {'R' if prediction == 1 else 'NR'}")
