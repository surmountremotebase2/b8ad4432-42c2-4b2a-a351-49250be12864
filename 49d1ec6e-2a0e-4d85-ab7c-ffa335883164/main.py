from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import InsiderTrading, BankPrimeLoanRate

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT"]  # Target stocks
        # Include both economic indicators and stock-specific data in data_list.
        self.data_list = [BankPrimeLoanRate()] + [InsiderTrading(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        # Daily data fits economic indicators and insider trading data analysis.
        return "1day"

    @property
    def assets(self):
        # This strategy targets AAPL and MSFT.
        return self.tickers

    @property
    def data(self):
        # Include the data_list defined in __init__.
        return self.data_list

    def run(self, data):
        # Start with an even split allocation as a base, can be adjusted based on strategy needs.
        allocation_dict = {ticker: 0.5 for ticker in self.tickers}
        prime_rate_data = data[("bank_prime_loan_rate",)]
        
        # Analyze latest prime rate to adjust overall market stance. Lower rates often indicate a more bullish stance.
        if prime_rate_data and prime_rate_data[-1]["value"] > 3.25:  # Example threshold for bullish/bearish stance.
            allocation_dict = {ticker: 0.25 for ticker in self.tickers}  # Reduce allocation in higher prime rate scenarios.
        
        # Loop through insider trading data for each ticker.
        for ticker in self.tickers:
            insider_trades = data[("insider_trading", ticker)]
            if insider_trades:
                # Check the latest insider transaction for the stock.
                latest_trade = insider_trades[-1]
                if "Sale" in latest_trade['transactionType']:
                    # Insider selling might indicate negative outlook, reduce allocation.
                    allocation_dict[ticker] *= 0.5  # Halve the allocation if there's a recent insider sale.

        # Ensure allocations are within 0 and 1.
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {ticker: alloc / total_allocation for ticker, alloc in allocation_dict.items()}

        return TargetAllocation(allocation_dict)