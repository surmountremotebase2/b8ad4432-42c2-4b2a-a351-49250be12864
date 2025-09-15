from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InsiderTrading, SocialSentiment

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker we're interested in
        self.ticker = "AAPL"
        # Add InsiderTrading and SocialSentiment to the data list for AAPL
        self.data_list = [InsiderTrading(self.ticker), SocialSentiment(self.ticker)]

    @property
    def interval(self):
        # Define the interval for data. Given the nature of our strategy, "1day" makes the most sense
        return "1day"
    
    @property
    def assets(self):
        # Specify the assets that this strategy will trade
        return [self.ticker]

    def run(self, data):
        # Initialize target allocation for AAPL to 0
        allocation = {self.ticker: 0}
        
        # Analyze insider trading data for buy transactions
        insider_buying = False
        for trade in data[("insider_trading", self.ticker)]:
            if trade['transactionType'].lower().startswith("p"):  # Purchase transactions start with "P"
                insider_buying = True
                break

        # Analyze social sentiment data for positive sentiment
        social_sentiment_positive = False
        latest_sentiment = data[("social_sentiment", self.ticker)][-1]  # Get the latest sentiment
        if latest_sentiment['stocktwitsSentiment'] > 0.5 and latest_sentiment['twitterSentiment'] > 0.5:
            social_sentiment_positive = True

        # If both conditions are met, allocate a portion of the portfolio to AAPL
        if insider_buying and social_sentiment_positive:
            allocation[self.ticker] = 0.5  # Allocate 50% to AAPL if both insider buying and positive sentiment are detected

        return TargetAllocation(allocation)