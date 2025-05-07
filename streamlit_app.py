"""
Class: CS 230 - 2
Name: Claudia Sweeney
Date: 5/8/2025
Data: Nuclear Explosions
URL:
Description:
This program analyzes the nuclear explosions across the globe before the year 2000. It begins by discussing so summary
data about the explosions. It them has a interactive MAp where uses can select what area of the world they want to look.
Finally, in the char section the users can use interactive features to build a table showcasing hoe many explosions
there were for different countries during certain years. They also can examine a bar char that highlights the different
explosion methods used and a pie chart of the different deployment countries
"""

#importing all necessary modules
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image


#reading the data from the csv into a panda
file_path = "C:\\Users\\crswe\\OneDrive - Bentley University\\Spring 2025\\CS 230\\nuclear_explosions.csv"
nuclear  = pd.read_csv(file_path)

#updating the column names of latitude and longitude so they can be read by the map
nuclear.rename(columns={"Location.Cordinates.Latitude":"lat", "Location.Cordinates.Longitude": "lon"}, inplace= True)

#Combining the date columns into a string [DA7] Add/drop/select/create new/group column
#uses the .astype() method: used https://www.geeksforgeeks.org/how-to-convert-pandas-columns-to-string/ for a how-to
nuclear['Date'] = (nuclear['Date.Month'].astype(str) + '-' + nuclear['Date.Day'].astype(str) +
                   '-' +nuclear['Date.Year'].astype(str))

#Averging the lower and upper yield [DA9] Add a new column or perform calculations on DataFrame columns
nuclear["Yield Average"] = (nuclear['Data.Yeild.Lower'] + nuclear['Data.Yeild.Upper'])/2

#Replacing the Nan in the name to say unnamed # [DA1] clean/manipulate data
nuclear.loc[nuclear["Data.Name"] == "Nan","Data.Name"] = "unnamed"

#Reading the database into a dictionary [PY5] dictionary where you write code to accesses it keys,values or items

# Initialize an empty dictionary to hold value counts for each column
column_value_counts = {}

# Loop through each column in the nuclear DF
for col in nuclear.columns:
    # Use value_counts() to count unique values in the column
    # documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.value_counts.html
    value_counts = nuclear[col].value_counts()

    # Convert the result to a dictionary
    #documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
    value_counts_dict = value_counts.to_dict()

    # Add this dictionary to the main dictionary, using the column name as the key
    column_value_counts[col] = value_counts_dict

#function to create a map  [PY1] a function with two or more parameters, with a default
def exp_map(lat, long, user_zoom = 7):

    #setting the view state based on lat and long
    view_state = pdk.ViewState(
        latitude= lat,
        longitude= long,
        zoom= user_zoom,
        pitch=0)

    #creating the first layer
    layer1 = pdk.Layer(type='ScatterplotLayer',
                       data=nuclear,
                       get_position='[lon, lat]',
                       get_radius=1000,
                       get_color=[255, 255, 0],
                       pickable=True
                       )

    #creating the second layer
    layer2 = pdk.Layer('ScatterplotLayer',
                       data=nuclear,
                       get_position='[lon, lat]',
                       get_radius=500,
                       get_color=[255, 165, 0],
                       pickable=True
                       )

    #creating a tool tip with info about the explosion
    tool_tip = {
        "html": "Explosion Name:<br/><b>{Data.Name}</b><br/>Date:<br/><b>{Date}</b><br/>Average Yield:<br/><b>{Yield Average}</b>",
        "style": {"backgroundColor": "red", "color": "white"}
    }

    # Create a map based on the view, layers, and tool tip [MAP] detailed map
    my_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v12',
        initial_view_state=view_state,
        layers=[layer1, layer2],
        tooltip= tool_tip#
    )

    #outputting the map
    st.pydeck_chart(my_map)

#function to create a data frame based on a requirements
def filter_explosions_by_year_range_and_country(start_year, end_year, country):
    #[DA5] Filter data by two or more conditions
    #ducomentation for use of the is in function - found on https://www.geeksforgeeks.org/how-to-check-if-pandas-column-has-value-from-list-of-string/
     df =  nuclear[(nuclear["Date.Year"] >= start_year) & (nuclear["Date.Year"] <= end_year)
            & (nuclear["WEAPON SOURCE COUNTRY"].isin(country))][['WEAPON SOURCE COUNTRY',
            'WEAPON DEPLOYMENT LOCATION', 'Data.Name', 'Date','Yield Average']]
     return df

#function to get dictionary key and values for a certain column [PY2] a function that returns more than one value
def get_keys_and_values(column_name):
    # [PY5] dictionary where you write code to accesses it keys,values or items
    column_keys = list(column_value_counts[column_name].keys())
    column_values = list(column_value_counts[column_name].values())
    return column_keys,column_values

#sidebar for menu
st.sidebar.title("Menu") #[ST4] Customize page design features (sidebar)
options = st.sidebar.radio("Select an option",["Introduction","Map","Charts"])

#printing title for the webpage
st.title("Nuclear Explosions Globally")

