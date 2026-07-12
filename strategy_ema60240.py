import pandas as pd
import config


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
    df["SELL"] = False

    return df