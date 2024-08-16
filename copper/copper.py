#IMPORT REQUIRED PACKAGE
import numpy as np
import streamlit as st
import pickle
import pandas as pd

st.title("INDUSTRIAL COPPER MODELING")
#TAB1 FOR PREDICTING SELLING_PRICE, TAB2 FOR PREDICTING STATUS
tab1, tab2 = st.tabs(["PREDICT SELLING PRICE", "PREDICT STATUS"])

#POSSIBLE VALUES FOR DROPDOWN MENU
status_options = ['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM', 'Wonderful', 'Revised', 'Offered', 'Offerable']
item_type_options = ['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']
country_options = [28., 25., 30., 32., 38., 78., 27., 77., 113., 79., 26., 39., 40., 84., 80., 107., 89.]
application_options = [10., 41., 28., 59., 15., 4., 38., 56., 42., 26., 27., 19., 20., 66., 29., 22., 40., 25., 67., 79., 3., 99., 2., 5., 39., 69., 70., 65., 58., 68.]
product=['611112', '611728', '628112', '628117', '628377', '640400', '640405', '640665', 
                     '611993', '929423819', '1282007633', '1332077137', '164141591', '164336407', 
                     '164337175', '1665572032', '1665572374', '1665584320', '1665584642', '1665584662', 
                     '1668701376', '1668701698', '1668701718', '1668701725', '1670798778', '1671863738', 
                     '1671876026', '1690738206', '1690738219', '1693867550', '1693867563', '1721130331', '1722207579']

#TAB1- PREDICT SELLING_PRICE-REGRESSION
with tab1:

    # LOAD PICKLE FOR MODEL.SCALER, ITEM_PRICE OHE, STATUS OHE
    with open(r"C:/Users/monis/Desktop/guvi project/copper/rmodel.pkl", 'rb') as file:
        loaded_model = pickle.load(file)
    with open(r'C:/Users/monis/Desktop/guvi project/copper/rscaler.pkl', 'rb') as f:
        scaler_loaded = pickle.load(f)
    with open(r"C:/Users/monis/Desktop/guvi project/copper/rit.pkl", 'rb') as f:
        t_loaded = pickle.load(f)
    with open(r"C:/Users/monis/Desktop/guvi project/copper/rs.pkl", 'rb') as f:
        s_loaded = pickle.load(f)

    #GET DATA FROM USER
    application = st.selectbox("Select Application", sorted(application_options))
    country = st.selectbox("Select Country", sorted(country_options))
    product_ref = st.selectbox("Select Product Reference", product)
    item_type = st.selectbox("Select Item Type", item_type_options)
    status = st.selectbox("Select Status", status_options)
    quantity_tons = st.text_input("Enter Quantity Tons")
    thickness = st.text_input("Enter thickness")
    width = st.text_input("Enter width")
    customer = st.text_input("Enter customer ID ")
    

    #TRANSFORM THE ENCODED DATA
    it_encoded=t_loaded.transform([[item_type]]).toarray()
    s_encoded=s_loaded.transform([[status]]).toarray()

    #PROCESS THE INPUT DATA
    input_data = pd.DataFrame({
        'quantity tons':[quantity_tons],
        'application':[application],
        'thickness':[thickness],
        'width':[width],
        'country':[country],
        'customer':[customer],
        'product_ref':[product_ref]
    })
    new_sample = np.concatenate((input_data,it_encoded,s_encoded), axis=1)
    new_sample1 = scaler_loaded.transform(new_sample)

    #PREDICT RESALE PRICE
    if st.button("Predict Resale Price"):
        prediction = loaded_model.predict(new_sample1)[0]
        st.success(f"The predicted resale price is: ${prediction}")

#TAB2- PREDICT STATUS-CLASSIFICATION
with tab2:

    # LOAD PICKLE FOR MODEL.SCALER, ITEM_PRICE OHE
    with open(r"C:/Users/monis/Desktop/guvi project/copper/cmodel.pkl", 'rb') as file:
        cmodel = pickle.load(file)
    with open(r'C:/Users/monis/Desktop/guvi project/copper/cscaler.pkl', 'rb') as f:
        cscaler_loaded = pickle.load(f)
    with open(r"C:/Users/monis/Desktop/guvi project/copper/ct.pkl", 'rb') as f:
        c_t_loaded = pickle.load(f)

    #GET DATA FROM USER
    application = st.selectbox("Application", sorted(application_options))
    country = st.selectbox("Country", sorted(country_options))
    product_ref = st.selectbox("Product Reference", product)
    item_type = st.selectbox("Item Type", item_type_options)
    quantity_tons = st.text_input("Quantity Tons")
    thickness = st.text_input("thickness")
    width = st.text_input("width")
    customer = st.text_input("customer ID ")
    selling = st.text_input("Selling Price")

    ##TRANSFORM THE ENCODED DATA
    cit_encoded=t_loaded.transform([[item_type]]).toarray()

    #PROCESS THE INPUT DATA
    input_data = pd.DataFrame({
        'quantity tons':[quantity_tons],
        'selling price':[selling],
        'application':[application],
        'thickness':[thickness],
        'width':[width],
        'country':[country],
        'customer':[customer],
        'product_ref':[product_ref]
    })
    new_sample = np.concatenate((input_data,cit_encoded), axis=1)
    new_sample1 = cscaler_loaded.transform(new_sample)

    #PREDICT STATUS
    if st.button("Predict Status"):
        status= cmodel.predict(new_sample1)
        if status==1:
            st.write("The status is WON")
        else:
            st.write("The status is LOST")
            