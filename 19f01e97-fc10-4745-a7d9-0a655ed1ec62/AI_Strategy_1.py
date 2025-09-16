from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, MACD

class MACDEMAStrategy(Strategy):

    def __init__(self):
        self._assets = ["AAPL", "MSFT", "GOOGL"]
        self._interval = "1day"

    @property
    def assets(self):
        return self._assets

    @property
    def interval(self):
        return self._interval

    @property
    def data(self):
        # No additional data sources needed for this strategy
        return []

    def run(self, data):
        # Default allocation for each asset is 0
        allocation_dict = {asset: 0 for asset in self.assets}

        for asset in self.assets:
            # Retrieve OHLCV data for the asset
            ohlcv_data = data["ohlcv"]

            # Calculate MACD and EMA for each asset
            macd_data = MACD(asset, ohlcv_data, fast=12, slow=26)
            ema_data = EMA(asset, ohlcv_data, length=9)

            if not macd_data or not ema_data:
                # Skip if there's insufficient data to compute MACD or EMA
                continue

            # Latest MACD and signal line values
            latest_macd = macd_data["MACD"][-1]
            latest_signal = macd_data["signal"][-1]
            latest_ema = ema_data[-1]
            current_price = ohlcv_data[-1][asset]['close']

            # Trading logic
            if latest_macd > latest_signal and current_price > latest_ema:
                # If MACD crosses above the signal line and current price is above EMA, we consider this a buy signal.
                allocation_dict[asset] = 1.0 / len(self.assets)
            elif latest_macd < latest_signal and current_price < latest_ema:
                # If MACD crosses below the signal line and current price is below EMA, we might consider selling but here we set the allocation to 0 as placeholder.
                allocation_dict[asset] = 0

        # Return allocation dictionary converted to TargetAllocation object
        return TargetAllocation(allocation_dict)

# To use this strategy, instantiate it and call the run method with the appropriate market data.