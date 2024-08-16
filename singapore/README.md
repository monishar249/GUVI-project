# Singapore_flat_resale_price_prediction

## Overview
This project aims to develop a machine learning model to predict the resale prices of flats in Singapore. The model is built using historical resale flat transaction data from the Housing and Development Board (HDB) of Singapore and is deployed as a user-friendly web application using Streamlit.

## Motivation
Estimating the resale value of flats in Singapore can be challenging due to the competitive market and numerous influencing factors such as location, flat type, floor area, and lease duration. This project aims to assist potential buyers and sellers by providing an estimated resale price based on these factors, helping them make informed decisions.

## Project Scope
1. **Data Collection and Preprocessing**: 
   - Collect historical resale flat transaction data from HDB covering the years 1990 to present.
   - Clean and structure the data for machine learning.

2. **Feature Engineering**:
   - Extract relevant features such as town, flat type, storey range, floor area, flat model, and lease commence date.
   - Create additional features to enhance prediction accuracy.

3. **Model Selection and Training**:
   - Choose appropriate regression models (e.g., linear regression, decision trees, random forests).
   - Train the model using a portion of the dataset.

4. **Model Evaluation**:
   - Evaluate the model's performance using regression metrics like Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R² Score.

5. **Streamlit Web Application**:
   - Develop a user-friendly web application using Streamlit.
   - Allow users to input flat details and get predicted resale prices based on the trained model.

6. **Deployment on Render**:
   - Deploy the Streamlit application on the Render platform for internet accessibility.
   - https://singapore-flat-resale-price-prediction-m7i3.onrender.com

7. **Testing and Validation**:
   - Thoroughly test the application to ensure accurate predictions and functionality.
