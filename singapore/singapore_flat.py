#IMPORT REQUIRED PACKAGE
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import pickle

#LOAD THE TRAINED MODEL
with open("C:/Users/monis/Desktop/guvi project/singapore/Resale_Flat_Prices.pkl" , "rb") as f:
    model = pickle.load(f)

#LOAD PICKLE LABEL ENCODER FOR TOWN
with open("C:/Users/monis/Desktop/guvi project/singapore/town.pkl" , "rb") as f:
    town_pkl = pickle.load(f)

#LOAD PICKLE LABEL ENCODER FOR FLAT TYPE
with open("C:/Users/monis/Desktop/guvi project/singapore/flat_type.pkl" , "rb") as f:
    flat_type_pkl = pickle.load(f)

#LOAD PICKLE LABEL ENCODER FOR FLAT MODEL
with open("C:/Users/monis/Desktop/guvi project/singapore/flat_model.pkl" , "rb") as f:
    flat_model_pkl = pickle.load(f)

#STREAMLIT APPLICATION
st.title("Singapore Resale Flat Price Prediction")
st.write("Enter the details of the flat to predict its resale price.")

#GET INPUT FROM USER
town = st.selectbox("Town", ['SENGKANG','WOODLANDS','PUNGGOL','JURONG WEST','TAMPINES','YISHUN','BEDOK','HOUGANG','CHOA CHU KANG','ANG MO KIO','BUKIT BATOK','BUKIT MERAH','BUKIT PANJANG','TOA PAYOH','KALLANG/WHAMPOA','PASIR RIS','SEMBAWANG','QUEENSTOWN','CLEMENTI','JURONG EAST','SERANGOON','BISHAN','CENTRAL AREA','BUKIT TIMAH'])
flat_type = st.selectbox("Flat Type", ['1 Room', '2 Room', '3 Room', '4 Room', '5 Room', 'Executive', 'Multi-Generation'])
flat_model = st.selectbox("Flat Model", ['Model A', 'Model B', 'Model C', 'Improved', 'New Generation', 'Simplified', 'Standard'])
block = st.number_input("Block[eg:760.0,min:1.0]")
floor_area_sqm = st.number_input("Floor Area (sqm)", min_value=10, max_value=200, step=1)
lease_commence_date = st.number_input("Lease Commence Date[eg:2004]", step=1)
resale_year = st.number_input("Resale Year[eg:2016]", step=1)
resale_month = st.number_input("Resale Month[min:1.max:12]",min_value=1, max_value=12, step=1)
storey_lower_bound = st.number_input("Storey Start", min_value=1, max_value=50, step=1)
storey_upper_bound = st.number_input("Storey End", min_value=1, max_value=50, step=1)
remaining_lease_in_month = st.number_input("Remaining Lease in Month[eg:240.0,min:1.0]", min_value=0, max_value=1100)

#TRANSFORM THE ENCODED DATA

town_encoded=town_pkl.transform([[town]])
flat_type_encoded=flat_type_pkl.fit_transform([[flat_type]])
flat_model_encoded=flat_model_pkl.transform([[flat_model]])

#PROCESS THE INPUT DATA
input_data = pd.DataFrame({
    'town':town_encoded,
    'flat_type':flat_type_encoded,
    'block':[block],
    'floor_area_sqm': [floor_area_sqm],
    'flat_model':flat_model_encoded,
    'lease_commence_date': [lease_commence_date],
    'resale_year':[resale_year],
    'resale_month':[resale_month],
    'storey_lower_bound': [storey_lower_bound],
    'storey_upper_bound': [storey_upper_bound],
    'remaining_lease_in_months': [remaining_lease_in_month]    
})

#PREDICT RESALE PRICE
if st.button("Predict Resale Price"):
    prediction = model.predict(input_data)
    st.success(f"The predicted resale price is: ${prediction}")