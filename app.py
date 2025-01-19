import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AmazonX: Next-Gen Recommendation Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load Data
@st.cache_data
def load_data():
    events_df = pd.read_csv('processed_amazon_events_data.csv')
    products_df = pd.read_csv('processed_amazon_products_data.csv')
    users_df = pd.read_csv('processed_amazon_users_data.csv')
    return events_df, products_df, users_df

events_df, products_df, users_df = load_data()

# Sidebar: User Selection
st.sidebar.title("User Selection")
user_id = st.sidebar.selectbox("Choose User ID", users_df['user_id'])

# Main Dashboard
st.title("AmazonX: Next-Gen Recommendation Engine")
st.markdown(
    """
    Welcome to AmazonX's Recommendation Dashboard!  
    Explore dynamic insights and personalized recommendations tailored to customer behavior.
    """
)

# 1. Recommendations Based on Browsing History
st.header("Recommendations Based on Browsing History")
def recommend_based_on_browsing(user_id):
    browsed_products = events_df[events_df['user_id'] == user_id]['product_id']
    
    if browsed_products.empty:
        return pd.DataFrame({"message": ["No browsing history found for this user."]})

    recommendations = products_df[products_df['product_id'].isin(browsed_products)]
    
    if recommendations.empty:
        return pd.DataFrame({"message": ["No matching products found in the catalog."]})
    
    return recommendations.sample(min(5, len(recommendations)))[['product_name', 'category', 'base_price', 'rating']]

browsing_recommendations = recommend_based_on_browsing(user_id)
st.table(browsing_recommendations)

# 2. Alternative Recommendations for Abandoned Cart (if no abandoned products found)
st.header("Alternative Recommendations")
st.markdown("""
Since there are no abandoned cart products for this user, we are recommending based on the most popular categories and top-rated products.
""")

def recommend_based_on_categories(user_id):
    # Get products the user has browsed
    browsed_product_ids = events_df[events_df['user_id'] == user_id]['product_id']
    
    if browsed_product_ids.empty:
        return pd.DataFrame({"message": ["No product browsed. Showing most popular products."]})

    # Get categories for the browsed products
    browsed_categories = products_df[products_df['product_id'].isin(browsed_product_ids)]['category'].value_counts().head(3).index
    
    recommendations = products_df[products_df['category'].isin(browsed_categories)]
    
    if recommendations.empty:
        return pd.DataFrame({"message": ["No products found in top categories. Showing most popular products."]})
    
    return recommendations.sample(min(5, len(recommendations)))[['product_name', 'category', 'base_price', 'rating']]

alternative_recommendations = recommend_based_on_categories(user_id)
st.table(alternative_recommendations)

st.sidebar.markdown("Created by Soham Kalgutkar | Empowering Recommendations!")
