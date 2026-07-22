import pandas as pd
import config


"""
EMA 60/240 Strategy
"""

import config


def prepare(df):
    """
    準備策略需要的資料

    如果策略需要自己計算 MACD、ATR、
    SuperTrend...等等，就放這裡。

    EMA60240 目前不用做任何事。
    """

    return df

def generate_signal(df):

    fast_name = f"EMA{config.FAST_EMA}"
    slow_name = f"EMA{config.SLOW_EMA}"

    # 多頭排列
    trend = (
        df[fast_name] > df[slow_name]
    )

    # ===========================
    # BUY
    # ===========================
    if config.BUY_MODE == "TREND":

        # 黃金交叉
        prev = trend.shift(1, fill_value=False)
        df["BUY"] = trend & (~prev)

    elif config.BUY_MODE == "CROSS":

        # 只要多頭排列就買
        df["BUY"] = trend

    else:
        raise ValueError("BUY_MODE 設定錯誤")

    # ===========================
    # SELL
    # ===========================
    df["SELL"] = (
    df["Close"] < df[f"EMA{config.EXIT_EMA}"]
    )

    return df