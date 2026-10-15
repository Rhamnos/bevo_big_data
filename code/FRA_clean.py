
import os
import pandas as pd
import matplotlib.pyplot as plt

from clean import clean_and_merge
from charts import charts_over_time, charts_by_cause

# Step 1: Define project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Step 2: Define input paths
IN_PATH_ACCIDENTS = os.path.join(
    PROJECT_ROOT,
    "data",
    "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv"
)

IN_PATH_OPERATIONS = os.path.join(
    PROJECT_ROOT,
    "data",
    "Operational Data_Full Data_data_Use_This.csv"
)

# Step 3: Define output directory
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "artifacts")

# Define full PNG file paths
CHART_TIME_PATH = os.path.join(
    OUTPUT_PATH, "derailments_over_time.png"
)

CHART_CAUSE_PATH = os.path.join(
    OUTPUT_PATH, "derailments_by_cause.png"
)


def main():

    # Step 4: Create output directory
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Step 5: Load datasets
    df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
    df_operations = pd.read_csv(IN_PATH_OPERATIONS)

    # Step 6: Clean and merge datasets
    cleaned_data = clean_and_merge(
        df_accidents, df_operations
    )

    # Step 7: Save cleaned dataset
    cleaned_data.to_csv(
        os.path.join(OUTPUT_PATH, "cleaned_data.csv"),
        index=False
    )

    # Step 8: Generate and save charts
    charts_over_time(cleaned_data, CHART_TIME_PATH)
    charts_by_cause(cleaned_data, CHART_CAUSE_PATH)


if __name__ == "__main__":
    main()
