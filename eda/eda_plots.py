import os 
import pandas as pd
from matplotlib import pyplot as plt

IN_PATH_ACCIDENTS = os.path.join("data", "Rail_Equipment_Accident_Incident_Data_(Form_54)_20261008.csv")
IN_PATH_OPERATIONS = os.path.join("data", "Operational Data_Full Data_data_Use_This.csv")


df = pd.read_csv(IN_PATH_ACCIDENTS)


monthly = (
    df.groupby(["Year", "Accident Month"])
    .size()
    .reset_index(name="accidents")
)

monthly["date"] = pd.to_datetime(dict(year=monthly["Year"], month=monthly["Accident Month"], day=1))
monthly = (monthly.set_index("date").sort_index())


plot = monthly["accidents"].plot(
    xlabel="Date",
    ylabel="Accidents per month",
    title="Accidents per month over time",
    figsize=(10,7),
)
plot.set_title("Accidents per month over time", fontsize=20)
plt.savefig("eda/eda_artifacts/accidents.png")


visibility_df = df.groupby("Visibility").size()

vis_plot = visibility_df.plot(
    kind="bar", 
    xlabel="Visibility Condition",
    ylabel="Total Accidents",
    title="Breakdown of Accidents by Visibility Condition",
    rot=0,
    fontsize=12,
    figsize=(10,6.5),
    )

vis_plot.set_title("Breakdown of Accidents by Visibility Condition", fontsize=18)
plt.savefig("eda/eda_artifacts/visibility.png")



# collision_df = df.groupby("Accident Type").size()
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
