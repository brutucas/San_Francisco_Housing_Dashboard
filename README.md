# San Francisco Real Estate Dashboard

![San Francisco Park Reading](Images/san-francisco.jpg)


## Background

My company has recently launched a Real Estate Investment division, and my supervisor needs  help developing a prototype dashboard for San Francisco investment opportunities. The dashboard I am going to build will use charts, maps, and visualizations to help customers decide if they want to invest in rental properties.

1. I have already been provided data on rental properties in San Francisco that includes census data and geographical data.
2. In the initial phase of this project, I will need to clean and organize the data.
3. Following data preparation, I will create charts, maps, and visualizations using Plotly.
4. The final step will be to integrate the visualizations into a user-friendly dashboard with Streamlit.

The dashboard will provide customers with information to make informed investment decisions and find the best investment opportunities.

In this assignment, I am setting out to accomplish the following tasks:
1. [Complete a notebook of rental analysis](#Rental-Analysis).
2. [Create a dashboard of interactive visualizations to explore the market data](#Dashboard).

## San Francisco Housing Costs Analysis 

### Rental Analysis

The first step to building the dashboard was to work out all of the calculations and visualizations in an analysis notebook. Once the code was written out and working in the notebook, I copied it over to a dashboard code and used with Streamlit to create the final layout.

#### Housing Units Per Year

In this section, I calculated the number of housing units per year and visualize the results as a bar chart using the Pandas plot function. The default chart was unclear - the limits made it difficult to see the difference between the yearly data. I opted to use the min, max, and standard deviation of the data to manually scale the y limits of the plot.

#### Average Housing Costs in San Francisco Per Year

In this section, I wanted to determine the average sales price per year and the average gross rent per year to better understand housing costs over time. This would be useful if, for example, a customer wants to know if they should expect an increase or decrease in the property value or rent over time. This will help them to determine how long to hold the rental property. I visualised the average (mean) gross rent and average price per square foot per year using line charts.

#### Average Prices and Gross Rent By Neighborhood

In this section, I created a function named 'average_price_by_neighborhood' to analyze and visualize the housing market trends in specific San Francisco neighborhoods. This function filters housing data for the chosen neighborhood, then it cleans the data, ensuring sale prices are numeric and any missing values are removed. The function also calculates the yearly average sale price per square foot, and finally generates a line plot displaying this trend over time.

I decided to use Plotly Express for visualization, because I wanted customisation and interactivity. I made sure to include {} when the function is called, so that the neighbourhood's name is returned with the plot. I followed these same steps to analyze average gross rent trends.

#### Top 10 Most Expensive Neighborhoods

In this section, I wanted to figure out which neighborhoods are the most expensive. To achieve this, I needed to use the 'groupby' and 'mean' method to calculate the average sale price for each neighborhood. This was one of the more interesting parts of the project, highlighting both overpriced and more reasonably-priced (by SF standards) neighborhoods.

#### Comparing cost to purchase versus rental income

In this section, I defined a function that took a selected neighborhood as input, filtered the data for that neighborhood, created and returned a bar chart (again, using Plotly Express, for the customisation and interactivity). This function returned the plot object, which made it possible to display the plot simply by calling the function with a selected neighborhood - efficient and effective.

During the building of this function, I made sure to specify the x-axis data as the index of the DataFrame, which represents the years in the sfo_data dataframe. I passed two columns ('gross_rent' and 'sale_price_sqr_foot') as a list to the y-axis parameter, and set the title to include the selected neighborhood. By doing so, the plot dynamically reflects the chosen area. I also customised the axis labels, renaming the generic "value" and "variable" to more descriptive labels, and set barmode to 'group' to display the bars side by side for easier data comparison.

#### Neighborhood Map

This section was one of the more difficult but also very rewarding parts of the project. I read in neighborhood location data and built an interactive map with the average rent price per neighborhood. I used a 'scatter_mapbox' from Plotly express to create the interactive visualization, and modified the 'size', 'color', 'color_continuous_scale' and zoom' arguments to make the map more visually-appealing.

### Dashboard

Once I had written out and tested all of the code and analysis, I used the Streamlit library to build an interactive dashboard for all of the visualizations. This required copying the code for each visualization from the analysis notebook and placing it into separate functions (1 function per visualization). This made it easier to build and modify the Streamlit layout. With testing, each function successfully returned the plot figure in a format that Streamlit could use to plot the
visualization. 
