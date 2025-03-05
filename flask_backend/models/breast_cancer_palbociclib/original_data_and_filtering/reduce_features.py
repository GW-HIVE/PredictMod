import pandas as pd
from sklearn.feature_selection import VarianceThreshold

def reduce_features(file_path,file_output_name):
    df = pd.read_csv(file_path, index_col=0)

    # Assuming the last column contains labels (0/1 for patient responsiveness)
    #labels = df.iloc[:, -1]  # Extract labels
    features = df.iloc[1:, 1:]  # Extract gene expression data

    # Compute variance for each gene (row)
    row_variances = features.var(axis=1)

    # Select top 100 rows with highest variance
    top_100_rows = row_variances.nlargest(100).index

    # Keep only the top 100 rows
    reduced_df = features.loc[top_100_rows]

    # Add back patient labels
    #reduced_df["Response"] = labels.loc[top_100_rows]

    # Save to CSV
    reduced_df.to_csv(file_output_name, index=True)

# Load dataset
reduce_features(file_path = "filtered_C0D0.csv",file_output_name="filtered_C0D0_reduced.csv")
reduce_features(file_path = "filtered_C1D1.csv",file_output_name="filtered_C1D1_reduced.csv")
reduce_features(file_path = "filtered_C1D15.csv",file_output_name="filtered_C1D15_reduced.csv")