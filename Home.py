import streamlit as st

st.set_page_config(
    page_title="Equity Transfer Pricing",
    page_icon="💼",
)

st.write("# Welcome to Equity Transfer Pricing! 💼")

st.sidebar.success("Select **Equity Valuation** page to start!")

st.markdown(
    """
    This application helps HR departments properly price the vested shares of new joiners from their previous companies. It allows you to assess the value of shares that need to be forfeited and propose compensation accordingly.
    
    **👈 Select the Create Portfolio page from the sidebar** to begin.

    ### Key Features:
    - Input details about a new joiner's vested shares from their previous employer
    - Automatically fetch the latest stock price of the previous company
    - Calculate the forfeiture cost, including tax implications
    - Generate recommendations on compensation packages for the new joiner, including equity replacements or bonuses

    ### How to Use:
    1. Go to the **Create Portfolio** page to input details of the new joiner's vested shares.
    2. Visualize the stock price history and see the calculated forfeiture cost.
    3. Generate and download reports with suggested compensation packages in the **Generate Report** page.
    """
)
