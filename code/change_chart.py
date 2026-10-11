import matplotlib.pyplot as plt


def plot_change_chart(change_table, output_path):
    """Save percentage changes by railroad and cause as a chart."""
    fig, ax = plt.subplots(figsize=(12, 6))
    change_table.plot(kind="bar", ax=ax)
    ax.set_title("Change in derailment rates: 2014–2016 to 2020–2022")
    ax.set_xlabel("Railroad company")
    ax.set_ylabel("Change in derailment rate (%)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.legend(title="Cause")
    ax.tick_params(axis="x", labelrotation=45)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

