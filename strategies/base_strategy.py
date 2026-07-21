class BaseStrategy:
    """
    Base class for all trading strategies.
    Every strategy should inherit from this class.
    """

    def generate_signal(self, df):
        """
        Generate buy/sell signals.
        """
        raise NotImplementedError(
            "generate_signal() must be implemented by the strategy."
        )