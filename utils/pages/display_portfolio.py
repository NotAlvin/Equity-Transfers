import streamlit as st
import pandas as pd
from datetime import datetime
from utils.session_state_helper import load_portfolios_from_json
from utils.exchange_rates_helper import fetch_latest_exchange_rates, convert_to_usd


def display_report_page():
    # Load portfolios
    portfolios = load_portfolios_from_json()

    # Create a dropdown to select a portfolio
    portfolio_names = list(portfolios.keys())
    selected_portfolio_name = st.selectbox("Select a Portfolio", options=portfolio_names)

    if selected_portfolio_name:
        # Retrieve the selected portfolio
        selected_portfolio = portfolios[selected_portfolio_name]

        # Display portfolio details
        st.write(f"**Selected Portfolio**: {selected_portfolio.name}")
        st.write("Equities in Portfolio:")
        for equity in selected_portfolio.equities.values():
            st.write(f"- {equity.name} ({equity.ticker}) - Shares Held: {equity.shares_held}, Vesting Date: {datetime.fromtimestamp(equity.vesting_date)}")

        return selected_portfolio

def generate_report(selected_portfolio, selected_method):
    if st.button("Generate Report"):
        st.success(f"Generating report for portfolio: {selected_portfolio.name}")

        # Collect the currencies for all equities in the selected portfolio
        currencies = {equity.currency for equity in selected_portfolio.equities.values()}
        
        # Fetch the latest exchange rates for the currencies
        rates = fetch_latest_exchange_rates(currencies)

        # Initialize a DataFrame to hold the historical prices for the chart
        price_data = pd.DataFrame()

        # Collect historical price data for each equity in the portfolio
        for equity in selected_portfolio.equities.values():
            if equity.historical_prices:  # Ensure historical prices are available
                # Convert the historical prices dictionary to a DataFrame
                prices_df = pd.Series(equity.historical_prices).rename_axis('Date').reset_index(name='Price')
                
                # Convert timestamps back to datetime
                prices_df['Date'] = pd.to_datetime(prices_df['Date'], unit='s')  # Convert timestamps to datetime
                
                # Convert prices to USD
                if equity.currency != 'USD':
                    prices_df['Price'] = convert_to_usd({equity.currency: prices_df['Price'].sum()}, rates)[equity.currency]
                prices_df['Ticker'] = equity.ticker
                
                # Append to price data
                price_data = pd.concat([price_data, prices_df], ignore_index=True)

        # Plotting the price data if available
        if not price_data.empty:
            # Pivoting the DataFrame to have dates as index and tickers as columns
            price_data_pivoted = price_data.pivot(index='Date', columns='Ticker', values='Price')
            st.line_chart(price_data_pivoted)

        # Calculate and display portfolio value based on the selected method
        portfolio_value = 0
        for equity in selected_portfolio.equities.values():
            # Calculate value for each equity in USD
            value = equity.calculate_value(method=selected_method)
            if value is not None:
                portfolio_value += value

        st.write(f"**Total Portfolio Value using '{selected_method}' method:** ${portfolio_value:,.2f} USD")

