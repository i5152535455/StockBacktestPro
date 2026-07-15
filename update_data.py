"""
StockBacktest Pro
Update Taiwan Stock Data
"""

import os
import data_provider
import stock_list

def update_all_data():

    print("=" * 40)
    print("StockBacktest Pro")
    print("Update Taiwan Stock Data")
    print("=" * 40)

    folder = "data/TW"

    if not os.path.exists(folder):
        os.makedirs(folder)

    print("Data folder:", folder)

    print()
    symbols = stock_list.get_tw_stocks()

    for symbol in symbols:

        df = data_provider.download_stock(symbol)

        save_path = os.path.join(
            folder,
            f"{symbol}.csv"
        )

        df.to_csv(save_path)

        print(f"{symbol} 完成 ({len(df)} 筆)")


if __name__ == "__main__":

    update_all_data()