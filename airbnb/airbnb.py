#IMPORT REQUIRED PACKAGE
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd


#SET PAGE CONFIGURATION
st.set_page_config(page_title="AirBnb-Analysis", page_icon=":bar_chart:", layout="wide")

with st.sidebar:
 SELECT = option_menu(
    menu_title=None,
    options=["Home", "Explore Data"])

#HOME
if SELECT=='Home':
    st.title("AIRBNB ANALYSIS")
    st.title("KEY SKILLS")
    st.markdown("<h3 style='font-size:20px;'>Python scripting, Data Preprocessing, Visualization,EDA, Streamlit, MongoDb</h3>", unsafe_allow_html=True)
    st.title("STEPS INVOLVED IN AIRBNB ANALYSIS")
    st.markdown("<h3 style='font-size:20px;'>STEP1: Establish a MongoDB connection</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px;'>STEP2: Clean and prepare the dataset</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px;'>STEP3: Develop a streamlit web application</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px;'>STEP4: Insight made on Price, Location, Property type and Rating</h3>", unsafe_allow_html=True)

#EXPLORE DATA
if SELECT=='Explore Data':
    df = pd.read_csv('airbnb_DATA.csv')

    cities = df['City'].unique()
    selected_cities = st.multiselect("Select Cities", options=cities, default=cities)
    filtered_df = df[df['City'].isin(selected_cities)]
    
    #PLOT1: PROPERTY_TYPE BY CITY
    property_count = filtered_df.groupby(['City', 'Property_type']).size().reset_index(name='Count')
    st.write("Property Types by City")
    fig = px.bar(
        data_frame=property_count,
        x='City',
        y='Count',
        color='Property_type',
        title="Distribution of Property Types by City",
        labels={'Count': 'Number of Properties', 'City': 'City'})
    st.plotly_chart(fig, use_container_width=True)

    #PLOT2: ROOM_TYPE BY CITY
    ROOM_count = filtered_df.groupby(['City', 'Room_type']).size().reset_index(name='Count')
    st.write("Room Types by City")
    fig = px.pie(
    data_frame=ROOM_count,
    names='Room_type',
    values='Count',
    color='Room_type',
    title=f"Distribution of Room Types",
    labels={'Count': 'Number of Rooms', 'room_type': 'Room Type'})
    st.plotly_chart(fig, use_container_width=True)

    st.title("PRICE ANALYSIS")

    #PLOT3:PRICE BY CITY
    st.write("PRICE BY CITY")
    price_by_city = filtered_df.groupby('City')['Price'].mean().reset_index().sort_values(by='Price', ascending=True)
    fig_price = px.bar(data_frame=price_by_city, x='Price', y='City',orientation='h')
    st.plotly_chart(fig_price, use_container_width=True)

    #PLOT4:PRICE BY PROPERTY_TYPE
    st.write("PRICE BY PROPERTY TYPE")
    price_by_city = filtered_df.groupby('Property_type')['Price'].mean().reset_index().sort_values(by='Price', ascending=True)
    fig_price = px.bar(data_frame=price_by_city, x='Property_type', y='Price',orientation='v')
    st.plotly_chart(fig_price, use_container_width=True)

    #PLOT5:PRICE BY ROOM_TYPE
    st.write("PRICE BY ROOM TYPE")
    price_by_room = filtered_df.groupby('Room_type')['Price'].mean().reset_index().sort_values(by='Price', ascending=True)
    fig = px.bar(data_frame=price_by_room,x='Room_type', y='Price',color='Price',title='Avg Price in each Room type')
    st.plotly_chart(fig,use_container_width=True)

    st.title("AVAILABLITY ANALYSIS")
    #PLOT6:CITY BY AVAILABLITY
    city_by_availablity = filtered_df.groupby('City').agg({
        'Availability_30': 'mean',
        'Availability_60': 'mean',
        'Availability_90': 'mean',
        'Availability_365': 'mean'
    }).reset_index()
    city_by_availablity = city_by_availablity.melt(id_vars='City', var_name='Availability Period', value_name='Availability')

    fig = px.line(
    data_frame=city_by_availablity,
    x='City',
    y='Availability',
    color='Availability Period',
    title="Availability of Property Types by City Over Time")

    st.plotly_chart(fig, use_container_width=True)
    
    #PLOT7: PROPERTY BY AVAILABLITY
    property_by_availablity = filtered_df.groupby('Property_type').agg({
        'Availability_30': 'mean',
        'Availability_60': 'mean',
        'Availability_90': 'mean',
        'Availability_365': 'mean'
    }).reset_index()
    property_by_availablity = property_by_availablity.melt(id_vars='Property_type', var_name='Availability Period', value_name='Availability')

    fig = px.area(
    data_frame=property_by_availablity,
    x='Property_type',
    y='Availability',
    color='Availability Period',
    title="Availability of Property Types Over Time")

    st.plotly_chart(fig, use_container_width=True)
    
    st.title("OCCUPANCY RATES")

    #PLOT8:DEMAND FOR PROPERTIES
    df_agg = filtered_df.groupby('Property_type').agg({
    'Min_nights': 'min',  
    'Max_nights': 'min'
    }).reset_index()

    fig = px.bar(df_agg, x='Property_type', y=['Min_nights', 'Max_nights'],barmode='group', labels={'value': 'Nights', 'property_type': 'Property Type'})
    fig.update_layout(title='Minimum and Maximum Nights by Property Type', xaxis_title='Property Type',yaxis_title='Nights')
    st.plotly_chart(fig)

    #PLOT9:OCCUPANCY RATE BY ROOM TYPE
    df_agg = filtered_df.groupby('Room_type').agg({
    'Total_bedrooms': 'mean',  
    'Total_beds': 'mean'
    }).reset_index()

    fig = px.bar(df_agg, x='Room_type', y=['Total_bedrooms', 'Total_beds'],barmode='group')
    fig.update_layout(title='Total bedrooms and Total beds by Room Type', xaxis_title='Room Type',yaxis_title='Total bedrooms and Total beds')
    st.plotly_chart(fig)

    #PLOT10:OCCUPANCY RATE BY PROPERTY TYPE
    agg = filtered_df.groupby('Property_type').agg({
    'Total_bedrooms': 'mean',  
    'Total_beds': 'mean'
    }).reset_index()

    fig = px.bar(agg, x='Property_type', y=['Total_bedrooms', 'Total_beds'],barmode='group')
    fig.update_layout(title='Total bedrooms and Total beds by Property Type', xaxis_title='Property_Type',yaxis_title='Total bedrooms and Total beds')
    st.plotly_chart(fig)


    #PLOT12:GEOSPATIAL VISUALIZATION
    st.write("GEO-SPATIAL VISUALIZATION")
    fig = px.scatter_mapbox(filtered_df, 
                            lat="Latitude", 
                            lon="Longitude", 
                            hover_name="City", 
                            zoom=5,
                            height=600
                           )
    fig.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig, use_container_width=True)