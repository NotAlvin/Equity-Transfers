import streamlit as st
from datetime import datetime
from utils.yahoo_search_helper import search_functionality
from utils.session_state_helper import remove_equity, add_portfolio
from utils.base_templates import VestingEvent

def display_add_portfolio_page(new_portfolio_name: str):
    st.write(f"Add Equities to {new_portfolio_name}")
    st.session_state['current_portfolio'].name = new_portfolio_name

    # Search functionality for equities
    search_functionality("main_search")

    if st.session_state['current_portfolio'].equities:
        st.write("Current Equities in Portfolio:")

        # Loop through each equity in the portfolio
        for name, equity in st.session_state['current_portfolio'].equities.copy().items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"- **{equity.name}** ({equity.ticker})")


            with col2:
                # Button to add a new vesting event (outside of form)
                if st.button(f"Add Vesting Event for {equity.name}"):
                    st.session_state['current_portfolio'].equities[equity.name].vesting_events.append(
                        {}
                    )

            # Form to manage vesting events for the equity
            with st.expander(f"Vesting Events for {equity.name}"):
                with st.form(f"equities_form_{equity.name}"):
                    for i, event in enumerate(st.session_state['current_portfolio'].equities[equity.name].vesting_events):
                        col1, col2, col3, col4 = st.columns([2, 3, 3, 2])
                        
                        with col1:
                            st.write(f"Vesting Event {i + 1}")

                        with col2:
                            # Input for shares vested
                            event['shares_vested'] = st.number_input(
                                "Shares Vested",
                                min_value=0,
                                key=f"shares_vested_{equity.name}_{i}"
                            )

                        with col3:
                            # Input for vesting date
                            vesting_date = st.date_input(
                                "Vesting Date",
                                key=f"vesting_date_{equity.name}_{i}"
                            )
                            # Convert to datetime.datetime and store timestamp
                            event['vesting_date'] = int(datetime.combine(vesting_date, datetime.min.time()).timestamp())
                            event = VestingEvent(**event)
                        with col4:
                            # Checkbox to delete the vesting event
                            if st.checkbox("Delete", key=f"delete_event_{equity.name}_{i}"):
                                st.session_state['current_portfolio'].equities[equity.name].vesting_events.pop(i)

                    # Submit button inside the form to save changes for the current equity
                    save_button = st.form_submit_button(f"Save {equity.name}")

                    # If the form is submitted
                    if save_button:
                        # Save changes to the portfolio after each equity update
                        add_portfolio()
                        st.success(f"Changes to {equity.name} saved successfully!")

