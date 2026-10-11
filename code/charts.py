
import pandas as pd
import matplotlib.pyplot as plt



def charts_over_time(df, output_path):
    """take in a pandas data frame [railroad_group, year, rate_per_million_miles].
    Return a chart of the derailments per railroad over time to the 
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


    ax.set_title("Derailments per million miles by railroad")
    ax.set_xlabel("Year")
    ax.set_ylabel("Derailments per million miles")
    ax.legend()

    fig.savefig(output_path, dpi=150, bbox_inches="tight")

    plt.close(fig)


    return

def charts_by_cause(df):
    """take in a pandas data frame. Return a chart of the derailments per railroad by cause"""


