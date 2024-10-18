import pandas as pd

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class VestingEvent(BaseModel):
    vesting_date: int = Field(description='Vesting date as timestamp')
    shares_vested: float = Field(description='Number of shares vested on this date')

class Equity(BaseModel):
    isin: Optional[str] = Field(default=None, description='ISIN of the equity', example='US9311421039')
    ticker: Optional[str] = Field(default=None, description='Ticker of the equity', example='WMT')
    name: Optional[str] = Field(default=None, description='Name of the equity', example='Walmart')
    currency: Optional[str] = Field(default=None, description='Currency of the equity', example='USD')
    latest_price: Optional[float] = Field(default=None, description='Latest market price of the equity', example=150.25)
    historical_prices: Optional[Dict[int, float]] = Field(default=None, description='Dictionary of historical prices by date (timestamp as int)')
    vesting_events: List[VestingEvent] = Field(default=[], description='List of vesting events for the equity')

    def calculate_value(self, method: str = "average") -> Optional[float]:
        """Calculates the total value of the equity based on vesting events and different price methods."""
        if not self.vesting_events:
            return None

        # Convert historical_prices dict to DataFrame for easier manipulation
        historical_df = self._get_historical_prices_df()

        total_value = 0

        for event in self.vesting_events:
            shares_vested = event.shares_vested

            if method == "latest":
                total_value += shares_vested * self.latest_price if self.latest_price else 0

            elif method == "average" and not historical_df.empty:
                # Calculate average price over the last 180 days
                last_180_days = historical_df.tail(180)
                if not last_180_days.empty:
                    avg_price_180_days = last_180_days['price'].mean()
                    total_value += shares_vested * avg_price_180_days

            elif method == "moving_average":
                # Calculate the 180-day moving average leading up to the vesting date
                historical_df['moving_avg'] = historical_df['price'].rolling(window=180).mean()

                # Convert vesting date from timestamp to datetime
                vesting_date_dt = pd.to_datetime(event.vesting_date, unit='s')

                # Get relevant prices leading up to the vesting date
                relevant_prices = historical_df[historical_df.index < vesting_date_dt]

                if not relevant_prices.empty and len(relevant_prices) >= 180:
                    # Use the last moving average value
                    moving_avg_value = relevant_prices['moving_avg'].iloc[-1]
                    total_value += shares_vested * moving_avg_value if pd.notna(moving_avg_value) else 0

        return total_value if total_value > 0 else None

    def _get_historical_prices_df(self) -> pd.DataFrame:
        """Helper method to convert historical prices (dictionary) into a DataFrame."""
        if not self.historical_prices:
            return pd.DataFrame()  # Return an empty DataFrame if no historical prices

        # Create DataFrame from historical prices dictionary
        prices_df = pd.DataFrame(list(self.historical_prices.items()), columns=["timestamp", "price"])
        prices_df["date"] = pd.to_datetime(prices_df["timestamp"], unit='s')  # Convert timestamp to datetime
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