import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def plot_change_chart(change_table, output_path):
    """Save percentage changes by railroad and cause as a chart."""
    colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00"]

    fig, ax = plt.subplots(figsize=(14, 7))

    change_table.plot(
        kind="bar",
        ax=ax,
        color=colors,
        width=0.75,
        edgecolor="white",
    )

    ax.set_title(
        "Change in derailment rates\n2014–2016 compared with 2020–2022",
        fontsize=17,
        fontweight="bold",
        loc="left",
        pad=20,
    )

    ax.set_xlabel("")
    ax.set_ylabel("Percentage change in derailment rate", fontsize=12)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100))

    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#E5E7EB")
    ax.axhline(0, color="#374151", linewidth=1)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.tick_params(axis="x", labelrotation=0, labelsize=11)
    ax.tick_params(axis="y", labelsize=11)

    ax.legend(
        title="Derailment cause",
        frameon=False,
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
