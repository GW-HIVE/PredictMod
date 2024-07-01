"""
File:           diabetes_predict.py
Author:         Karina Martinez
Version:        1.0
Description:    The script loads the pre-trained classifier from the diabetes_classifier.pkl file, 
                reads an input file with plasma protein N-glycome levels, and outputs whether the patient 
                is predicted to develop type 2 diabetes or remain normoglycaemic within 10 years.

                This script accepts a filename argument:
                Usage: diabetes_predict.py [options] 

                Options:
                    -h, --help                      show this help message and exit    
                    -f FILENAME, --file=FILENAME    example input csv file [default: example_input.csv]
"""

import joblib
import pandas as pd
from optparse import OptionParser

def preprocess_data(df):
    # Add GlyTouCan (https://glytoucan.org/) accessions to glycan peak (GP) headers
    headers = pd.read_csv("gtc_headers.csv", sep=",")
    header_list = headers["Header"].to_list()
    df.columns=header_list

    # Combine features with same structure
    glycan_dict = {
        "GP32-33_G67579EM":["GP32_G67579EM","GP33_G67579EM"],
        "GP38-39_G12638YK":["GP38_G12638YK","GP39_G12638YK"],
        "GP41-43_G16933RK":["GP41_G16933RK","GP42_G16933RK","GP43_G16933RK"]
               }
    
    # Create dataframe with combined features
    df_combined = pd.DataFrame()
    for key,value in glycan_dict.items():
        df_combined[key] = df[value].sum(axis=1)

    # Join combined features with original dataframe, drop individual peaks included in combined features
    df_out = df.join(df_combined)
    df_out = df_out.drop(columns=["GP32_G67579EM","GP33_G67579EM","GP38_G12638YK","GP39_G12638YK","GP41_G16933RK","GP42_G16933RK","GP43_G16933RK"])
    
    return df_out


###############################

def main():

    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)
    parser.add_option("-f","--filename",action="store",dest="filename",default="example_input.csv",help="example input csv file [default: %default]")
    (options,args) = parser.parse_args()

    filename = options.filename

    # Open the pickle file
    model = joblib.load("diabetes_classifier.pkl")

    # Get example input data
    input_file = pd.read_csv(filename, sep=",")
    processed_df = preprocess_data(input_file)

    pred = model.predict(processed_df)

    outcome = "Type 2 diabetes" if pred == 1 else "Normoglycaemic"
        
    print(f"Prediction based on plasma protein N-glycome: {outcome}")


if __name__ == "__main__":
    main()