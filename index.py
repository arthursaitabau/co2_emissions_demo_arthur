import pandas as pd
import numpy as np
import plotly.express as px
from itables import show
import country_converter as coco

# Define table_df
emissions = pd.read_csv("data/co2_cons.csv")
for col in ["2021", "2022"]:
    has_k = emissions[col].str.contains("k")
    values = emissions[col].str.replace("k", "")
    emissions[col] = np.where(has_k, values.astype(float) * 1000, values.astype(float))
table_df = emissions[["country", "2000", "2022"]].copy()
table_df["Absolute Change"] = table_df["2022"] - table_df["2000"]
table_df["Relative Change"] = (table_df["Absolute Change"] / table_df["2000"]) * 100
table_df["Relative Change"] = table_df["Relative Change"].round(0).astype(str) + "%"

# Define fig_chart
emissions_long = emissions.melt(
    id_vars="country", var_name="year", value_name="emissions"
)
emissions_long["year"] = pd.to_numeric(emissions_long["year"], errors="coerce")
emissions_long["emissions"] = pd.to_numeric(
    emissions_long["emissions"], errors="coerce"
)
emissions_long_1990_2022 = emissions_long.query("1990 <= year <= 2022")
countries_of_interest = ["Kenya", "Malaysia", "France", "Brazil", "Australia"]
emissions_long_1990_2022 = emissions_long_1990_2022[
    emissions_long_1990_2022["country"].isin(countries_of_interest)
]
fig_chart = px.line(
    emissions_long_1990_2022,
    x="year",
    y="emissions",
    color="country",
    title="CO2 Emissions (1990-2022)",
)

# Define fig_map
emissions_long_1990_2022["country_code"] = coco.convert(
    emissions_long_1990_2022["country"], to="ISO3"
)
fig_map = px.choropleth(
    emissions_long_1990_2022,
    locations="country_code",
    color="emissions",
    hover_name="country",
    animation_frame="year",
    title="Global CO2 Emissions (1990-2022)",
)
