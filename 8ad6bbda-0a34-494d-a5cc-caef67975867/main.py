from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import Asset, InstitutionalOwnership, BankPrimeLoanRate
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        self.data_list = [
            InstitutionalOwnership("AAPL"),
            BankPrimeLoanRate(),
        ]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        current_price = data["ohlcv"][-1]["AAPL"]["close"]
        sma_50_day = SMA("AAPL", data["ohlcv"], 50)[-1]
        rsi_value = RSI("AAPL", data["ohlcv"], 14)[-1]
        institutional_ownership_current = data[("institutional_ownership", "AAPL")][-1]["investorsHoldingChange"]
        prime_rate_current = data[("bank_prime_loan_rate",)][-1]["value"]
        prime_rate_previous = data[("bank_prime_loan_rate",)][-2]["value"]

        aapl_stake = 0

        # Check if current price is above the 50-day SMA and RSI is in desired range
        if current_price > sma_50_day and 40 < rsi_value < 60:
            # Check if institutional ownership is increasing and the prime rate is steady or falling
            if institutional_ownership_current > 0 and prime_rate_current <= prime_rate_previous:
                aapl_stake = 0.5  # Allocate 50% as an example allocation

        log(f"AAPL Allocation: {aapl_stake}")
        
        return TargetAllocation({"AAPL": aapl_stake})