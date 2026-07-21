"""
StockBacktest Pro
Update Taiwan Stock Data
"""

import os
from services import data_provider
import services.stock_list as stock_list

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
    symbols = stock_list.get_stocks_only()

    success = 0
    failed = 0

    for symbol in symbols:

        try:

            df = data_provider.download_stock(symbol)

            save_path = os.path.join(
                folder,
                f"{symbol}.csv"
            )

            df.to_csv(save_path)

            success += 1

            print(f"✓ {symbol} 完成 ({len(df)} 筆)")

        except Exception as e:

            failed += 1

            print(f"✗ {symbol} 失敗：{e}")

    total = success + failed

    print()
    print("=" * 40)
    print("Update Finished")
    print("=" * 40)
    print(f"Total   : {total}")
    print(f"Success : {success}")
    print(f"Failed  : {failed}")


if __name__ == "__main__":

   update_all_data()