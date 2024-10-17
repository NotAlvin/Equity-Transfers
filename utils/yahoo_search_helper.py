import pandas as pd
import requests
import yfinance as yf
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_searchbox import st_searchbox

from utils.base_templates import Equity
from utils.session_state_helper import add_equity


def make_search_callout(search_string: str) -> str:
    url = 'https://query1.finance.yahoo.com/v1/finance/search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    }
    params = dict(
        q=search_string,
        quotesCount=10,
        newsCount=0,
        listsCount=0,
        quotesQueryId='tss_match_phrase_query'
    )
    resp = requests.get(url=url, headers=headers, params=params)
    data = resp.json()
    if "quotes" not in data: # No results found
        return {}
    return data["quotes"]

def search_yahoo_finance(search_term: str) -> list[tuple[str, str]]:
    candidates = make_search_callout(search_term)
    formatted_results = []
    for candidate in candidates:
        ticker = candidate["symbol"]
        try:
            name = candidate["shortname"] if "shortname" in candidate else candidate["longname"]
            if candidate["isYahooFinance"]:
                formatted_results.append(
                    (
                        f"{name} ({ticker})", 
                        ticker
                    ))
        except Exception as e:
            print(f'Error {e} with search for {candidate}')
    return formatted_results

def search_functionality(key: str,) -> None:
    with stylable_container(
        key=f"container_equity_searchbox_{key}",
        css_styles="""
            {
                width: 90%;
            }
            """,
    ):
        selected_value = st_searchbox(
            search_yahoo_finance,
            key="equity_searchbox_" + key,
            clear_on_submit=True,
            placeholder="Search Equities...",
        )
    
    if selected_value is not None:
        selected_equity = get_equity_from_ticker(selected_value)
        add_equity(selected_equity)

def get_equity_from_ticker(ticker_str: str) -> Equity:
    ticker = yf.Ticker(ticker_str)

    # Fetch historical data for the last 1 year
    history = ticker.history(period="1y")  # 'Close' prices for 1 year

    # Convert historical close prices to a pandas Series with dates as index
    historical_prices_series = history['Close']

    # Convert Series to dictionary with timestamps
    historical_prices_dict = historical_prices_series.rename_axis('Date').rename(lambda x: int(x.timestamp())).to_dict()

    equity = Equity(
        isin=ticker.isin,
        ticker=ticker_str,
        name=ticker.info.get("shortName") or ticker.info.get("longName", None),
        currency=ticker.info.get('currency', None),
        latest_price=historical_prices_series.iloc[-1],  # Last available close price
        historical_prices=historical_prices_dict,  # Convert Series to dict
        shares_held=0  # Placeholder for number of shares
    )
    return equity