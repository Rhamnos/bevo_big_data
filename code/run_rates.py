import os
import pandas as pd
from clean import clean_and_merge, df_accidents, df_operations
from rates import calculate_period_rates


data = clean_and_merge(df_accidents, df_operations)
os.makedirs("artifacts/rates", exist_ok=True)

yearly_tables = []

for year in range(2014, 2023):
    yearly_rates = calculate_period_rates(data, year, year)
    yearly_rates["year"] = year
    yearly_tables.append(yearly_rates)

annual_rates = pd.concat(yearly_tables, ignore_index=True)

early_rates = calculate_period_rates(data, 2014, 2016)
late_rates = calculate_period_rates(data, 2020, 2022)
full_period_rates = calculate_period_rates(data, 2014, 2022)

annual_rates.to_csv("artifacts/rates/annual_rates.csv", index=False)
early_rates.to_csv("artifacts/rates/rates_2014_2016.csv", index=False)
late_rates.to_csv("artifacts/rates/rates_2020_2022.csv", index=False)
full_period_rates.to_csv("artifacts/rates/rates_2014_2022.csv", index=False)

print("Saved four rate tables in artifacts/rates.")
