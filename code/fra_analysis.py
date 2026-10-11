import os
import pandas as pd

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

OUT_PATH = "artifacts"
os.makedirs(OUT_PATH, exist_ok = True)

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS, low_memory=False)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)

#Converts the year column to numbers
def filter_years(df):
    #creates a copy so the original dataset stays unchanged
    df = df.copy()
    df["Year"] = pd.to_numeric(df["Year"], errors = "coerce")

    return df[df["Year"].between(2014,2022)]

df_accidents_cleaned = filter_years(df_accidents)
df_operations_cleaned = filter_years(df_operations)

df_accidents_cleaned.to_csv(
    os.path.join(OUT_PATH, "accidents_cleaned_csv"),
    index = False)

df_operations_cleaned.to_csv(
    os.path.join(OUT_PATH, "accidents_cleaned_csv"),
    index = False)



    
