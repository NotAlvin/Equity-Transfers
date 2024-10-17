import streamlit as st
from utils.session_state_helper import load_portfolios_from_json
from utils.pages.create_portfolio import display_add_portfolio_page
from utils.base_templates import Portfolio

# Set page configuration
st.set_page_config(page_title="Portfolio Setup", page_icon="💼")

st.title("Portfolio Creation 💼")
st.subheader("Add equities with their vesting schedules.")

if 'portfolios' not in st.session_state:
    st.session_state['portfolios'] = load_portfolios_from_json()

# Add new portfolio
new_portfolio_name = st.text_input("New Portfolio Name")

if new_portfolio_name:
    # Check if portfolio name already exists
    if new_portfolio_name in st.session_state['portfolios']:
    # Load the existing portfolio
        existing_portfolio = st.session_state['portfolios'][new_portfolio_name]
        st.session_state['current_portfolio'] = existing_portfolio
        
        # Display the add portfolio page with the existing portfolio
        display_add_portfolio_page(new_portfolio_name)

    else:
        # Create a new portfolio
        new_portfolio = Portfolio(name=new_portfolio_name, equities={})
        st.session_state['current_portfolio'] = new_portfolio
        st.session_state['portfolios'][new_portfolio_name] = new_portfolio  # Add new portfolio to session state

        # Display the add portfolio page for the new portfolio
        display_add_portfolio_page(new_portfolio_name)
