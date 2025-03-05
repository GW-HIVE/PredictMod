import pandas as pd
import numpy as np

# Load the CSV file
file_path = "DNA_microarray_data_utf8.csv"  # Update with your actual file path

df = pd.read_csv(file_path, index_col=0, header=0) #first column is gene symbols

# Find column indices containing "BL"
C0D0_columns = [idx for idx, col in enumerate(df.columns) if "BL" in col]
C1D1_columns = [idx for idx, col in enumerate(df.columns) if "C1D1" in col]
b1D15_columns = [idx for idx, col in enumerate(df.columns) if "C1_D15" in col]
# Print the indices
#print("Indices of columns containing 'BL':", bl_columns)

df.iloc[:, C0D0_columns].to_csv("filtered_C0D0.csv", index=True)
df.iloc[:, C1D1_columns].to_csv("filtered_C1D1.csv", index=True)
df.iloc[:, b1D15_columns].to_csv("filtered_C1D15.csv", index=True)
