
import os
import pandas as pd
import matplotlib.pyplot as plt

from clean import clean_and_merge
from charts import charts_over_time, charts_by_cause

# Step 1: Define input and output paths
IN_PATH_ACCIDENTS = os.path.join(
    "data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv"
)

IN_PATH_OPERATIONS = os.path.join(
    "data", "Operational Data_Full Data_data_Use_This.csv"
)

OUTPUT_PATH = "artifacts"


def main():

    # Step 2: Create output directory
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Step 3: Load datasets
    df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
    df_operations = pd.read_csv(IN_PATH_OPERATIONS)

    # Step 4: Clean and merge datasets
    cleaned_data = clean_and_merge(df_accidents, df_operations)

    # Step 5: Save cleaned dataset
    cleaned_data.to_csv(
        os.path.join(OUTPUT_PATH, "cleaned_data.csv"),
        index=False
    )

    # Step 6: Generate and save charts
    charts_over_time(cleaned_data, OUTPUT_PATH)
    charts_by_cause(cleaned_data, OUTPUT_PATH)


if __name__ == "__main__":
    main()
