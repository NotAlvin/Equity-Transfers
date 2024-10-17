import json
import streamlit as st
from utils.base_templates import Equity, Portfolio

PORTFOLIOS_JSON_PATH = 'data/portfolios.json'

def save_portfolios_to_json(portfolios: dict[str, Portfolio], file_path: str=PORTFOLIOS_JSON_PATH) -> None:
    portfolios_data = {name: portfolio.dict() for name, portfolio in portfolios.items()}
    with open(file_path, 'w') as json_file:
        json.dump(portfolios_data, json_file, indent=4)

def load_portfolios_from_json(file_path: str=PORTFOLIOS_JSON_PATH) -> dict[str, Portfolio]:
    with open(file_path, 'r') as json_file:
        portfolios_data = json.load(json_file)
    return {name: Portfolio(**data) for name, data in portfolios_data.items()}


def add_equity(equity: Equity) -> None:
    """
    Adds an equity to the current portfolio being created.
    """
    if equity.name not in st.session_state['current_portfolio'].equities:
        st.session_state['current_portfolio'].equities[equity.name] = equity
    
def remove_equity(equity: Equity) -> None:
    """
    Removes an equity from the current portfolio being created.
    """
    if equity.name in st.session_state['current_portfolio'].equities:
        del st.session_state['current_portfolio'].equities[equity.name]

def update_equity(shares_held: float, selected_portfolio: str, equity: Equity):
    """
    Updates the number of shares held for a given equity in an existing portfolio.
    """
    st.session_state['portfolios'][selected_portfolio].equities[equity.name].shares_held = shares_held
    save_portfolios_to_json(st.session_state['portfolios'], PORTFOLIOS_JSON_PATH)

def add_portfolio() -> None:
    """
    Adds the current portfolio to the list of portfolios and saves it.
    """
    portfolio = st.session_state['current_portfolio']
    st.session_state['portfolios'][portfolio.name] = portfolio
    save_portfolios_to_json(st.session_state['portfolios'], PORTFOLIOS_JSON_PATH)

def remove_portfolio(portfolio_name: str) -> None:
    """
    Removes an existing portfolio.
    """
    if portfolio_name in st.session_state['portfolios']:
        del st.session_state['portfolios'][portfolio_name]
        
    save_portfolios_to_json(st.session_state['portfolios'], PORTFOLIOS_JSON_PATH)
    # Reset current portfolio if it was deleted
    if st.session_state['current_portfolio'].name == portfolio_name:
        st.session_state['current_portfolio'] = Portfolio(name='', equities={})
    

def toggle_display() -> None:
    """
    Toggles a display flag in session state.
    """
    st.session_state['display'] = not st.session_state['display']
