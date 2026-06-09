import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Global Temperature Dashboard',
    page_icon='🌡️',
)


@st.cache_data(ttl='1d')
def get_temperature_data():
    """Load the Berkeley Earth monthly global temperature anomaly dataset."""
    url = 'https://storage.googleapis.com/berkeley-earth-temperature-hr/global/Global_TAVG_monthly.txt'
    columns = [
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years would you like to view?',
    min_value=min_year,
    max_value=max_year,
    value=[min_year, max_year],
)

filtered_df = temperature_df[
    (temperature_df['Year'] >= from_year)
    & (temperature_df['Year'] <= to_year)
].sort_values('Date')

fig = px.line(
    filtered_df,
    x='Date',
    y='Monthly_Anomaly',
    labels={
        'Date': 'Month',
        'Monthly_Anomaly': 'Temperature anomaly (°C)',
    },
    title='Monthly global temperature anomaly',
)

st.plotly_chart(fig, use_container_width=True)

latest = filtered_df.tail(1)
average = filtered_df['Monthly_Anomaly'].mean()

col1, col2 = st.columns(2)
col1.metric('Latest monthly anomaly', f"{latest['Monthly_Anomaly'].iloc[0]:.2f} °C")
col2.metric('Average anomaly in selected range', f"{average:.2f} °C")
