import pandas as pd
import config


def generate_signal(df):

    fast_name = f"EMA{config.FAST_EMA}"
    slow_name = f"EMA{config.SLOW_EMA}"

    trend = (
        df[fast_name] > df[slow_name]
    )

    # 昨天是否也是多頭排列
    prev = trend.shift(1, fill_value=False)

    # 只有今天第一次變成 True 才買
    df["BUY"] = trend & (~prev)
    df["SELL"] = (
    (df[fast_name] < df[slow_name]) &
    (df[fast_name].shift(1) >= df[slow_name].shift(1))
)

    return df