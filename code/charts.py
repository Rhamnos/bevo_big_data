import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from rates import calculate_period_rates


def charts_over_time(df, output_path):
    """take in a pandas data frame [railroad_group, year, rate_per_million_miles].
    Return nothing. Plot of the derailments per railroad over time to the 
    specified output path"""
    
    fig, ax = plt.subplots(figsize=(8,5))

    rate_per_year = df.groupby(["railroad_group", "year"])["rate_per_million_miles"].sum()
    rate_per_year = rate_per_year.unstack("railroad_group")
    for railroad in rate_per_year:
        if railroad == "other":
            line_color = "gray"
        else:
            line_color = None
        ax.plot(rate_per_year.index, rate_per_year[railroad], marker = "o", label = railroad, color = line_color)


    ax.set_title("Derailments Per Million Miles by Railroad")
    ax.set_xlabel("Year")
    ax.set_ylabel("Derailments Per Million Miles")
    ax.set_ylim(bottom=0)
    ax.legend(loc = "upper left", bbox_to_anchor = (1.02,1))

    fig.savefig(output_path, dpi=150, bbox_inches="tight")

    plt.close(fig)

    return

def charts_by_cause(df, output_path):
    """take in a pandas data frame [railroad_group, year, cause_group, 
    derailments, total_miles]. Return nothing. Plot a chart of the derailments per railroad by cause"""

    fig, ax = plt.subplots(figsize=(8,5))

    cause_df = df.groupby(["railroad_group", "cause_group"])["derailments"].sum()
    cause_df = cause_df.unstack("railroad_group")
    group_year = df.groupby(["railroad_group","year"])["total_miles"].first()
    group_year = group_year.groupby("railroad_group").sum()
    mile_per_millions = group_year / 1000000
    cause_rate = cause_df/mile_per_millions
    cause_rate = cause_rate.T
    cause_names = {"E": "Electrical/Mechanical", "H": "Human", "M":"Misc.+Signal", "T":"Track"}
    cause_rate = cause_rate.rename(columns = cause_names)
    
    cause_rate.plot(kind = "bar", stacked = True, ax = ax, rot=0)

    ax.set_title("Derailment Rates Per Cause for Each Railroad")
    ax.set_xlabel("Railroads")
    ax.set_ylabel("Derailment per Million Miles")
    ax.set_ylim(bottom=0)
    ax.legend(loc = "upper left", bbox_to_anchor = (1.02,1))

    fig.savefig(output_path, dpi=150, bbox_inches="tight")

    plt.close(fig)

    return


