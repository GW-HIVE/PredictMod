# Import necessary libraries
import pandas as pd
import numpy as np

# Read patient EHR data, patient diagnosis, and target variables to observe

obs = pd.read_excel('observe_.xlsx')
patients = pd.read_excel('patients_xl.xlsx')
refs = pd.read_excel('var_list_.xlsx')

#Iterate through all patient records and find unique patients and their diagnosis

Unique_patients = (patients["PATIENT"].unique()) #find unique patients within dataset
prediabetes_patients = [] #account for prediabetes then nothing, or diabetes to prediabetes
diabetes_patients = [] #account for first prediabetes diagnosis, then diabetes, or just diabetes
counter = 0
for i in Unique_patients:
  current_patient = i #captures each unique patient within the dataset
  current_patient_list = []
  for j in patients.iterrows():
    if j[1][1] == i:
      current_patient_list.append([i,j[1][2]])
  sorted_list = sorted(current_patient_list, key=lambda x: x[0])
  if sorted_list[-1][1].strip().lower() == 'diabetes':
    #print(sorted_list[-1][1] + " IS THE SAME AS DIABETES: so appened to diabetes")
    diabetes_patients.append(i)
  else:
    prediabetes_patients.append(i)
pre = np.zeros((len(prediabetes_patients),))
de = np.ones((len(diabetes_patients),))
label = np.append(pre,de)
all_patient_tags = prediabetes_patients + diabetes_patients

#Iterate through unique patient identifiers and find variables associated with that patient

row_select = [0, 1, 2, 4, 5, 6, 7]
ehr_list = refs.iloc[row_select, 2]
input_data = np.zeros((len(all_patient_tags),len(ehr_list)))
patient_row_index = 0
for current_patient in all_patient_tags:
  var_col_index = 0
  print("Current Patient: " + str(patient_row_index))
  patient_rows = obs[obs['PATIENT'].str.contains(current_patient)]
  patient_ind = np.array(patient_rows.index)
  for ehr_var in ehr_list:
    ehr_rows = obs[obs['DESCRIPTION'].str.contains(ehr_var)]
    ehr_ind = np.array(ehr_rows.index)
    common_rows = np.intersect1d(patient_ind, ehr_ind)
    if common_rows.shape == np.zeros(0).shape:
      input_data[patient_row_index,var_col_index] = np.nan #if no intersection, then don't add data? or make data 0
    else:
      specific_rows = obs.loc[common_rows]
      dat_to_append = specific_rows.iloc[-1,5] #last measurment since it's sorted by epoch, and 5 col is actual value
      input_data[patient_row_index,var_col_index] = dat_to_append
    var_col_index += 1
  patient_row_index += 1
#pain severity, diastolic, systolic, calcium, sodium, potassium, chloride, body weight (UPPER PART WORKS)

#Process to check if there are any NANs per column: Turn this into a function perhaps later

print(type(input_data))
print(input_data.shape[1])
for i in range(1,input_data.shape[1]):
  count = 0
  for j in range(1,input_data.shape[0]):
    if np.isnan(input_data[j-1, i-1]):
      count += 1
  print("Column: "+ str(i) + " contains: " + str(count) + " NANs")

#Saving current inputs to work with GAN model

df = pd.DataFrame(input_data)
df2 = pd.DataFrame(label)
## save to xlsx file
filepath = 'data.xlsx'
df.to_excel(filepath, index=False)
filepath_l = 'label.xlsx'
df2.to_excel(filepath_l, index=False)