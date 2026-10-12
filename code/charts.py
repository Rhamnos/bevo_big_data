import matplotlib.pyplot as plt



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
