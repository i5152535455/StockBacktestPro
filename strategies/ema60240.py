import config
from utils import indicators

"""
EMA 60/240 Strategy
"""


def get_info():
    return {
        "name": "EMA",
        "version": "1.0",
        "description": "EMA60 / EMA240 Cross"
    }


def prepare(df):
    """
    計算策略需要的 EMA
    """

    df = indicators.calculate_ema(df)

    return df


def generate_signal(df):

    fast_name = f"EMA{config.FAST_EMA}"
    slow_name = f"EMA{config.SLOW_EMA}"

    # ======================================
    # EMA 多空位置
    # ======================================

    fast_above = df[fast_name] > df[slow_name]
    fast_below = df[fast_name] <= df[slow_name]

    # ======================================
    # BUY
    # CROSS 模式：
    #
    # 前一根：
    # EMA60 <= EMA240
    #
    # 現在：
    # EMA60 > EMA240
    #
    # 才算真正黃金交叉
    # ======================================

    if config.BUY_MODE == "CROSS":

        df["BUY"] = (
            fast_above
            & fast_below.shift(1, fill_value=True)
        )

    elif config.BUY_MODE == "TREND":

        df["BUY"] = fast_above

    else:

        raise ValueError(
            "BUY_MODE 必須是 CROSS 或 TREND"
        )

    # ======================================
    # SELL
    # 跌破 EXIT_EMA 出場
    # ======================================

    exit_name = f"EMA{config.EXIT_EMA}"

    df["SELL"] = (
        df["Close"] < df[exit_name]
    )

    df["EXIT_REASON"] = ""

    df.loc[
        df["SELL"],
        "EXIT_REASON"
    ] = f"{exit_name} Exit"

    return df