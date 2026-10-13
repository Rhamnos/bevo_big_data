import os
from clean import clean_and_merge, df_accidents, df_operations
from rates import calculate_period_rates
from change_chart import plot_change_chart


data = clean_and_merge(df_accidents, df_operations)
early_rates = calculate_period_rates(data, 2014, 2016)
late_rates = calculate_period_rates(data, 2020, 2022)

early_table = early_rates.pivot(index="railroad_group", columns="cause_group", values="rate_per_million_miles")
late_table = late_rates.pivot(index="railroad_group", columns="cause_group", values="rate_per_million_miles")
causes = ["E", "H", "M", "T"]
early_table = early_table.reindex(columns=causes).fillna(0)
late_table = late_table.reindex(columns=causes).fillna(0)
early_denominator = early_table.replace(0, float("nan"))
change_table = (late_table - early_table) / early_denominator * 100

cause_names = {"E": "Equipment", "H": "Human factors", "M": "Misc. + signal", "T": "Track"}
change_table = change_table.rename(columns=cause_names, index={"other": "Other"})

# Select each railroad's overall totals for the two rows below the chart.
early_totals = early_rates.loc[early_rates["cause_group"] == "Total"].copy()
late_totals = late_rates.loc[late_rates["cause_group"] == "Total"].copy()
early_totals = early_totals.set_index("railroad_group")
late_totals = late_totals.set_index("railroad_group")
early_totals = early_totals.rename(index={"other": "Other"})
late_totals = late_totals.rename(index={"other": "Other"})

os.makedirs("artifacts", exist_ok=True)
change_table.to_csv("artifacts/change_rates.csv")
plot_change_chart(change_table, "artifacts/change_chart_preview.png", early_totals, late_totals)
print(change_table.round(2).to_string())
print("Saved chart to artifacts/change_chart_preview.png.")

if change_table.isna().any().any():
    print("N/A values have a zero or unavailable early-period rate, so their percentage change is undefined.")
