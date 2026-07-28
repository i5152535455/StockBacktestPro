import pandas as pd
import config
from utils import indicators

"""
EMA 60/240 Strategy
"""

def get_info():
    return {
        "name": "EMA",
        "version": "1.0",
        "description": "EMA60 / EMA240 Trend"
    }


def prepare(df):
    """
    準備策略需要的資料
    """

    df = indicators.calculate_ema(df)

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

    df["EXIT_REASON"] = ""
    df.loc[df["SELL"], "EXIT_REASON"] = "EMA60 Exit"


    return df