import os
import pandas as pd

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)



def clean_accidents(data):
    parents = ["BNSF", "UP", "NS", "CSX", "CPKC", "CN", "NJTR"]
    clean1 = data[["Year", "Reporting Parent Railroad Code", "Accident Number", "Accident Type", "Primary Accident Cause Code"]]
    clean1 = clean1.loc[clean1["Year"] <= 2022]
    clean1["Primary Accident Cause Code"] = clean1["Primary Accident Cause Code"].str.strip().str[0]
    clean2 = clean1.drop_duplicates(subset=["Accident Number"]).copy()
    clean2 = clean2.loc[clean2["Accident Type"].str.strip() == "Derailment"].copy()
    all_parents = clean2["Reporting Parent Railroad Code"].str.strip()
    clean2["Reporting Parent Railroad Code"] = all_parents.where(all_parents.isin(parents), "other")
    clean3 = clean2.drop(columns=["Accident Number", "Accident Type"])
    clean3 = (clean3
              .groupby(["Year", "Reporting Parent Railroad Code", "Primary Accident Cause Code"], as_index=False)
              .size()
              .rename(columns={"size": "derailments"})
              )
    # clean3 = clean3.reset_index(drop=True)
    return clean3


def clean_operations(data):
    parents = ["BNSF", "UP", "NS", "CSX", "CPKC", "CN", "NJTR"]
    clean1 = data[["Year", "Railroadcode", "Reporting Parent Railroad Code", "Total Train Miles"]].copy()
    all_parents = clean1["Reporting Parent Railroad Code"].str.strip()
    clean1["Reporting Parent Railroad Code"] = all_parents.where(all_parents.isin(parents), "other")
    clean1["Total Train Miles"] = pd.to_numeric(clean1["Total Train Miles"].str.replace(",", ""))
    clean2 = (clean1
              .groupby(["Year", "Reporting Parent Railroad Code"], as_index = False)["Total Train Miles"]
              .sum()
              )
    return clean2

def merge_dfs(accidents, operations):
    merged = accidents.merge(
        operations,
        how="left",
        on=["Year", "Reporting Parent Railroad Code"],
    )
    merged["rate_per_million_miles"] = (merged["derailments"] / merged["Total Train Miles"] * 1000000)

    return merged[["Year", "Reporting Parent Railroad Code", "Primary Accident Cause Code", "derailments", "Total Train Miles", "rate_per_million_miles"]]


df_rates = merge_dfs(clean_accidents(df_accidents), clean_operations(df_operations))

def change_names(data):
    df_final = data.rename(columns={
        "Year": "year",
        "Reporting Parent Railroad Code": "railroad_ group",
        "Primary Accident Cause Code": "cause_group",
        "Total Train Miles": "total_miles",
    })
    return df_final


names = change_names(df_rates)
print(names)







# def merge_data(data1, data2):

# def final_clean_accidents(data):
#     rename = data.rename(columns={"Year": "year", 
#                                   "Reporting Parent Railroad Code": "railroad_group", 
#                                   "Accident Type": "derailment", "Primary Accident Cause Code": "cause_group"})
#     final_clean = rename
#     return final_clean





# clean1 = top_seven_accidents(df_accidents)
# clean2 = top_seven_operations(df_operations)
# print(clean1)
# print(clean2)


# clean = clean_operations(df_operations)
# print(len(clean))
# operation_match = check_mismatch(clean)
# print(len(operation_match))