import pandas as pd
import config_ema60240 as config


def load_data(filepath):

    df = pd.read_csv(filepath, header=[0,1], index_col=0)

    # 把第二層欄位去掉
    df.columns = df.columns.get_level_values(0)

    # 將索引(Date)變成真正欄位
    df = df.reset_index()

    # 第一欄改名
    df.rename(columns={"index": "Date"}, inplace=True)

    # 日期格式
    df["Date"] = pd.to_datetime(df["Date"])

    return df

def convert_timeframe(df):

    if config.TIMEFRAME == "D":
        return df

    rule = {
        "W": "W-FRI",
        "M": "ME"
    }

    if config.TIMEFRAME not in rule:
        raise ValueError("TIMEFRAME 必須是 D、W 或 M")

    df = df.copy()

    df = df.set_index("Date")

    df = df.resample(rule[config.TIMEFRAME]).agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    df = df.dropna()

    df = df.reset_index()

    return df

def calculate_ema(df):

    fast_name = f"EMA{config.FAST_EMA}"
    slow_name = f"EMA{config.SLOW_EMA}"

    df[fast_name] = (
        df["Close"]
        .ewm(span=config.FAST_EMA, adjust=False)
        .mean()
    )

    df[slow_name] = (
        df["Close"]
        .ewm(span=config.SLOW_EMA, adjust=False)
        .mean()
    )

    return df