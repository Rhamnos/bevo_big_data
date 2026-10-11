import os
import pandas as pd

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)


def check_mismatch(data):
    mismatches = data[data["Railroadcode"] != data["Reporting Parent Railroad Code"]]
    return mismatches


def map_company_to_parent():
    pass


def top_seven_accidents(data):
    parents = ["BNSF", "UP", "NS", "CSX", "CPKC", "CN", "NJTR"]
    clean1 = data[["Year", "Reporting Railroad Code", "Reporting Parent Railroad Code", "Accident Number", "Accident Type", "Primary Accident Cause Code"]]
    clean1 = clean1.loc[clean1["Year"] <= 2022]
    clean1["Primary Accident Cause Code"] = clean1["Primary Accident Cause Code"].str.strip().str[0]
    clean2 = clean1.drop_duplicates(subset=["Accident Number"])
    clean3 = clean2.loc[clean2["Reporting Parent Railroad Code"].isin(parents)]
    return clean3


def top_seven_operations(data):
    parents = ["BNSF", "UP", "NS", "CSX", "CPKC", "CN", "NJTR"]
    clean1 = data[["Year", "Railroadcode", "Reporting Parent Railroad Code", "Total Train Miles"]].copy()
    clean1["Reporting Parent Railroad Code"] = (clean1["Reporting Parent Railroad Code"].str.strip())
    clean2 = clean1.loc[clean1["Reporting Parent Railroad Code"].isin(parents)]
    return clean2


# def merge_data(data1, data2):






clean1 = top_seven_accidents(df_accidents)
clean2 = top_seven_operations(df_operations)
print(clean1)
print(clean2)


# clean = clean_operations(df_operations)
# print(len(clean))
# operation_match = check_mismatch(clean)
# print(len(operation_match))