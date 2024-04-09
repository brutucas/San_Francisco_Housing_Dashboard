import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Import the necessary CSVs to Pandas DataFrames
avg_gross_rent = pd.read_csv('Data/avg_gross_rent_csv.csv')
avg_housing = pd.read_csv('Data/avg_housing_csv.csv')
avg_sale_price = pd.read_csv('Data/avg_sale_price_csv.csv')
neighborhood_coords = pd.read_csv('Data/neighborhoods_coordinates.csv')
sfo_data = pd.read_csv('Data/sfo_neighborhoods_census_data.csv', index_col='year')

'''
## San Francisco Housing Cost Analysis

To visualise the San Francisco Housing Cost data, I did the following:
- copied (and checked) the plotting code for each visualization;
- wrapped these plots in separate functions to be compatible with Streamlit;
- included code to ensure that each function returns the plot object for dashboard integration;
- removed .show() commands to prevent plots from appearing outside the dashboard context;
- ensured that plots were displayed correctly within the Streamlit dashboard;
- ran (and re-ran) the dashboard using the command `streamlit run 'dashboard.py'.
'''

# Define Visualization Functions
def housing_units_per_year():
    "Housing Units Per Year."
    avg_housing_units = sfo_data.groupby('year')['housing_units'].mean()
    avg_housing_units = pd.DataFrame(avg_housing_units).reset_index()
    min_housing_units = avg_housing_units['housing_units'].min()
    max_housing_units = avg_housing_units['housing_units'].max()
    std_housing_units = avg_housing_units['housing_units'].std()
    fig = plt.figure(figsize=(10, 5))
    avg_housing_units.plot.bar(x='year', y='housing_units', title='Average Housing Units in San Francisco from 2010-2016', xlabel='Year', ylabel='Avg Housing Units', legend=False, ax=plt.gca())
    plt.ylim(min_housing_units - std_housing_units, max_housing_units + std_housing_units)
    return fig

def average_gross_rent():
    """Average Gross Rent in San Francisco Per Year."""
    avg_gross_rent = sfo_data.groupby('year')['gross_rent'].mean()
    avg_gross_rent_df = pd.DataFrame(avg_gross_rent).reset_index()
    fig = px.line(avg_gross_rent_df, x='year', y='gross_rent', title='Average Gross Rent in San Francisco Per Year')
    fig.update_layout(xaxis_title='Year', yaxis_title='Gross Rent')
    return fig
def average_sales_price():
    """Average Sales Price Per Year."""
    avg_sale_price = sfo_data.groupby('year')['sale_price_sqr_foot'].mean()
    avg_sale_price_df = pd.DataFrame(avg_sale_price).reset_index()
    fig = px.line(avg_sale_price_df, x='year', y='sale_price_sqr_foot', title='Average Sale Price Per Square Foot in San Francisco Per Year')
    fig.update_layout(xaxis_title='Year', yaxis_title='Avg. Sale Price per Square Foot')
    return fig

def average_price_by_neighborhood(neighborhood):
    """Average Prices by Neighborhood."""
    df_prices = sfo_data[sfo_data['neighborhood'] == neighborhood]   
    df_prices['sale_price_sqr_foot'] = pd.to_numeric(df_prices['sale_price_sqr_foot'], errors='coerce') # Convert 'sale_price_sqr_foot' to a numeric type, ignore errors to avoid conversion issues
    df_prices = df_prices.dropna(subset=['sale_price_sqr_foot']) # Drop rows with NaN values in 'sale_price_sqr_foot' after conversion
    df_avg_prices = df_prices.groupby('year')['sale_price_sqr_foot'].mean() # Group by 'year' and calculate mean, ensuring 'sale_price_sqr_foot' is now numeric
    df_avg_prices = pd.DataFrame(df_avg_prices).reset_index()
    fig = px.line(df_avg_prices, x='year', y='sale_price_sqr_foot', title=f'Average Prices by Neighborhood: {neighborhood}')
    fig.update_layout(xaxis_title='Year', yaxis_title='Avg. Sale Price per Square Foot')
    return fig

