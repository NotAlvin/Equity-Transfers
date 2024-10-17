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

def fetch_latest_exchange_rates(currencies, currency_mapping=CURRENCY_MAPPING):
    """Fetches the latest exchange rates for given currencies against USD."""
    rates = {"USD": 1}
    
    # First, check if rates are already available in the JSON file
    existing_rates = load_rates_from_json()
    if existing_rates:
        return existing_rates  # Return the existing rates if found

    for currency in currencies:
        if currency != "USD":
            try:
                # Fetch the latest exchange rate from FRED
                exchange_rate = web.get_data_fred(f'DEX{currency_mapping[currency]}').iloc[-1]
                rates[currency] = exchange_rate.iloc[0]  # Get the latest rate
            except Exception as e:
                print(f"Error fetching exchange rate for {currency}: {e}")

    # Save the fetched rates to a JSON file
    save_rates_to_json(rates)
    
    return rates

def convert_to_usd(amounts, rates):
    """Converts amounts in different currencies to USD."""
    usd_values = {}
    for currency, amount in amounts.items():
        if currency in rates:
            usd_values[currency] = amount * rates[currency]
        else:
            print(f"No exchange rate available for {currency}.")
    return usd_values
