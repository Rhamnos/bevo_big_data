import os

import pandas as pd
from matplotlib import pyplot as plt

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)

# Create two csv's with column index and label for both datasets
OUTPATH_ACCIDENTS_COLUMNS = os.path.join("eda", "accidents_columns.csv")
OUTPATH_OPERATIONS_COLUMNS = os.path.join("eda", "operations_columns.csv")

pd.Series(df_accidents.columns).to_csv(OUTPATH_ACCIDENTS_COLUMNS)
pd.Series(df_operations.columns).to_csv(OUTPATH_OPERATIONS_COLUMNS)


def check_repeats(data, column):
    """
    Function used to identify columns with duplicate values
    Returns the total amount of values for the given column that are reported more than once.
    """
    return (data[column].value_counts() > 1).sum()


unique_railroad = (df_operations["Reporting Parent Railroad Name"]
                   .dropna()
                   .str.strip()
                   .unique()
)
unique_railroad_accident = (df_accidents["Reporting Railroad Name"]
                            .dropna()
                            .str.strip()
                            .unique()
)

a = set(unique_railroad)   
b = set(unique_railroad_accident)

in_both = a & b      
only_in_a = a - b      
only_in_b = b - a      

print(len(in_both), len(only_in_a), len(only_in_b))

print(only_in_b)


# def merge_dat(data1, data2):
#     accidents = df_accidents["Reporting Parent Railroad Code"]