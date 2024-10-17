import streamlit as st
from utils.pages.display_portfolio import display_report_page, generate_report

# Set page configuration
st.set_page_config(page_title="Portfolio Report", page_icon="📊")

st.title("Portfolio Report 📊")
st.subheader("Visualize your selected portfolio and its value.")

# Call the function to display the report page
selected_portfolio = display_report_page()
# Calculate portfolio value based on selected method
mapping = {"Latest: Using Latest Price": "latest",
           "Average: Using average price from the past 180 days": "average",
           "Moving Average: Extrapolating the price at vesting date": "moving_average"
}
selected_method = st.selectbox("Select Portfolio Value Calculation Method", mapping.keys())
generate_report(selected_portfolio, mapping[selected_method])
