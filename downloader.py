import os
import yfinance as yf
import config


def download_data():

    ticker = "2330.TW"

    print(f"開始下載 {ticker}")

    df = yf.download(
        ticker,
        start=config.START_DATE,
        end=config.END_DATE,
        auto_adjust=True
    )

    if df.empty:
        print("下載失敗")
        return

    # ===== 把新版 MultiIndex 轉成一般欄位 =====
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

    # Date 變成一般欄位
    df.reset_index(inplace=True)

    save_path = os.path.join("data", "TW", "2330.csv")

    df.to_csv(save_path, index=False)

    print("下載完成")
    print(save_path)