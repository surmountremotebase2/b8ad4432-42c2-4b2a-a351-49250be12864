from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import SocialSentiment, GDPAllCountries, Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"
        # Add necessary data sources to the data_list
        self.data_list = [SocialSentiment(self.ticker), GDPAllCountries(), Asset(self.ticker)]
    
    @property
    def interval(self):
        # Using daily data for analysis
        return "1day"
    
    @property
    def assets(self):
        # Focusing the strategy on Apple stocks
        return [self.ticker]
    
    @property
    def data(self):
        return self.data_list
    
    def run(self, data):
        allocation = 0  # Default to no position
        
        # Access the required data from the data dictionary
        social_sentiment = data[("social_sentiment", self.ticker)]
        gdp_data = data[("gdp_by_country",)]
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14)
        
        # Ensure there is enough data to make a decision
        if social_sentiment and gdp_data and rsi_values:
            latest_sentiment = social_sentiment[-1]['twitterSentiment']
            previous_sentiment = social_sentiment[-2]['twitterSentiment'] if len(social_sentiment) > 1 else latest_sentiment
            sentiment_improved = latest_sentiment > previous_sentiment
            
            # Assuming the latest GDP entry is the most recent data point
            latest_gdp_growth = gdp_data[-1]['value']
            previous_gdp_growth = gdp_data[-2]['value'] if len(gdp_data) > 1 else latest_gdp_growth
            gdp_growing = latest_gdp_growth > previous_gdp_growth
            
            # Check if RSI indicates overbought or oversold
            latest_rsi = rsi_values[-1]
            oversold = latest_rsi < 30
            overbought = latest_rsi > 70
            
            # Define the trading logic based on conditions
            if sentiment_improved and gdp_growing and oversold:
                allocation = 1  # Full allocation to go long
            elif not sentiment_improved and not gdp_growing and overbought:
                allocation = 0  # No allocation, equivalent to going short or not holding
            
        return TargetAllocation({self.ticker: allocation})