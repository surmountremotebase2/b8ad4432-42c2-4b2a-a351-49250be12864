from surmount.base_class import Strategy, TargetAllocation
from surmount.data import GDPAllCountries, ConsumerConfidence

class TradingStrategy(Strategy):
    def __init__(self):
        # We're interested in the US market, hence focusing on SPY
        self.tickers = ["SPY"]
        # Adding GDP and Consumer Confidence to our data list
        self.data_list = [GDPAllCountries(), ConsumerConfidence()]
    
    @property
    def interval(self):
        # Daily data is sufficient for this type of macroeconomic analysis
        return "1day"
    
    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initial allocation for SPY is set conservatively to 0
        spy_allocation = 0
        
        # Extracting the most recent GDP and Consumer Confidence data for the U.S.
        gdp_data = [record for record in data[("gdp_by_country",)] if record["country"] == "United States"]
        confidence_data = data[("consumer_confidence",)]
        
        if gdp_data and confidence_data:
            most_recent_gdp = gdp_data[-1]["value"]
            most_recent_confidence = confidence_data[-1]["value"]
            
            # Check conditions - we look for GDP growth and high consumer confidence as bullish signals
            if most_recent_gdp > gdp_data[-2]["value"] and most_recent_confidence > 100:
                # We consider it bullish and allocate 60% to SPY. The 60% is arbitrary and for demonstration.
                spy_allocation = 0.6
            else:
                # In cases of concern, keep the allocation at 0 (or could adjust to another conservative allocation)
                spy_allocation = 0

        return TargetAllocation({"SPY": spy_allocation})