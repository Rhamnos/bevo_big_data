import os
import pandas as pd

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)



def clean_accidents(data):
    """
    Cleans the accidents data set by filtering to specific columns, years, and accident types.
    Final output is a dataframe with total accidents by cause code by company by year.
    """
    parents_7 = ["BNSF", "UP", "NS", "CSX", "CPKC", "CN", "NJTR"]
    all_parents = data["Reporting Parent Railroad Code"].str.strip()

    df_filter_col = data[["Year", "Reporting Parent Railroad Code", "Accident Number", "Accident Type", "Primary Accident Cause Code"]]
    df_filter_year = df_filter_col.loc[df_filter_col["Year"] <= 2022]
    df_filter_year["Primary Accident Cause Code"] = df_filter_year["Primary Accident Cause Code"].str.strip().str[0]
    df_drop_dups = df_filter_year.drop_duplicates(subset=["Accident Number"]).copy()
    df_filter_derailments = df_drop_dups.loc[df_drop_dups["Accident Type"].str.strip() == "Derailment"].copy()
    df_filter_derailments["Reporting Parent Railroad Code"] = all_parents.where(all_parents.isin(parents_7), "other")
    df_drop_col = df_filter_derailments.drop(columns=["Accident Number", "Accident Type"])
    df_drop_col["Primary Accident Cause Code"] = df_drop_col["Primary Accident Cause Code"].replace({"S": "M"})
    df_accidents_clean = (df_drop_col
              .groupby(["Year", "Reporting Parent Railroad Code", "Primary Accident Cause Code"], as_index=False)
              .size()
              .rename(columns={"size": "derailments"})
              )
    return df_accidents_clean


def clean_operations(data):
    """
    Cleans the operations dataset, filters the parent companies to the top 7 
    with the largest operation volume and every other company is aggregated into "other".
    Final output is total train miles by company by year.
    """
    parents = ["BNSF", "UP", "NS", "CSX", "CPKC", "CN", "NJTR"]
    df_filter_columns = data[["Year", "Railroadcode", "Reporting Parent Railroad Code", "Total Train Miles"]].copy()
    all_parents = df_filter_columns["Reporting Parent Railroad Code"].str.strip()
    df_filter_columns["Reporting Parent Railroad Code"] = all_parents.where(all_parents.isin(parents), "other")
    df_filter_columns["Total Train Miles"] = pd.to_numeric(df_filter_columns["Total Train Miles"].str.replace(",", ""))
    df_operations_clean = (df_filter_columns
              .groupby(["Year", "Reporting Parent Railroad Code"], as_index = False)["Total Train Miles"]
              .sum()
              )
    return df_operations_clean


def merge_dfs(accidents, operations):
    """
    Merges the two cleaned dataframes on year and reporting parent railroad code
    Creates column that gives the total derailments by cause per million miles of operation within a given year.
    Returns dataframe organized by rate per million miles by cause group by company by year.
    """
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
    """
    Changes the names of the merged data set to snake case
    """
    df_final = data.rename(columns={
        "Year": "year",
        "Reporting Parent Railroad Code": "railroad_group",
        "Primary Accident Cause Code": "cause_group",
        "Total Train Miles": "total_miles",
    })
    return df_final


def clean_and_merge(accidents, operations):
    """
    Combines the functions above into one function that cleans and merges the two datasets
    Returns dataframe organized by rate per million miles by cause group by company by year.
    """
    accidents_cleaned = clean_accidents(accidents)
    operations_cleaned = clean_operations(operations)
    merged_data = merge_dfs(accidents_cleaned, operations_cleaned)
    final_df = change_names(merged_data)
    return final_df

clean = clean_and_merge(df_accidents, df_operations)