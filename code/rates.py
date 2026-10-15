import pandas as pd


def calculate_period_rates(data, start_year, end_year):
    """Calculate overall and per-cause derailment rates for a range of years."""

    period_data = data.loc[data["year"] >= start_year].copy()
    period_data = period_data.loc[period_data["year"] <= end_year].copy()

    cause_groups = period_data.groupby(
        ["railroad_group", "cause_group"], as_index=False
    )
    total_derailments = cause_groups["derailments"].sum()

    railroad_totals = period_data.groupby("railroad_group", as_index=False)[
        "derailments"
    ].sum()
    railroad_totals["cause_group"] = "Total"
    total_derailments = pd.concat(
        [total_derailments, railroad_totals], ignore_index=True
    )

    yearly_miles = period_data.drop_duplicates(subset=["railroad_group", "year"])
    railroad_groups = yearly_miles.groupby("railroad_group", as_index=False)
    total_miles = railroad_groups["total_miles"].sum()

    rates = total_derailments.merge(total_miles, on="railroad_group")
    rates["rate_per_million_miles"] = (
        rates["derailments"] / rates["total_miles"] * 1000000
    )

    return rates
