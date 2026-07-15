"""
Data Provider
下載股票資料
"""

import yfinance as yf


def download_stock(symbol, market="TW"):

    if market == "TW":
        ticker = f"{symbol}.TW"
    else:
        ticker = symbol

    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        start="2020-01-01",
        auto_adjust=True,
        progress=False
    )

    df = yf.download(
        ticker,
        start="2020-01-01",
        auto_adjust=True,
        progress=False
    )

    # yfinance 新版會回傳 MultiIndex，轉成單層欄位
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)
    # 移除欄位名稱 Price
    df.columns.name = None
    return df