def top_most_expensive_neighborhoods():
    """Top 10 Most Expensive Neighborhoods."""
    avg_neighborhood_price = sfo_data.groupby('neighborhood')['sale_price_sqr_foot'].mean()
    avg_neighborhood_df = pd.to_numeric(avg_neighborhood_price, errors='coerce')
    avg_neighborhood_df = pd.DataFrame(avg_neighborhood_price).reset_index()
    top_10_exp_neighborhoods = avg_neighborhood_df.sort_values(by='sale_price_sqr_foot', ascending=False).head(10)
    top_10_bar = px.bar(top_10_exp_neighborhoods, x='neighborhood', y='sale_price_sqr_foot', title='Top 10 Most Expensive Neighborhoods in San Francisco')
    top_10_bar.update_layout(xaxis_title='San Francisco Neighborhood', yaxis_title='Sale Price per Square Foot')
    return top_10_bar

def most_expensive_neighborhoods_rent_sales(selected_neighborhood):
    """Comparison of Rent and Sales Prices of Most Expensive Neighborhoods."""   
    df_costs = sfo_data[sfo_data['neighborhood'] == selected_neighborhood]
    df_costs_bar = px.bar(df_costs, x=df_costs.index, 
                          y=['sale_price_sqr_foot', 'gross_rent'], 
                          title='Comparison of Sale Price per Square Foot and Gross Rent',
                          labels={"value": "USD", "variable": "Metrics"},
                          barmode='group')
    return df_costs_bar

def neighborhood_map():
    """Neighborhood Map."""
    neighborhood_avg = sfo_data.groupby(by='neighborhood').mean().reset_index()
    neighborhood_avg.rename(columns={'neighborhood': 'Neighborhood', 'gross_rent': 'Gross Rent'}, inplace=True)
    neighborhood_map_data = pd.merge(neighborhood_avg, neighborhood_coords, on='Neighborhood')
    sfo_map = px.scatter_mapbox(neighborhood_map_data, lat='Lat', lon='Lon', 
                            size='sale_price_sqr_foot', color='Gross Rent',
                            zoom=11, height=600, hover_data=['Neighborhood'])
    sfo_map.update_layout(mapbox_style="carto-positron")
    return sfo_map

# Most expensive neighbourhoods in San Francisco by year
df_costs = sfo_data.groupby([sfo_data.index, "neighborhood"]).mean()
df_costs.reset_index(inplace=True)
df_costs.rename(columns={"level_0": "year"}, inplace=True)

df_expensive_neighborhoods = sfo_data.groupby(by="neighborhood").mean()
df_expensive_neighborhoods = df_expensive_neighborhoods.sort_values(by="sale_price_sqr_foot", ascending=False).head(10)
df_expensive_neighborhoods = df_expensive_neighborhoods.reset_index()

df_expensive_neighborhoods_per_year = df_costs[df_costs["neighborhood"].isin(df_expensive_neighborhoods["neighborhood"])]

def sunburst():
    """Sunburst Plot."""
    fig = px.sunburst(df_expensive_neighborhoods_per_year, 
                path=['year', 'neighborhood'], 
                values='sale_price_sqr_foot', 
                color='gross_rent', height=600, 
                title="Cost Analysis of Most Expensive Neighborhoods in San Francisco")
    return fig

# Start Streamlit App
st.pyplot(housing_units_per_year())

st.plotly_chart(average_gross_rent())
st.plotly_chart(average_sales_price())

st.plotly_chart(average_price_by_neighborhood('Bayview'))
st.plotly_chart(average_price_by_neighborhood("Alamo Square"))
st.plotly_chart(average_price_by_neighborhood('Central Richmond'))

st.plotly_chart(top_most_expensive_neighborhoods())

st.plotly_chart(most_expensive_neighborhoods_rent_sales('Bayview'))
st.plotly_chart(most_expensive_neighborhoods_rent_sales('Alamo Square'))
st.plotly_chart(most_expensive_neighborhoods_rent_sales('Central Richmond'))

st.plotly_chart(sunburst())