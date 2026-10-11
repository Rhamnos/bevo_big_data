import os
import pandas as pd

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

OUT_PATH = "artifacts"
os.makedirs(OUT_PATH, exist_ok = True)

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS, low_memory=False)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)
