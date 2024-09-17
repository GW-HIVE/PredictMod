"""
File:           ccrcc_predict.py
Author:         Karina Martinez
Version:        1.1
Description:    The script loads the pre-trained classifier from the ccrcc_classifier.pkl file, 
                reads an input file with 10814 clear cell renal cell carcinoma tumor glycoproteomic
                abundances, and outputs whether the patient is predicted have high or low risk
                of death or disease progression within 5 years from tumor resection.

                This script accepts a filename argument:
                Usage: ccrcc_predict.py [options] 

                Options:
                    -h, --help                      show this help message and exit    
                    -f FILENAME, --file=FILENAME    example input csv file [default: example_input.csv]
"""

# fmt: off
import joblib
import pandas as pd
from optparse import OptionParser

def get_glycoforms(glycoform_df):
    """
    Helper function to display gene, glycosylation site, sequence, and glycan composition in header.
    """
    site_dict = {}

    for i in glycoform_df.columns:
        row = i.split("_")
        gene, pep_start, sequence, gly_site, glycan = row[0], int(row[1]), row[2], int(row[4]), row[5]
        glycosylation_site = pep_start + gly_site - 1
    
        glycosite = gene + "_" + str(glycosylation_site) + "_" + glycan

        if glycosite not in site_dict:
            site_dict[glycosite] = [i]

        else:
            site_dict[glycosite].append(i)

    df_dict = {}

    for key,value in site_dict.items():
        df_dict[key] = glycoform_df[value].sum(axis=1)


    return pd.DataFrame(df_dict)


###############################

def main():

    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)
    parser.add_option("-f","--filename",action="store",dest="filename",default="example_input.csv",help="example input csv file [default: %default]")
    (options,args) = parser.parse_args()

    filename = options.filename

    # Open the pickle file
    model = joblib.load("ccrcc_classifier.pkl")

    # Get example input data
    input_file = pd.read_csv(filename, sep=",")
    processed_df = get_glycoforms(input_file)

    pred = model.predict(processed_df)

    outcome = "Low risk" if pred == 1 else "High risk"
        
    print(f"Prediction based on tumor N-glycoproteomic profile: {outcome}")


if __name__ == "__main__":
    main()
# fmt: on
