from surmount.base_class import Strategy, TargetAllocation
from surmount.data import SocialSentiment, Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # Focused on Apple for this strategy
        # Social sentiment data for sentiment analysis
        self.data_list = [SocialSentiment(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"  # Using daily data for analysis

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            allocation = 0  # Default allocation
            
            # Social sentiment analysis for bullish or bearish sentiment
            sentiment_data = data.get(("social_sentiment", ticker), [])
            if sentiment_data and "twitterSentiment" in sentiment_data[-1]:
                sentiment_score = sentiment_data[-1]["twitterSentiment"]

                # Trading volume analysis for activity increase
                volume_data = data.get("ohlcv", [])
                if volume_data:
                    current_volume = volume_data[-1][ticker]["volume"]
                    previous_volume = volume_data[-2][ticker]["volume"] if len(volume_data) > 1 else current_volume
                    
                    # Check for positive sentiment and significant volume increase (more than 10% increase)
                    if sentiment_score > 0.5 and current_volume > 1.1 * previous_volume:
                        allocation = 1  # Full allocation if conditions are met
            
            # Setting the allocation for the ticker
            allocation_dict[ticker] = allocation

        return TargetAllocation(allocation_dict)