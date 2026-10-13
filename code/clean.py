import os
import pandas as pd

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)



def clean_accidents(data):
    """
    Function cleans the accidents data set.
    1. Filters down to the necessary columns and removes data past 2022
    2. Changes the accident cause code to the single identifier (M,S,E,T,H)
    3. Drop the duplicate accident reports
    4. Filter the accident type to only derailments
    5. Filter the parent companies to the top 7, all other companies are in other
    6. Drop Columns that the final output does not need
    7. Combine the M and S cause codes together by changing all Ss into Ms
    8. Last step is to organize by year -> by company -> by primary accident cause code
    """
    parents = ["BNSF", "UP", "NS", "CSX", "CPKC", "CN", "NJTR"]
    clean1 = data[["Year", "Reporting Parent Railroad Code", "Accident Number", "Accident Type", "Primary Accident Cause Code"]]
    clean1 = clean1.loc[clean1["Year"] <= 2022]
    clean1["Primary Accident Cause Code"] = clean1["Primary Accident Cause Code"].str.strip().str[0]
    clean2 = clean1.drop_duplicates(subset=["Accident Number"]).copy()
    clean2 = clean2.loc[clean2["Accident Type"].str.strip() == "Derailment"].copy()
    all_parents = clean2["Reporting Parent Railroad Code"].str.strip()
    clean2["Reporting Parent Railroad Code"] = all_parents.where(all_parents.isin(parents), "other")
    clean3 = clean2.drop(columns=["Accident Number", "Accident Type"])
    clean3["Primary Accident Cause Code"] = clean3["Primary Accident Cause Code"].replace({"S": "M"})
    clean3 = (clean3
              .groupby(["Year", "Reporting Parent Railroad Code", "Primary Accident Cause Code"], as_index=False)
              .size()
              .rename(columns={"size": "derailments"})
              )
    return clean3


def clean_operations(data):
    """
    Function cleans the operations dataset
    1. Filters down to necessary columns
    2. Filter the parent companies to the top 7, all other companies are in other
    3. Change total train miles to numeric value
    4. Organiz and aggregate data by year -> by parent company code -> by total train miles
    """
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

    return merged[["Year", "Reporting Parent Railroad Code", 
                   "Primary Accident Cause Code", "derailments", 
                   "Total Train Miles", "rate_per_million_miles"]]


def change_names(data):
    df_final = data.rename(columns={
        "Year": "year",
        "Reporting Parent Railroad Code": "railroad_group",
        "Primary Accident Cause Code": "cause_group",
        "Total Train Miles": "total_miles",
    })
    return df_final


def clean_and_merge(accidents, operations):
    accidents_cleaned = clean_accidents(accidents)
    operations_cleaned = clean_operations(operations)
    merged_data = merge_dfs(accidents_cleaned, operations_cleaned)
    final_df = change_names(merged_data)
    return final_df
