import os
import pandas as pd

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)


def remove_duplicates(data, column):
    """
    Removes the duplicate accidents from the accident dataset
    """
    df_cleaned = data.drop_duplicates(subset=column)
    return df_cleaned

df_accidents_cleaned = remove_duplicates(df_accidents, "Accident Number")
