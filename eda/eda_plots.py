import os 
import pandas as pd
from matplotlib import pyplot as plt

IN_PATH = os.path.join("data", "rail_accident.csv")
OUT_DIR = "data"
OUT_PATH = os.path.join(OUT_DIR, "county.csv")

# theme = load_theme("arctic_dark")
# theme.apply()

df = pd.read_csv(IN_PATH)



texas_df = ( 
    df.loc[df["State Abbreviation"] == "TX"]
    .groupby(["Year", "Accident Month", "County Name"], as_index=False)["Train Speed"]
    .mean()
)

texas_year_df = (
    df.loc[df["State Abbreviation"] == "TX"]
    .groupby(["Year", "County Name"], as_index=False)["Train Speed"]
    .mean()            
)

monthly = (
    df.groupby(["Year", "Accident Month"])
    .size()
    .reset_index(name="collisions")
)

monthly["date"] = pd.to_datetime(dict(year=monthly["Year"], month=monthly["Accident Month"], day=1))
monthly = (monthly.set_index("date").sort_index())


# plot = monthly["collisions"].plot(
#     xlabel="Date",
#     ylabel="Collisions per month",
#     title="Collisions per month over time",
#     figsize=(10,7),
# )
# plot.set_title("Collisions per month over time", fontsize=20)
# theme.apply_transforms()
# plt.savefig("collisions.png")


visibility_df = df.groupby("Visibility").size()

# vis_plot = visibility_df.plot(
#     kind="bar", 
#     xlabel="Visibility Condition",
#     ylabel="Total Accidents",
#     title="Breakdown of Accidents by Visibility Condition",
#     rot=0,
#     fontsize=12,
#     figsize=(10,6.5),
#     )

# vis_plot.set_title("Breakdown of Accidents by Visbility Condition", fontsize=20)
# theme.apply_transforms()
# plt.savefig("visibility.png")


state_df = df.groupby("State Abbreviation").size()

state_plot = state_df.plot(
    kind="bar",
    xlabel= "State",
    ylabel="Total Accidents",
    title="Breakdown of Accidents by State",
    fontsize=10,
)
theme.apply_transforms()
plt.savefig("state_accidents.png")



collision_df = df.groupby("Accident Type").size()
# print(collision_df)
# collision_plot = collision_df.plot(
#     kind="bar",
#     xlabel= "Collision Type",
#     ylabel="Total Collisions",
#     title="Breakdown of Accidents by Type",
#     fontsize=7,
#     rot=30,
# )

# plt.savefig("accidents_type.png")
