from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class EMAMomentumStrategy(Strategy):
    def __init__(self):
        self._assets = ["SPY", "QQQ", "AAPL"]
        self._interval = "1day"
    
    @property
    def assets(self):
        return self._assets
    
    @property
    def interval(self):
        return self._interval
    
    @property
    def data(self):
        # No additional data sources are required for this strategy.
        return []
    
    def run(self, data):
        # Initial allocation dictionary with zero allocation
        allocation_dict = {asset: 0.0 for asset in self.assets}
        
        for asset in self.assets:
            if asset in data["ohlcv"]:  # Check if OHLCV data is available for the asset
                ohlcv = data["ohlcv"][asset]
                short_ema = EMA(asset, ohlcv, length=12)  # Calculate 12-day EMA
                long_ema = EMA(asset, ohlcv, length=26)  # Calculate 26-day EMA
                
                if short_ema is not None and long_ema is not None:
                    # Check the last (most recent) values of both EMAs to decide on the position
                    if short_ema[-1] > long_ema[-1]:
                        # Short-term momentum is stronger than long-term, suggesting bullish sentiment
                        allocation_dict[asset] = 1 / len(self.assets)  # Allocate evenly across assets
                    else:
                        # Bearish sentiment or lack of strong momentum; no allocation for this asset
                        allocation_dict[asset] = 0.0
                else:
                    log(f"Insufficient data to calculate EMAs for {asset}. Skipping.")
            else:
                log(f"No OHLCV data available for {asset}. Skipping.")
            
        return TargetAllocation(allocation_dict)

# Note: Be sure to test this strategy on a development environment with historical data to ensure it behaves as expected, and adjust parameters or logic as necessary.