def plot_change_chart(change_table, output_path):
    """Plot rate changes with counts and mileage for both periods."""

    early_rates = calculate_period_rates(change_table, 2014, 2016)
    late_rates = calculate_period_rates(change_table, 2020, 2022)

    early_table = early_rates.pivot(index="railroad_group", columns="cause_group", values="rate_per_million_miles")
    late_table = late_rates.pivot(index="railroad_group", columns="cause_group", values="rate_per_million_miles")
    causes = ["E", "H", "M", "T"]
    early_table = early_table.reindex(columns=causes).fillna(0)
    late_table = late_table.reindex(columns=causes).fillna(0)
    early_denominator = early_table.replace(0, float("nan"))
    change_table = (late_table - early_table) / early_denominator * 100

    cause_names = {"E": "Electrical/Mechanical", "H": "Human factors", "M": "Misc. + signal", "T": "Track"}
    change_table = change_table.rename(columns=cause_names, index={"other": "Other"})

    # Select each railroad's overall totals for the two rows below the chart.
    early_totals = early_rates.loc[early_rates["cause_group"] == "Total"].copy()
    late_totals = late_rates.loc[late_rates["cause_group"] == "Total"].copy()
    early_totals = early_totals.set_index("railroad_group")
    late_totals = late_totals.set_index("railroad_group")
    early_totals = early_totals.rename(index={"other": "Other"})
    late_totals = late_totals.rename(index={"other": "Other"})
    
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.subplots_adjust(left=0.10, right=0.985, bottom=0.305, top=0.75)

    change_table.plot(kind="bar", ax=ax, color=colors, width=0.55, edgecolor="white", linewidth=0.5, legend=False)

    fig.text(0.5425, 0.94, "Change in derailment rates", ha="center", fontsize=24, fontweight="bold", color="#243040")
    fig.text(0.5425, 0.893, "2014–2016 compared with 2020–2022", ha="center", fontsize=15, color="#64748b")
    fig.legend(loc="upper left", bbox_to_anchor=(0.095, 0.862), ncol=4, frameon=False, fontsize=12, handlelength=1.5, columnspacing=2)

    ax.set_xlabel("")
    ax.set_ylabel("Percentage change in derailment rate", fontsize=12, color="#475569", labelpad=14)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#e7ebf0", linewidth=0.8)
    ax.axhline(0, color="#64748b", linewidth=1.1)

    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(False)

    ax.tick_params(axis="x", labelrotation=0, labelsize=12, length=0, pad=13)
    ax.tick_params(axis="y", labelsize=11, length=0, pad=8, colors="#64748b")

    for label in ax.get_xticklabels():
        label.set_fontweight("bold")
        label.set_color("#334155")

    for position in range(len(change_table.index) - 1):
        ax.axvline(position + 0.5, color="#e3e8ef", linewidth=0.8)

    minimum = change_table.min().min()
    maximum = change_table.max().max()
    ax.set_ylim(min(-20, minimum - 20), max(20, maximum + 20))

    # Add each percentage at the end of its bar.
    for cause_number, bars in enumerate(ax.containers):
        for railroad_number, bar in enumerate(bars):
            value = change_table.iloc[railroad_number, cause_number]
            center = bar.get_x() + bar.get_width() / 2

            if pd.isna(value):
                ax.annotate("N/A", xy=(center, 0), xytext=(0, 5), textcoords="offset points", ha="center", va="bottom", fontsize=9, color="#64748b")
            else:
                rounded_value = round(value)
                label = str(rounded_value) + "%"

                if rounded_value > 0:
                    label = "+" + label

                if value >= 0:
                    offset = 5
                    alignment = "bottom"
                else:
                    offset = -5
                    alignment = "top"

                ax.annotate(label, xy=(center, value), xytext=(0, offset), textcoords="offset points", ha="center", va=alignment, fontsize=9, color="#475569")

    # These rows show totals across all causes.
    fig.text(0.5425, 0.231, "2014–2016 → 2020–2022   ·   Totals across all causes for each railroad", ha="center", fontsize=11, color="#64748b")
    fig.text(0.015, 0.164, "Total derailments", fontsize=11, color="#475569")
    fig.text(0.015, 0.120, "Train-miles (millions)", fontsize=10, color="#64748b")

    for position, railroad in enumerate(change_table.index):
        early_count = early_totals.loc[railroad, "derailments"]
        late_count = late_totals.loc[railroad, "derailments"]
        early_miles = early_totals.loc[railroad, "total_miles"] / 1000000
        late_miles = late_totals.loc[railroad, "total_miles"] / 1000000
        count_text = f"{early_count:,.0f} → {late_count:,.0f}"
        miles_text = f"{early_miles:,.1f} → {late_miles:,.1f}"
        ax.text(position, -0.317, count_text, transform=ax.get_xaxis_transform(), ha="center", fontsize=11, color="#334155", clip_on=False)
        ax.text(position, -0.416, miles_text, transform=ax.get_xaxis_transform(), ha="center", fontsize=10, color="#64748b", clip_on=False)

    fig.text(0.10, 0.05, "Source: FRA Form 54 and operational data. Rates use derailments per million train-miles.", fontsize=9, color="#7c8798")

    if change_table.isna().any().any():
        fig.text(0.10, 0.026, "N/A = percentage change is undefined because the early-period rate is zero or unavailable.", fontsize=9, color="#7c8798")

    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)