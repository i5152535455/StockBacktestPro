import os
import pandas as pd
import config

from services.backtest_service import run


# ======================================
# Scanner Settings
# ======================================

folder = "data/TW"

results = []

print("========== Stock Scanner ==========")
print(f"Timeframe : {config.TIMEFRAME}")
print(f"Fast EMA  : {config.FAST_EMA}")
print(f"Slow EMA  : {config.SLOW_EMA}")
print(f"Buy Mode  : {config.BUY_MODE}")
print()


# ======================================
# 暫時關閉詳細輸出
# ======================================

original_verbose = config.VERBOSE
config.VERBOSE = False


# ======================================
# Scan all stocks
# ======================================

for file in os.listdir(folder):

    if not file.endswith(".csv"):
        continue


    filepath = os.path.join(folder, file)

    stock = file.replace(".csv", "")

    print(f"讀取：{filepath}")

    try:

        # ==================================
        # 使用正式 Backtest Service
        # ==================================

        result = run(filepath)

        metrics = result["metrics"]
        trades = result["trades"]

        print()
        print("========== DEBUG TRADES ==========")
        print(trades)
        print()
        print("Total Profit Amount:")
        print(trades["Profit Amount"].sum())

        # ==================================
        # 沒有交易
        # ==================================

        if metrics["Trades"] == 0:

            print(f"{stock} 無交易")

            continue

        # ==================================
        # 取得交易日期
        # ==================================

        trade_periods = []

        for trade in trades:

            try:

                buy_date = pd.to_datetime(
                    trade["Buy Date"]
                ).strftime("%Y-%m-%d")

                sell_date = pd.to_datetime(
                    trade["Sell Date"]
                ).strftime("%Y-%m-%d")

                trade_periods.append(
                    f"{buy_date} → {sell_date}"
                )

            except Exception:

                pass

        trade_period = " | ".join(
            trade_periods
        )

        # ==================================
        # 儲存結果
        # ==================================

        results.append({

            "Stock":
                stock,

            "ROI":
                round(
                    metrics["ROI"],
                    2
                ),

            "Max Drawdown":
                round(
                    metrics["Max Drawdown"],
                    2
                ),

            "Trades":
                metrics["Trades"],

            "Win Rate":
                round(
                    metrics["Win Rate"],
                    2
                ),

            "Profit Factor":
                round(
                    metrics["Profit Factor"],
                    2
                ),

            "Net Profit": round(metrics["Net Profit"], 0),
            "Final Capital": round(metrics["Final Capital"], 0),

            "Final Capital":
                metrics["Final Capital"],

            "Trade Period":
                trade_period

        })

        print(
            f"{stock} "
            f"ROI={metrics['ROI']:.2f}% "
            f"DD={metrics['Max Drawdown']:.2f}% "
            f"Trades={metrics['Trades']}"
        )

    except Exception as e:

        print(
            f"{file} 發生錯誤：{e}"
        )


# ======================================
# 恢復 VERBOSE
# ======================================

config.VERBOSE = original_verbose


# ======================================
# 建立 DataFrame
# ======================================

results_df = pd.DataFrame(results)


if results_df.empty:

    print()
    print("沒有任何股票產生交易。")

else:

    # ==================================
    # ROI 排名
    # ==================================

    results_df = results_df.sort_values(
        by="ROI",
        ascending=False
    ).reset_index(drop=True)

    results_df.insert(
        0,
        "Rank",
        range(
            1,
            len(results_df) + 1
        )
    )

    # ==================================
    # 顯示結果
    # ==================================

    print()
    print(
        "========== ALL STOCKS RANKING =========="
    )

    print(
        results_df.to_string(
            index=False
        )
    )

    # ==================================
    # 儲存
    # ==================================

    os.makedirs(
        "output",
        exist_ok=True
    )

    results_df.to_csv(
        "output/scanner_result.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print(
        "已輸出：output/scanner_result.csv"
    )