#show intro section if intro is selected
if options =='Introduction':

    #header for section
    st.header("Introduction")

    #writing an intro blurb
    st.write("""
    This project explores a dataset of global nuclear explosions that occurred prior to the year 2000. The dataset
    includes records of the date, location, yield estimates, and the countries responsible for each detonation as
    well some other statisitcs. This website allows users to visualize and filter the data through maps, charts,
    and tables. Users can explore explosions over periods of time and compare countries' nuclear activities. The app
    also includes a geographical map of explosion sites, a breakdown of weapon types, and the distribution of the 
    source country offering insights into the historical context and global distribution of nuclear testing. """)

    #displaying an image
    image_path = "C:\\Users\\crswe\\OneDrive - Bentley University\\Spring 2025\\CS 230\\nuclear_expolsion_picture.jpg"
    img = Image.open(image_path)
    st.image(img, width=700, caption="Nuclear Explosion")

    #section header
    st.header("Here are some important facts")

    #sorting the data so the earliest date is first and outputting the info [DA2] Sort data in descending order by one column
    sorted_data = nuclear.sort_values(["Date"])[['WEAPON DEPLOYMENT LOCATION', 'Data.Name', 'Date', 'Yield Average']]
    st.write(f"The earliest explosion was {nuclear["Data.Name"].iloc[0]} and it occurred on {nuclear["Date"].iloc[0]}.")
    st.write(sorted_data.head(1))

    #finding the largest average yield and the outputting info about it [DA3] Find top largest vales of a column
    largest = nuclear[nuclear["Yield Average"] == nuclear["Yield Average"].max()][['WEAPON DEPLOYMENT LOCATION', 'Data.Name', 'Date', 'Yield Average']]
    st.write(f"The largest explosion was {largest.iloc[0]["Data.Name"]} and had an average yield of {largest.iloc[0]["Yield Average"]:.2f}  kilotons of TNT.")
    st.write(largest)

    #outputting info about most notable explosions [DA4] Filter data by one condition
    st.write("Two of the most notable explosions are Hiroshima and Nagasaki.")
    important_data = nuclear[nuclear['WEAPON DEPLOYMENT LOCATION'].isin(["Hiroshima", "Nagasaki"])][['WEAPON DEPLOYMENT LOCATION', 'Data.Name', 'Date', 'Yield Average']]
    st.write(important_data)

#show map in map is selection
elif options == "Map":

    #creating list of views
    views = ["Global", "USA-Centered", "Pacific", "Russia/Former USSR", 'Historical']

    # select box to pick which map view [ST1] streamlit widgets -- drop down
    view_selection = st.selectbox("Please select the map view:", views)

    #header based on view
    st.header(f"Here is the {view_selection} view:")

    #outuputting map based on selected view [PY1] default function, called twice
    if view_selection == "Global":
        exp_map(20, 0, 2)
    if view_selection == "USA-Centered":
        exp_map(37, -117, )
    if view_selection == "Pacific":
        exp_map(-22, -140)
    if view_selection == "Russia/Former USSR":
        exp_map(50, 78)
    if view_selection == "Historical":
        exp_map(34, 132, 7)

elif options == "Charts":

    st.header(f"Table of nuclear explosions based on the year:")

    #getting the list of source countries and their counts
    countries,country_counts  = get_keys_and_values('WEAPON SOURCE COUNTRY')


    #getting the list of deployment type and their counts
    deploy_type, deploy_counts = get_keys_and_values('Data.Type')

    #getting list of years
    year_keys = get_keys_and_values('Date.Year')[0]

    #Convert list to int and sort #[PY4] list comprehension
    years_sorted = sorted([int(y) for y in year_keys])

    # multiselect to select counties user wants to view data for [ST2] streamlit widgets -- multi-select
    selected_country = st.multiselect("Please select the countries you want to see:", countries)

    # slider to select year range user wants to view data for [ST3] streamlit widgets -- slider
    #documentation for slider features https://docs.streamlit.io/develop/api-reference/widgets/st.slider
    year_range = st.slider("Please select a year range:", min_value=min(years_sorted), max_value=max(years_sorted),
                           value=(min(years_sorted), max(years_sorted)))

    # Call the function to filter the data based on user input and show result #[VIZ1] table
    filtered_data = filter_explosions_by_year_range_and_country(year_range[0], year_range[1], selected_country)
    st.write(filtered_data)


    #writing how many explosions there are for the given criteria
    if selected_country:
        st.write(f"There are {len(filtered_data)} nuclear explosions for {" and ".join(selected_country)} between {year_range[0]} and {year_range[1]}.")


    #header for section
    st.header("Bar Chart")

    # Create a figure and axis for the bar chart [VIZ2] bar charts
    fig1, ax1 = plt.subplots(figsize=(17, 8))

    #Creating bar chart for the number of nuclear explosions based on the deployment country
    bars = ax1.bar(deploy_type, deploy_counts, color="red")

    #title for bar chart
    ax1.set_title(f"Bar chart of number of nuclear explosions based on the deployment type:")

    #adding axis labels
    ax1.set_xlabel('Deployment Types')
    ax1.set_ylabel('Deployment Type Counts')

    #adding counts above column --- adding labels found by using https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar_label.html
    ax1.bar_label(bars)

    # Show the plot in streamlit
    st.pyplot(fig1)

    # header for section
    st.header("Pie Chart")

    # Create a figure and axis for the pie chart [VIZ3] pie charts
    fig2, ax2 = plt.subplots(figsize=(10, 10))

    # title for bar chart
    ax2.set_title(f"Pie chart of deployment country:")

    # Create a pie chart of different deployment types
    ax2.pie(country_counts, labels=countries, autopct='%.2f%%')

    # Show the plot in streamlit
    st.pyplot(fig2)
