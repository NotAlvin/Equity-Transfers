from pydantic import BaseModel, Field
from typing import Optional
import pandas as pd

class Equity(BaseModel):
    isin: Optional[str] = Field(default=None, description='ISIN of the equity', example='US9311421039')
    ticker: Optional[str] = Field(default=None, description='Ticker of the equity', example='WMT')
    name: Optional[str] = Field(default=None, description='Name of the equity', example='Walmart')
    currency: Optional[str] = Field(default=None, description='Currency of the equity', example='USD')
    latest_price: Optional[float] = Field(default=None, description='Latest market price of the equity', example=150.25)
    historical_prices: Optional[dict[int, float]] = Field(default=None, description='Dictionary of historical prices by date (timestamp as int)')
    shares_held: Optional[float] = Field(default=None, description='Number of shares held for this equity', example=100.0)
    vesting_date: Optional[int] = Field(default=None, description='Date when the shares are set to vest, timestamp is number of seconds since 1970-01-01', example=1545730073)

    def calculate_value(self, method: str = "latest") -> Optional[float]:
        """Calculates the total value of the equity based on shares held and different price methods."""
        if not self.shares_held:
            return None

        # Convert historical_prices dict to DataFrame for easier manipulation
        historical_df = self._get_historical_prices_df()

        if method == "latest":
            return self.shares_held * self.latest_price if self.latest_price else None

        elif method == "average" and not historical_df.empty:
            # Calculate average price over the last 180 days
            last_180_days = historical_df.tail(180)
            if last_180_days.empty:
                return None
            avg_price_180_days = last_180_days['price'].mean()
            return self.shares_held * avg_price_180_days

        elif method == "moving_average" and self.vesting_date:
            # Calculate the 180-day moving average leading up to the vesting date
            historical_df['moving_avg'] = historical_df['price'].rolling(window=180).mean()

            # Convert vesting date from timestamp to datetime
            vesting_date_dt = pd.to_datetime(self.vesting_date, unit='s')

            # Get relevant prices leading up to the vesting date
            relevant_prices = historical_df[historical_df.index < vesting_date_dt]

            if relevant_prices.empty:
                return None  # No relevant prices available

            # If we have enough data points, calculate the extrapolated price
            if len(relevant_prices) >= 180:
                # Use the last moving average value
                moving_avg_value = relevant_prices['moving_avg'].iloc[-1]
                return self.shares_held * moving_avg_value if pd.notna(moving_avg_value) else None
            else:
                return None  # Not enough data to calculate the moving average

        return None


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