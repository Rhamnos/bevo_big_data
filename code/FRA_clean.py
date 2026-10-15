import os
import pandas as pd

from clean import clean_and_merge
from charts import charts_over_time, charts_by_cause, plot_change_chart

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IN_PATH_ACCIDENTS = os.path.join(
    PROJECT_ROOT, "data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv"
)

IN_PATH_OPERATIONS = os.path.join(
    PROJECT_ROOT, "data", "Operational Data_Full Data_data_Use_This.csv"
)

OUTPUT_PATH = os.path.join(PROJECT_ROOT, "artifacts")

CHART_TIME_PATH = os.path.join(OUTPUT_PATH, "derailments_over_time.png")

CHART_CAUSE_PATH = os.path.join(OUTPUT_PATH, "derailments_by_cause.png")

CHART_CHANGE_PATH = os.path.join(OUTPUT_PATH, "changes_between_periods.png")


def main():
    """Takes in nothing and outputs nothing. Completes analysis on
    defined files and outputs graphs and cleaned data to defined path"""

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    df_accidents = pd.read_csv(IN_PATH_ACCIDENTS)
    df_operations = pd.read_csv(IN_PATH_OPERATIONS)

    cleaned_data = clean_and_merge(df_accidents, df_operations)

    cleaned_data.to_csv(os.path.join(OUTPUT_PATH, "cleaned_data.csv"), index=False)

    charts_over_time(cleaned_data, CHART_TIME_PATH)
    charts_by_cause(cleaned_data, CHART_CAUSE_PATH)
    plot_change_chart(cleaned_data, CHART_CHANGE_PATH)


if __name__ == "__main__":
    main()
