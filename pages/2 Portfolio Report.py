import streamlit as st
from utils.pages.display_portfolio import display_report_page, generate_report
from utils.exchange_rates_helper import CURRENCY_MAPPING

# Set page configuration
st.set_page_config(page_title="Portfolio Report", page_icon="📊")

st.title("Portfolio Report 📊")
st.subheader("Visualize your selected portfolio and its value.")

# Call the function to display the report page
selected_portfolio = display_report_page()
generate_report(selected_portfolio)
