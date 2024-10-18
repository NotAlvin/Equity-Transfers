import os
import json
import pandas_datareader.data as web
from datetime import datetime

CURRENCY_MAPPING = {
    'EUR': 'USEU',  # Euro
    'GBP': 'USUK',  # British Pound
    'JPY': 'JPUS',  # Japanese Yen
    'AUD': 'USAL',  # Australian Dollar
    'CAD': 'CAUS',  # Canadian Dollar
    'CHF': 'SZUS',  # Swiss Franc
    'CNY': 'CHUS',  # Chinese Yuan
    'NZD': 'USNZ',  # New Zealand Dollar
    'SGD': 'SIUS',  # Singapore Dollar
    'HKD': 'HKUS',  # Hong Kong Dollar
    'INR': 'INUS',  # Indian Rupee
    'MXN': 'MXUS',  # Mexican Peso
    'ZAR': 'SFUS'   # South African Rand
}

def save_rates_to_json(rates):
    """Saves the exchange rates to a JSON file."""
    filename = f"data/exchange_rates/{datetime.now().date()}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(rates, f)

def load_rates_from_json():
    """Loads exchange rates from a JSON file if it exists."""
    filename = f"data/exchange_rates/{datetime.now().date()}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def fetch_latest_exchange_rates(currency_mapping=CURRENCY_MAPPING):
    """Fetches the latest exchange rates for given currencies against USD."""
    rates = {"USD": 1}
    
    # First, check if rates are already available in the JSON file
    existing_rates = load_rates_from_json()
    if existing_rates:
        return existing_rates  # Return the existing rates if found

    for currency in currency_mapping:
        if currency != "USD":
            try:
                # Fetch the latest exchange rate from FRED
                exchange_rate = web.get_data_fred(f'DEX{currency_mapping[currency]}').iloc[-1]
                if currency in {'EUR', 'NZD', 'GPB'}:
                    rates[currency] = round(1/exchange_rate.iloc[0], 4)  # Get the latest rate
                else:
                    rates[currency] = exchange_rate.iloc[0]  # Get the latest rate
                    
            except Exception as e:
                print(f"Error fetching exchange rate for {currency}: {e}")

    # Save the fetched rates to a JSON file
    save_rates_to_json(rates)
    return rates

def convert_to_base_currency(prices, rates, from_currency='USD', to_currency='USD'):
    """Converts a series of prices to the selected base currency using exchange rates.
    
    Args:
        prices (pd.Series or float): The prices to convert.
        rates (dict): A dictionary containing exchange rates.
        from_currency (str): The currency of the input prices (default is 'USD').
        to_currency (str): The target currency to convert to (default is 'USD').

    Returns:
        pd.Series or float: Converted prices in the target currency.
    """
    if from_currency == to_currency:
        return prices  # No conversion needed

    if from_currency == 'USD':
        # Convert from USD to the target currency
        exchange_rate = rates.get(to_currency, 1)  # Use rate or default to 1 if not found
        return prices * exchange_rate  # Convert from USD to the base currency

    elif to_currency == 'USD':
        # Convert from any currency to USD
        exchange_rate = rates.get(from_currency, 1)  # Use rate or default to 1 if not found
        return prices / exchange_rate  # Convert to USD

    else:
        # Convert from one currency to another (not involving USD)
        from_rate = rates.get(from_currency, 1)  # Get the from currency rate, default to 1
        to_rate = rates.get(to_currency, 1)      # Get the to currency rate, default to 1
        return (prices / from_rate) * to_rate  # Convert from from_currency to to_currency


