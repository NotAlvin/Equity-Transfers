import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Assuming this is imported from your equity class
from utils.session_state_helper import load_portfolio
from utils.finance_helper import get_historical_prices, calculate_value

# Load the portfolio from session state
if 'created_portfolio' not in st.session_state or not st.session_state.created_portfolio.equities:
    st.warning("No portfolio found. Please create a portfolio first.")
else:
    portfolio = st.session_state.created_portfolio

    # User selection for valuation method
    st.title("Portfolio Valuation Report")
    st.subheader(f"Portfolio: {portfolio.name}")

    valuation_method = st.radio(
        "Select the valuation method:",
        ('Latest Price', 'Average of Last 180 Days', 'Moving Average at Vesting Date')
    )

    # Let the user apply a discount rate
    discount_rate = st.slider("Apply a discount rate (%)", min_value=0.0, max_value=20.0, step=0.1, value=5.0)

    # Initialize data for the report
    report_data = []
    historical_data = []

    for ticker, equity in portfolio.equities.items():
        st.subheader(f"{equity.name} ({equity.ticker})")

        # Get historical prices (you might need a custom method to pull prices, e.g., via yfinance)
        historical_prices = get_historical_prices(equity.ticker, days=180)  # Adjust this as needed
        historical_data.append(historical_prices)

        # Display historical price chart
        if not historical_prices.empty:
            st.line_chart(historical_prices['Close'])

        # Calculate value based on the chosen method
        if valuation_method == 'Latest Price':
            valuation = calculate_value(equity, method='latest_price')
        elif valuation_method == 'Average of Last 180 Days':
            valuation = calculate_value(equity, method='average_180_days')
        elif valuation_method == 'Moving Average at Vesting Date':
            valuation = calculate_value(equity, method='moving_average', vesting_date=equity.vesting_date)

        # Apply discounting to the valuation
        discounted_valuation = valuation * (1 - (discount_rate / 100))

        # Display the result for the current equity
        st.write(f"Valuation (Discounted): ${discounted_valuation:.2f}")

        # Add the data for report generation
        report_data.append({
            'Ticker': equity.ticker,
            'Name': equity.name,
            'Valuation': discounted_valuation,
            'Shares Held': equity.shares_held,
            'Currency': equity.currency,
            'Vesting Date': equity.vesting_date
        })

    # Convert report data to DataFrame for visualization/export
    df_report = pd.DataFrame(report_data)

    st.write("### Portfolio Valuation Report")
    st.table(df_report)

    # Generate a downloadable CSV report
    csv_report = df_report.to_csv(index=False)
    st.download_button(label="Download CSV Report", data=csv_report, mime='text/csv')
