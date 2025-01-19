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
    # Get top 3 categories the user has browsed
    browsed_categories = events_df[events_df['user_id'] == user_id]['category'].value_counts().head(3).index
    
    recommendations = products_df[products_df['category'].isin(browsed_categories)]
    
    if recommendations.empty:
        return pd.DataFrame({"message": ["No products found in top categories. Showing most popular products."]})
    
    return recommendations.sample(min(5, len(recommendations)))[['product_name', 'category', 'base_price', 'rating']]

alternative_recommendations = recommend_based_on_categories(user_id)
st.table(alternative_recommendations)

# 3. Top Rated and Discounted Products (Popular Products in the Catalog)
st.header("Top Rated and Discounted Products")
top_rated_discounted = products_df[(
    products_df['rating'] >= 4.5) & (products_df['discount'] > 0)
].sort_values(by='rating', ascending=False).head(5)

st.table(top_rated_discounted[['product_name', 'category', 'base_price', 'discount', 'rating']])

# 4. User Segmentation-Based Recommendations
st.header("User Segmentation Recommendations")
def recommend_for_segment(user_id):
    user_cluster = users_df.loc[users_df['user_id'] == user_id, 'cluster'].values[0]
    if user_cluster == 0:
        return products_df[products_df['category'] == 'Electronics'].sample(5)
    else:
        return products_df[products_df['category'] == 'Fashion'].sample(5)

segmentation_recommendations = recommend_for_segment(user_id)
st.table(segmentation_recommendations[['product_name', 'category', 'base_price', 'rating']])

# 5. Seasonal Trends Visualization
st.header("Seasonal Trends")
st.markdown("Interactive visualization of purchasing trends by season.")
seasonal_trends = events_df.groupby(['month', 'event_type']).size().unstack().fillna(0)
st.line_chart(seasonal_trends)

# 6. Filters: Price, Prime, Popularity
st.sidebar.header("Advanced Filters")
min_price = st.sidebar.slider("Min Price", int(products_df['base_price'].min()), int(products_df['base_price'].max()), 0)
max_price = st.sidebar.slider("Max Price", int(products_df['base_price'].min()), int(products_df['base_price'].max()), 500)
only_prime = st.sidebar.checkbox("Show Prime Eligible Only", value=False)

st.header("Filtered Recommendations")
def filter_and_sort_recommendations(recommendations):
    filtered = recommendations[(
        recommendations['base_price'] >= min_price) & (recommendations['base_price'] <= max_price)
    ]
    if only_prime:
        filtered = filtered[filtered['prime_eligible'] == True]
    return filtered.sort_values(by=['rating', 'review_count'], ascending=[False, False])

filtered_recommendations = filter_and_sort_recommendations(products_df)
st.table(filtered_recommendations[['product_name', 'category', 'base_price', 'rating', 'prime_eligible']].head(10))

st.sidebar.markdown("Created by Soham Kalgutkar | Empowering Recommendations!")
