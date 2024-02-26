#%%
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import pickle
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import sklearn
print("Ready to Go")
#%%
train_table = pd.read_csv("MDClone_v2.0.csv")
train_table.head()
#%%
#Drop rows that do not contain a value of 1 for bmi 30
filtered_tt = train_table[train_table['bmi30'] == 1]
filtered_tt["bmi30"].head()
#Drop rows that do not have a record initial and final weight 
filtered_tt = filtered_tt[filtered_tt['wt']> 0]
filtered_tt = filtered_tt[filtered_tt['resulting_wt']> 0]
filtered_tt['resulting_wt'].head()
# %%
#Create new column named "wt_red" that contains percent decrease in weight for each patient
filtered_tt["wt_red"] = ((filtered_tt['wt'] - filtered_tt['resulting_wt'])/filtered_tt['wt'])*100
filtered_tt["wt_red"].head()
# %%
#Function that creates a new column that contains "R" for responders and "N" for non-responders 
def response_status (value): 
    if value >= 5:
        return "R"
    else:
        return "N"
filtered_tt['response'] = filtered_tt["wt_red"].apply(response_status)
# %%
#Drop the "resulting_wt" and "wt_red" columns
filtered_tt = filtered_tt.drop(["resulting_wt", "wt_red"], axis=1)
#%%
#merge "protein_loinc" and "protein_key" for "protein" output 
def handle_missing(protein_key, protein_loinc):
    if not pd.isnull(protein_key) and not pd.isnull(protein_loinc):
        return protein_key
    elif not pd.isnull(protein_key):
        return protein_key
    elif not pd.isnull(protein_loinc):
        return protein_loinc
    else:
        return np.nan
