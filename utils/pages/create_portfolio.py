import streamlit as st
from datetime import datetime
from utils.yahoo_search_helper import search_functionality
from utils.session_state_helper import remove_equity, add_portfolio

def display_add_portfolio_page(new_portfolio_name: str):
    st.write(f"Add Equities to {new_portfolio_name}")
    st.session_state['current_portfolio'].name = new_portfolio_name

    # Search functionality for equities
    search_functionality("main_search")

    # Display added equities and input for vesting dates
    if st.session_state['current_portfolio'].equities:
        st.write("Current Equities in Portfolio:")
        
        # Use a form to manage vesting date input and delete button cleanly
        with st.form("equities_form"):
            for name, equity in st.session_state['current_portfolio'].equities.copy().items():
                col1, col2, col3, col4 = st.columns([3, 2, 4, 2])
                with col1:
                    st.write(f"- **{equity.name}** ({equity.ticker})")
                with col2:
                    shares_held = st.number_input("No. of shares held", min_value=0, max_value=None, key=f"shares_held_{equity.name}")
                    st.session_state['current_portfolio'].equities[equity.name].shares_held = shares_held
                with col3:
                    vesting_date = st.date_input(f"Vesting Date for {equity.ticker}", value=datetime.today(), key=f"vesting_date_{equity.name}")
                    # Convert to datetime.datetime if it's a date object
                    vesting_datetime = datetime.combine(vesting_date, datetime.min.time())
                    # Store the timestamp in the equity object
                    st.session_state['current_portfolio'].equities[equity.name].vesting_date = int(vesting_datetime.timestamp())
                with col4:
                    # Use checkbox for delete action instead of button to avoid rerun issues
                    if st.checkbox("Delete", key=f"delete_{equity.ticker}"):
                        remove_equity(equity)

            # Add a submit button for the form
            save_button = st.form_submit_button("Save Portfolio", type="primary")

        # Save portfolio action
        if save_button:
            add_portfolio()
            st.success(f"Portfolio '{new_portfolio_name}' created successfully!")
