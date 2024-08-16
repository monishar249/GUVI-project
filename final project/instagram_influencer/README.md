# Instagram Influencers Analysis

## Project Overview

This project focuses on analyzing Instagram influencers by leveraging a dataset containing various metrics related to their social media presence. The goal is to understand the impact and influence of these users by examining their posts, engagement rates, follower counts, and more. This analysis can help identify key influencers, trends, and opportunities for marketing and outreach strategies.

## Dataset Description

The dataset contains the following columns, each providing different aspects of the influencers' profiles:

- **rank**: Rank of the influencer (Integer).
- **channel_info**: Username of the Instagrammer (String).
- **influence_score**: Influence score of the user (Float).
- **posts**: Number of posts the user has made so far (Integer).
- **followers**: Number of followers of the user (Integer).
- **avg_likes**: Average likes on the Instagrammer's posts (Float).
- **60dayeng_rate**: Last 60 days engagement rate of the Instagrammer as a fraction of engagements they have done so far (Float).
- **newpostavg_like**: Average likes on the user’s new posts (Float).
- **total_likes**: Total likes the user has received on their posts (in billions) (Float).
- **country**: Country or region of origin of the user (String).

## Objective

The objective of this project is to analyze the influence and engagement of Instagram influencers based on the provided dataset. This analysis will help in identifying the most impactful influencers and understanding the factors contributing to their success on the platform.

## Project Steps

1. **Data Exploration**:
   - Load and inspect the dataset to understand its structure and content.
   - Visualize key statistics and trends in the data, such as distribution of followers, average likes, and engagement rates.

2. **Data Preprocessing**:
   - Handle any missing or inconsistent data.
   - Perform feature engineering to create new insights or refine existing metrics.
   - Normalize or scale data as needed for analysis.

3. **Analysis**:
   - Identify top influencers based on various metrics such as influence score, number of followers, and engagement rates.
   - Explore relationships between different features, such as the correlation between followers and average likes.
   - Use clustering or other methods to categorize influencers based on their profiles.
