# Guvi Courses Rating Prediction

## Project Overview

This project aims to design a regression model to predict the ratings given by learners to Guvi courses based on various features such as course title, price, number of subscribers, and more. By analyzing this dataset, we aim to uncover insights that can help improve course performance and identify opportunities for revenue generation.

## Dataset Description

The dataset contains information about Guvi courses in various categories, including:

- **course_title**: The title of the Guvi course (String).
- **url**: The URL of the Guvi course (String).
- **price**: The price of the Guvi course (Float).
- **num_subscribers**: The number of subscribers for the Guvi course (Integer).
- **num_reviews**: The number of reviews for the Guvi course (Integer).
- **num_lectures**: The number of lectures in the Guvi course (Integer).
- **level**: The level of the Guvi course (String).
- **Rating**: The rating of the Guvi course (Float) - **Target Variable**.
- **content_duration**: The content duration of the Guvi course (Float).
- **published_timestamp**: The timestamp of when the Guvi course was published (Datetime).
- **subject**: The subject of the Guvi course (String).

## Objective

The primary objective of this project is to build a regression model that accurately predicts the course ratings based on the features provided in the dataset.

## Project Steps

1. **Data Exploration**: 
   - Initial examination of the dataset to understand its structure and identify any missing values or outliers.
   - Summary statistics and visualizations to gain insights into the distribution of different features.

2. **Data Preprocessing**:
   - Handling missing values, if any.
   - Feature engineering: Creating new features or transforming existing ones to improve model performance.
   - Encoding categorical variables and normalizing numerical features.

3. **Model Building**:
   - Selection of regression models (e.g., Linear Regression, Random Forest, Gradient Boosting).
   - Training the models using the preprocessed data.
   - Hyperparameter tuning to optimize model performance.

4. **Model Evaluation**:
   - Evaluation of the models using metrics such as RMSE (Root Mean Squared Error), MAE (Mean Absolute Error), and R-squared.
   - Comparison of model performance to select the best model.

5. **Insights and Recommendations**:
   - Analysis of feature importance to understand which factors most influence course ratings.
   - Recommendations for course improvement and strategies to increase ratings.
