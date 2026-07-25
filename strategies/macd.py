"""
MACD Trend Strategy
"""

import config
from utils import indicators

def get_info():
    return {
        "name": "MACD",
        "version": "1.0",
        "description": "EMA Trend + MACD Cross"
    }


def prepare(df):
    """
    Prepare indicators required by MACD strategy.
    """

    df = indicators.calculate_ema(df)
    df = indicators.calculate_macd(df)

    return df


def generate_signal(df):

    # ===========================
    # Trend Filter
    # ===========================

    trend = (
        df[f"EMA{config.FAST_EMA}"]
        >
        df[f"EMA{config.SLOW_EMA}"]
    )


    # ===========================
    # MACD Cross
    # ===========================

    golden_cross = (
        (df["MACD"] > df["MACD_SIGNAL"])
        &
        (
            df["MACD"].shift(1)
            <=
            df["MACD_SIGNAL"].shift(1)
        )
    )

    dead_cross = (
        (df["MACD"] < df["MACD_SIGNAL"])
        &
        (
            df["MACD"].shift(1)
            >=
            df["MACD_SIGNAL"].shift(1)
        )
    )

    # ===========================
    # BUY / SELL
    # ===========================

    df["BUY"] = trend & golden_cross

    df["SELL"] = dead_cross


    print(
    "BUY:",
    df["BUY"].sum(),
    "SELL:",
    df["SELL"].sum()
)

    df["EXIT_REASON"] = ""
    df.loc[df["SELL"], "EXIT_REASON"] = "MACD Exit"


    return df
