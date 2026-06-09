import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="GDP Dashboard",
    page_icon="🌍",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_gdp_data(path: str = "data/gdp_data.csv") -> pd.DataFrame:
    """Load the GDP dataset and reshape it into a long format for plotting."""
    df = pd.read_csv(path)
    year_columns = [column for column in df.columns if column.isdigit()]

    long_df = df[["Country Name", *year_columns]].copy()
    long_df = long_df.melt(
        id_vars=["Country Name"],
        value_vars=year_columns,
        var_name="Year",
        value_name="GDP",
    )
    long_df["Year"] = pd.to_numeric(long_df["Year"], errors="coerce")
    long_df["GDP"] = pd.to_numeric(long_df["GDP"], errors="coerce")

    return long_df.dropna(subset=["Year", "GDP"]).sort_values(["Country Name", "Year"]).reset_index(drop=True)


st.title(":earth_americas: GDP dashboard")
st.caption("Explore GDP trends for selected countries from the World Bank dataset in this repository.")

all_data = load_gdp_data()
all_countries = sorted(all_data["Country Name"].unique())
selected_countries = st.multiselect(
    "Select countries to compare",
    options=all_countries,
    default=["United States", "China", "India"],
)

if not selected_countries:
    st.info("Select at least one country to display the GDP trend chart.")
    st.stop()

filtered_df = all_data[all_data["Country Name"].isin(selected_countries)]

fig = px.line(
    filtered_df,
    x="Year",
    y="GDP",
    color="Country Name",
    markers=True,
    title="GDP (current US$) over time",
)
fig.update_yaxes(title="GDP (current US$)")
fig.update_xaxes(title="Year")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Selected data")
st.dataframe(
    filtered_df.pivot(index="Year", columns="Country Name", values="GDP").sort_index(),
    use_container_width=True,
)
