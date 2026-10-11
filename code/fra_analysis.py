import os
import pandas as pd

# Load the FRA datasets
IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")

# Create the artifacts folder
OUT_PATH = "artifacts"
os.makedirs(OUT_PATH, exist_ok=True)

df_accidents = pd.read_csv(IN_PATH_ACCIDENTS, low_memory=False)
df_operations = pd.read_csv(IN_PATH_OPERATIONS)


# Filter datasets to years 2014–2022
def filter_years(df):
    df = df.copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    return df[df["Year"].between(2014, 2022)]


# Remove duplicate records
def remove_duplicates(data, column):
    """
    Removes duplicate records based on the specified column.
    """
    df_cleaned = data.drop_duplicates(subset=column)
    return df_cleaned


# Filter both datasets
df_accidents_cleaned = filter_years(df_accidents)
df_operations_cleaned = filter_years(df_operations)

# Remove identical rows from the filtered accident data
df_accidents_cleaned = df_accidents_cleaned.drop_duplicates()


# Save cleaned datasets to artifacts
df_accidents_cleaned.to_csv(
    os.path.join(OUT_PATH, "accidents_cleaned.csv"),
    index=False
)

df_operations_cleaned.to_csv(
    os.path.join(OUT_PATH, "operations_cleaned.csv"),
    index=False
)
    
