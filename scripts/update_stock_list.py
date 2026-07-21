import requests
import pandas as pd
import os


def update_stock_list():

    print("=" * 40)
    print("Update Taiwan Stock List")
    print("=" * 40)

    folder = "data/metadata"

    if not os.path.exists(folder):
        os.makedirs(folder)

    url = (
        "https://openapi.twse.com.tw/v1/"
        "exchangeReport/STOCK_DAY_ALL"
    )

    print("Downloading TWSE stock list...")

    data = requests.get(url, timeout=30).json()

    df = pd.DataFrame(data)

        # 只保留需要的欄位
    df = df[["Code", "Name"]].copy()

    # 加上市場別
    df["Market"] = "TWSE"

    # 判斷類型
    df["Type"] = df["Code"].apply(
        lambda x: "Stock" if str(x).isdigit() and len(str(x)) == 4 else "ETF"
    )

    # 股票代號統一轉字串
    df["Code"] = df["Code"].astype(str)

    # 依股票代號排序
    df = df.sort_values("Code").reset_index(drop=True)

    print(df.head())
    print(f"\n共 {len(df)} 筆")

    save_path = os.path.join(
        folder,
        "tw_stock_list.csv"
    )

    df.to_csv(save_path, index=False, encoding="utf-8-sig")

    print(f"\nSaved: {save_path}")


if __name__ == "__main__":
    update_stock_list()