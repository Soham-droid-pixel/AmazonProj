# Step 2: Create the Streamlit app (app.py)
%%writefile app.py
import streamlit as st
import pandas as pd

# Load data (Assuming processed CSV files for events, products, and users)
events_df = pd.read_csv('/content/drive/MyDrive/10192_10189act6/processed_amazon_events_data.csv')
products_df = pd.read_csv('/content/drive/MyDrive/10192_10189act6/processed_amazon_products_data.csv')
users_df = pd.read_csv('/content/drive/MyDrive/10192_10189act6/processed_amazon_users_data.csv')

# Display column names for debugging
st.write("Users DataFrame Columns:", users_df.columns)

# Dropdown for selecting user
user_id = st.selectbox("Select User ID", users_df['user_id'])

# Get user data
user_data = users_df.loc[users_df['user_id'] == user_id].iloc[0]

# Display user demographics with a check for missing columns
st.write(f"**Age:** {user_data['age']}")
st.write(f"**Gender:** {user_data['gender']}")
st.write(f"**Prime Member:** {'Yes' if user_data['is_prime_member'] else 'No'}")

# Safely retrieve 'preferred_platform' if it exists, otherwise display 'Not Available'
preferred_platform = user_data.get('preferred_platform', 'Not Available')
st.write(f"**Preferred Platform:** {preferred_platform}")

# Function to provide recommendations based on the user's Prime status
def get_recommendations(user_id):
    is_prime_member = user_data['is_prime_member']
    # Example logic for Prime Members
    if is_prime_member:
        recommended_products = products_df[products_df['prime_eligible'] == True].head(5)
    else:
        recommended_products = products_df.sample(5)
    
    return recommended_products

# Get product recommendations
recommended_products = get_recommendations(user_id)

# Display recommendations
st.write("**Product Recommendations:**")
st.write(recommended_products[['product_name', 'category', 'base_price']])

# Optionally, you can display the products as a table for better readability
st.table(recommended_products[['product_name', 'category', 'base_price']])


# Step 3: Set up ngrok to expose the Streamlit app
from pyngrok import ngrok

# Open a tunnel to the streamlit app
public_url = ngrok.connect(port='8501')
st.write('Streamlit app is live at:', public_url)

# Step 4: Run the Streamlit app
!streamlit run app.py &

