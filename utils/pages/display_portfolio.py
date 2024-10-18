import streamlit as st
import pandas as pd
from datetime import datetime
from utils.session_state_helper import load_portfolios_from_json
from utils.exchange_rates_helper import fetch_latest_exchange_rates, convert_to_base_currency

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

        return selected_portfolio

def generate_report(selected_portfolio):
    # Select the calculation method and base currency at the top
    # Calculate portfolio value based on selected method
    mapping = {
            "Average: Using average price from the past 180 days": "average",
            "Latest: Using Latest Price": "latest",
            "Moving Average: Extrapolating the price at vesting date": "moving_average"
            }
    selected_method = st.selectbox("Select Calculation Method", options=mapping.keys())
    selected_method = mapping[selected_method]
    base_currency = st.selectbox("Select Base Currency", options=["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "NZD", "SGD", "HKD", "INR", "MXN", "ZAR"], index=0)

    if st.button("Generate Report"):
        st.success(f"Generating report for portfolio: {selected_portfolio.name}")
        st.subheader("Recent price changes in underlying equities")
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

                # Convert prices from USD to the selected base currency
                prices_df['Price_in_base_currency'] = prices_df['Price'].apply(
                    lambda price: convert_to_base_currency(price, rates, from_currency=equity.currency, to_currency=base_currency)
                )

                prices_df['Ticker'] = equity.ticker
                
                # Append to price data
                price_data = pd.concat([price_data, prices_df[['Date', 'Price_in_base_currency', 'Ticker']]], ignore_index=True)

        # Plotting the price data if available
        if not price_data.empty:
            # Pivoting the DataFrame to have dates as index and tickers as columns
            price_data_pivoted = price_data.pivot(index='Date', columns='Ticker', values='Price_in_base_currency')
            st.line_chart(price_data_pivoted)

        # Display payout schedule
        st.subheader("Payout Schedule")
        payout_schedule = []
        current_time = datetime.now().timestamp()

        # Initialize a total portfolio value
        total_portfolio_value = 0

        # Collect payout events for each equity
        for equity in selected_portfolio.equities.values():
            for event in equity.vesting_events:
                # Calculate the value of each vesting event based on the selected method
                value = equity.calculate_value(method=selected_method)
                value = convert_to_base_currency(value, rates, from_currency=equity.currency, to_currency=base_currency)
                if value is not None:
                    # Adjust for time value of money with the discount rate

                    total_portfolio_value += value

                    # Add the payout event to the schedule
                    payout_schedule.append({
                        "Equity": equity.name,
                        "Ticker": equity.ticker,
                        "Vesting Date": datetime.fromtimestamp(event.vesting_date),
                        "Shares Vested": event.shares_vested,
                        f"Value ({base_currency})": round(value, 2)
                    })

        # Display the payout schedule as a table
        if payout_schedule:
            payout_df = pd.DataFrame(payout_schedule)
            # Ensure the vesting_date is sorted
            payout_df = payout_df.sort_values(by='Vesting Date')
            daily_payouts = payout_df.groupby('Vesting Date').agg({f'Value ({base_currency})': 'sum'}).reset_index()
            daily_payouts.columns = ['Vesting Date', 'Amount Paid']
            payout_df['Month'] = payout_df['Vesting Date'].dt.to_period('M')
            monthly_payout_df = payout_df.groupby(['Month']).agg({
                f'Value ({base_currency})': 'sum'
            }).reset_index()
            # Calculate cumulative payout
            monthly_payout_df[f'Cumulative Payout ({base_currency})'] = monthly_payout_df[f'Value ({base_currency})'].cumsum()


            # Plotting the cumulative payouts over time
            if not payout_df.empty:
                st.bar_chart(daily_payouts.set_index('Vesting Date'))
                st.table(monthly_payout_df)

        st.write(f"**Total Portfolio Value using '{selected_method}' method in {base_currency}:** {total_portfolio_value:,.2f} {base_currency}")