filtered_tt['protein'] = filtered_tt.apply(lambda row: handle_missing(row['protein_key'], row['protein_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["protein_loinc","protein_key"], axis=1)
#%%
#merge "platelet_loinc" and "platelet_key" for "platelet" output 
def handle_missing(platelet_key, platelet_loinc):
    if not pd.isnull(platelet_key) and not pd.isnull(platelet_loinc):
        return platelet_key
    elif not pd.isnull(platelet_key):
        return platelet_key
    elif not pd.isnull(platelet_loinc):
        return platelet_loinc
    else:
        return np.nan
filtered_tt['platelet'] = filtered_tt.apply(lambda row: handle_missing(row['platelet_key'], row['platelet_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["platelet_loinc","platelet_key"], axis=1)
# %%
#merge "sodium_loinc" and "sodium_key" for "sodium" output 
def handle_missing(sodium_key, sodium_loinc):
    if not pd.isnull(sodium_key) and not pd.isnull(sodium_loinc):
        return sodium_key
    elif not pd.isnull(sodium_key):
        return sodium_key
    elif not pd.isnull(sodium_loinc):
        return sodium_loinc
    else:
        return np.nan
filtered_tt['sodium'] = filtered_tt.apply(lambda row: handle_missing(row['sodium_key'], row['sodium_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["sodium_loinc","sodium_key"], axis=1)
# %%
#merge "potassium_loinc" and "potassium_key" for "potassium" output 
def handle_missing(potassium_key, potassium_loinc):
    if not pd.isnull(potassium_key) and not pd.isnull(potassium_loinc):
        return potassium_key
    elif not pd.isnull(potassium_key):
        return potassium_key
    elif not pd.isnull(potassium_loinc):
        return potassium_loinc
    else:
        return np.nan
filtered_tt['potassium'] = filtered_tt.apply(lambda row: handle_missing(row['potassium_key'], row['potassium_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["potassium_loinc","potassium_key"], axis=1)
#%%
#merge "fast_glucose_loinc" and "fast_glucose_key" for "fast_glucose" output 
def handle_missing(fast_glucose_key, fast_glucose_loinc):
    if not pd.isnull(fast_glucose_key) and not pd.isnull(fast_glucose_loinc):
        return fast_glucose_key
    elif not pd.isnull(fast_glucose_key):
        return fast_glucose_key
    elif not pd.isnull(fast_glucose_loinc):
        return fast_glucose_loinc
    else:
        return np.nan
filtered_tt['fast_glucose'] = filtered_tt.apply(lambda row: handle_missing(row['fast_glucose_key'], row['fast_glucose_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["fast_glucose_loinc","fast_glucose_key"], axis=1)
# %%
#merge "ldl_loinc" and "ldl_key" for "ldl" output 
def handle_missing(ldl_key, ldl_loinc):
    if not pd.isnull(ldl_key) and not pd.isnull(ldl_loinc):
        return ldl_key
    elif not pd.isnull(ldl_key):
        return ldl_key
    elif not pd.isnull(ldl_loinc):
        return ldl_loinc
    else:
        return np.nan
filtered_tt['ldl'] = filtered_tt.apply(lambda row: handle_missing(row['ldl_key'], row['ldl_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["ldl_loinc","ldl_key"], axis=1)
#%%
#merge "hdl_loinc" and "hdl_key" for "hdl" output 
def handle_missing(hdl_key, hdl_loinc):
    if not pd.isnull(hdl_key) and not pd.isnull(hdl_loinc):
        return hdl_key
    elif not pd.isnull(hdl_key):
        return hdl_key
    elif not pd.isnull(hdl_loinc):
        return hdl_loinc
    else:
        return np.nan
filtered_tt['hdl'] = filtered_tt.apply(lambda row: handle_missing(row['hdl_key'], row['hdl_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["hdl_loinc","hdl_key"], axis=1)
#%%
#merge "triglycerides_loinc" and "triglycerides_key" for "triglycerides" output 
def handle_missing(triglycerides_key, triglycerides_loinc):
    if not pd.isnull(triglycerides_key) and not pd.isnull(triglycerides_loinc):
        return triglycerides_key
    elif not pd.isnull(triglycerides_key):
        return triglycerides_key
    elif not pd.isnull(triglycerides_loinc):
        return triglycerides_loinc
    else:
        return np.nan
filtered_tt['triglycerides'] = filtered_tt.apply(lambda row: handle_missing(row['triglycerides_key'], row['triglycerides_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["triglycerides_loinc","triglycerides_key"], axis=1)
# %%
#merge "hematocrit_loinc" and "hematocrit_key" for "hematocrit" output 
def handle_missing(hematocrit_key, hematocrit_loinc):
    if not pd.isnull(hematocrit_key) and not pd.isnull(hematocrit_loinc):
        return hematocrit_key
    elif not pd.isnull(hematocrit_key):
        return hematocrit_key
    elif not pd.isnull(hematocrit_loinc):
        return hematocrit_loinc
    else:
        return np.nan
filtered_tt['hematocrit'] = filtered_tt.apply(lambda row: handle_missing(row['hematocrit_key'], row['hematocrit_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["hematocrit_loinc","hematocrit_key"], axis=1)
#%%
#merge "bun_loinc" and "bun_key" for "bun" output 
def handle_missing(bun_key, bun_loinc):
    if not pd.isnull(bun_key) and not pd.isnull(bun_loinc):
        return bun_key
    elif not pd.isnull(bun_key):
        return bun_key
    elif not pd.isnull(bun_loinc):
        return bun_loinc
    else:
        return np.nan
filtered_tt['bun'] = filtered_tt.apply(lambda row: handle_missing(row['bun_key'], row['bun_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["bun_loinc","bun_key"], axis=1)
#%%
#merge "calcium_loinc" and "calcium_key" for "calcium" output 
def handle_missing(calcium_key, calcium_loinc):
    if not pd.isnull(calcium_key) and not pd.isnull(calcium_loinc):
        return calcium_key
    elif not pd.isnull(calcium_key):
        return calcium_key
    elif not pd.isnull(calcium_loinc):
        return calcium_loinc
    else:
        return np.nan
filtered_tt['calcium'] = filtered_tt.apply(lambda row: handle_missing(row['calcium_key'], row['calcium_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["calcium_loinc","calcium_key"], axis=1)
# %%
#merge "co2_loinc" and "co2_key" for "co2" output 
def handle_missing(co2_key, co2_loinc):
    if not pd.isnull(co2_key) and not pd.isnull(co2_loinc):
        return co2_key
    elif not pd.isnull(co2_key):
        return co2_key
    elif not pd.isnull(co2_loinc):
        return co2_loinc
    else:
        return np.nan
filtered_tt['co2'] = filtered_tt.apply(lambda row: handle_missing(row['co2_key'], row['co2_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["co2_loinc","co2_key"], axis=1)
# %%
#merge "chloride_loinc" and "chloride_key" for "chloride" output 
def handle_missing(chloride_key, chloride_loinc):
    if not pd.isnull(chloride_key) and not pd.isnull(chloride_loinc):
        return chloride_key
    elif not pd.isnull(chloride_key):
        return chloride_key
    elif not pd.isnull(chloride_loinc):
        return chloride_loinc
    else:
        return np.nan
filtered_tt['chloride'] = filtered_tt.apply(lambda row: handle_missing(row['chloride_key'], row['chloride_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["chloride_loinc","chloride_key"], axis=1)
#%%
#merge "creatinine_loinc" and "creatinine_key" for "creatinine" output 
def handle_missing(creatinine_key, creatinine_loinc):
    if not pd.isnull(creatinine_key) and not pd.isnull(creatinine_loinc):
        return creatinine_key
    elif not pd.isnull(creatinine_key):
        return creatinine_key
    elif not pd.isnull(creatinine_loinc):
        return creatinine_loinc
    else:
        return np.nan
filtered_tt['creatinine'] = filtered_tt.apply(lambda row: handle_missing(row['creatinine_key'], row['creatinine_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["creatinine_loinc","creatinine_key"], axis=1)
#%%
#merge "chol_total_loinc" and "chol_total_key" for "chol_total" output 
def handle_missing(chol_total_key, chol_total_loinc):
    if not pd.isnull(chol_total_key) and not pd.isnull(chol_total_loinc):
        return chol_total_key
    elif not pd.isnull(chol_total_key):
        return chol_total_key
    elif not pd.isnull(chol_total_loinc):
        return chol_total_loinc
    else:
        return np.nan
filtered_tt['chol_total'] = filtered_tt.apply(lambda row: handle_missing(row['chol_total_key'], row['chol_total_loinc']), axis=1)
filtered_tt = filtered_tt.drop(["chol_total_loinc","chol_total_key"], axis=1)
#%%
#clean table - numeric values for ethnicity.  
def numeriethnicity (row):
    ordinalethnicity = row ["ethnicity"]
    if ordinalethnicity == "Not Hispanic or Latino": return 0
    if ordinalethnicity == "Hispanic or Latino": return 1
    if ordinalethnicity == "Unknown by patient": return np.nan
    if ordinalethnicity == "nan": return np.nan
    if ordinalethnicity == "Declined to answer": return np.nan
    if ordinalethnicity == "censored": return np.nan
    return ordinalethnicity
filtered_tt["ethnicity"] = filtered_tt.apply(numeriethnicity, axis=1)
#%%
#clean table - numeric values for race 
def numerirace (row): 
    ordinalrace = row ["race"]
    if ordinalrace == "Black or African American": return 0
    if ordinalrace == "White": return 1
    if ordinalrace == "White not of Hispanic origin": return 1
    if ordinalrace == "White  ;  White not of Hispanic origin": return 1
    if ordinalrace == "Native Hawaiian or other Pacific Islander": return 2
    if ordinalrace == "Black or African American  ;  White": return 3 
    if ordinalrace == "Asian": return 2
    if ordinalrace == "Asian  ;  Native Hawaiian or other Pacific Islander": return 2
    if ordinalrace == "Native Hawaiian or other Pacific Islander  ;  White": return 4 
    if ordinalrace == "American Indian or Alaska Native  ;  White": return 5
    if ordinalrace == "American Indian or Alaska Native  ;  Black or African American": return 6
    if ordinalrace == "Black or African American  ;  Native Hawaiian or other Pacific Islander": return 7
    if ordinalrace == "Asian  ;  White": return 8
    if ordinalrace == "Asian  ;  Black or African American": return 9
    if ordinalrace == "American Indian or Alaska Native": return 10
    if ordinalrace == "nan": return np.nan
    if ordinalrace == "Declined to answer": return np.nan
    if ordinalrace == "Declined to answer  ;  White": return np.nan
    if ordinalrace == "Unknown by patient": return np.nan
    if ordinalrace == "Unknown by patient  ;  White": return np.nan
    if ordinalrace == "Black or African American  ;  Unknown by patient": return np.nan
    if ordinalrace == "Declined to answer  ;  White not of Hispanic origin": return np.nan
    if ordinalrace == "Black or African American  ;  Declined to answer": return np.nan
    if ordinalrace == "censored": return np.nan
    return ordinalrace
filtered_tt["race"] = filtered_tt.apply(numerirace, axis=1)
# %%
#clean table - numeric value for gender 
def numericgender (row):
    ordinalgender = row["gender"]
    if ordinalgender == "Male": return 0
    if ordinalgender == "Female": return 1
    if ordinalgender == "censored": return np.nan
    return ordinalgender
filtered_tt["gender"] = filtered_tt.apply(numericgender, axis =1)
#%%
#Establish X and y variables 
X = filtered_tt.drop(["response","smoke"], axis=1)
y = filtered_tt["response"]
print("Table Ready to Go")
#%%
#Fill missing values with mean
imputer = SimpleImputer(strategy='mean')  
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
#%%
#Train test split
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.25 ,random_state=123)
print("Ready to Go")
#%%
#Train Decision Tree Classifier 
DTC = DecisionTreeClassifier() 
DTC.fit(X_train, y_train)
print(f'DTC train score: {DTC.score(X_train,y_train)}')
print(f'DTC test score:  {DTC.score(X_test,y_test)}')
print(confusion_matrix(y_test, DTC.predict(X_test)))
print(classification_report(y_test, DTC.predict(X_test)))
#%%
#Train Random Forest Classifier - Just to view performance metrics 
RF = RandomForestClassifier() 
RF.fit(X_train, y_train)
print(f'RF train score: {RF.score(X_train,y_train)}')
print(f'RF test score:  {RF.score(X_test,y_test)}')
print(confusion_matrix(y_test, RF.predict(X_test)))
print(classification_report(y_test, RF.predict(X_test)))
# %%
#Convert RF into pickle 
with open("mdclone2.0_RF.pickle", "wb") as fp:
    pickle.dump(RF, fp)
fp.close()
#%%
#Make a prediction using RF
with open("mdclone2.0_RF.pickle", "rb") as fp:
    RF = pickle.load(fp)
fp.close()

# Make predictions from a single patient's data
sample = pd.read_csv("MDClone_unknown1.csv")
sample = sample.drop(["response"], axis=1)
prediction = RF.predict(sample)
print(f"Prediction based on metagenomic profile: {prediction}")