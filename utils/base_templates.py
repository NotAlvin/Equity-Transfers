from datetime import datetime, timedelta
from typing import Optional, Dict
import pandas as pd
from pydantic import BaseModel, Field


class Equity(BaseModel):
    isin: Optional[str] = Field(
        default=None, description='ISIN of the equity', example='US9311421039'
    )
    ticker: Optional[str] = Field(
        default=None, description='Ticker of the equity', example='WMT'
    )
    name: Optional[str] = Field(
        default=None, description='Name of the equity', example='Walmart'
    )
    currency: Optional[str] = Field(
        default=None, description='Currency of the equity', example='USD'
    )
    latest_price: Optional[float] = Field(
        default=None, description='Latest market price of the equity', example=150.25
    )
    historical_prices: Optional[Dict[str, float]] = Field(
        default=None, description='Dictionary of historical prices of the equity by date (YYYY-MM-DD)'
    )
    shares_held: Optional[float] = Field(
        default=None, description='Number of shares held for this equity', example=100.0
    )
    vesting_date: Optional[datetime] = Field(
        default=None, description='Date when the shares are set to vest', example='2024-12-31'
    )

    def calculate_value(self, method: str = "latest") -> Optional[float]:
        """
        Calculates the total value of the equity based on shares held and different price methods.
        
        Methods:
        - 'latest': Use the latest price to calculate the value.
        - 'average': Use the average price from the past 180 days.
        - 'moving_average': Use a 180-day moving average up to the vesting date.
        """
        if not self.shares_held:
            return None

        if method == "latest":
            # Method 1: Use the latest price
            return self.shares_held * self.latest_price if self.latest_price else None

        elif method == "average" and self.historical_prices:
            # Method 2: Use the average price of the past 180 days
            historical_df = self._get_historical_prices_df()
            if historical_df is None:
                return None
            # Calculate the average price of the past 180 days
            last_180_days = historical_df.tail(180)  # Assuming prices are sorted by date
            avg_price_180_days = last_180_days['price'].mean()
            return self.shares_held * avg_price_180_days

        elif method == "moving_average" and self.historical_prices and self.vesting_date:
            # Method 3: Use a 180-day moving average leading up to the vesting date
            historical_df = self._get_historical_prices_df()
            if historical_df is None:
                return None
            # Calculate the 180-day moving average up to the vesting date
            historical_df['moving_avg'] = historical_df['price'].rolling(window=180).mean()
            # Get the moving average price on the vesting date
            vesting_str = self.vesting_date.strftime('%Y-%m-%d')
            if vesting_str in historical_df.index:
                price_on_vesting = historical_df.loc[vesting_str, 'moving_avg']
                return self.shares_held * price_on_vesting
            else:
                return None  # Vesting date out of range of historical data

        return None

    def _get_historical_prices_df(self) -> Optional[pd.DataFrame]:
        """Helper method to convert historical prices dict into a DataFrame."""
        if not self.historical_prices:
            return None
        # Convert historical_prices (dict) to DataFrame
        prices_df = pd.DataFrame(
            list(self.historical_prices.items()), columns=["date", "price"]
        )
        prices_df["date"] = pd.to_datetime(prices_df["date"])
        prices_df.set_index("date", inplace=True)
        return prices_df.sort_index()  # Ensure the data is sorted by date


class Portfolio(BaseModel):
    name: str = Field(
        default = None,
        description='Name of the portfolio'
    )
    equities: dict[str, Equity] = Field(
        default_factory=dict, 
        description='Dictionary of equities with ticker as key'
    )
    def to_json(self):
        return self.json(indent=4)  # Converts the portfolio to a JSON string with indentation for readability