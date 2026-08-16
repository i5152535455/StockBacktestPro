import os
import glob
import pandas as pd

import config
from services.backtest_service import run


# ======================================
# Market Optimizer Settings
# ======================================

DATA_FOLDER = "data/TW"
OUTPUT_FILE = "output/TW_market_ranking.csv"


# ======================================
# 固定策略參數
# ======================================

FAST_EMA = 60
SLOW_EMA = 200

# EMA CROSS
BUY_MODE = "CROSS"

# 跌破 Fast EMA 出場
EXIT_EMA = FAST_EMA


# ======================================
# 儲存原本設定
# ======================================

original_fast = config.FAST_EMA
original_slow = config.SLOW_EMA
original_exit_ema = config.EXIT_EMA
original_buy_mode = config.BUY_MODE
original_strategy = config.STRATEGY
original_verbose = config.VERBOSE


# ======================================
# 強制設定
# ======================================

config.FAST_EMA = FAST_EMA
config.SLOW_EMA = SLOW_EMA
config.EXIT_EMA = EXIT_EMA

config.BUY_MODE = BUY_MODE
config.STRATEGY = "ema60240"

# 非常重要：
# 不要讓每支股票把交易過程全部印出來
config.VERBOSE = False


# ======================================
# 找出所有台股 CSV
# ======================================

files = glob.glob(
    os.path.join(DATA_FOLDER, "*.csv")
)

files.sort()


print()
print("======================================")
print("      TW Market EMA CROSS Backtest")
print("======================================")
print()
print(f"Strategy : EMA{FAST_EMA}/{SLOW_EMA}")
print(f"Buy Mode : {BUY_MODE}")
print(f"Exit EMA : EMA{EXIT_EMA}")
print(f"Stocks   : {len(files)}")
print()


# ======================================
# 開始回測
# ======================================

results = []

total = len(files)

for i, filepath in enumerate(files, start=1):

    filename = os.path.basename(filepath)

    # 例如 2330.csv → 2330
    code = os.path.splitext(filename)[0]

    print(
        f"[{i}/{total}] {code}",
        end="\r"
    )

    try:

        result = run(filepath)

        metrics = result["metrics"]
        trades = result["trades"]

        print()
        print("========== DEBUG TRADES ==========")
        print(trades)
        print()
        print("Total Profit Amount:")
        print(trades["Profit Amount"].sum())

# ======================================
# 整理交易日期
# ======================================

        trade_dates = []

        if not trades.empty:

            for _, trade in trades.iterrows():

                buy_date = pd.to_datetime(
                    trade["Buy Date"]
                ).strftime("%Y-%m-%d")

                sell_date = pd.to_datetime(
                    trade["Sell Date"]
                ).strftime("%Y-%m-%d")

                buy_price = float(
                    trade["Buy Price"]
                )

                sell_price = float(
                    trade["Sell Price"]
                )

                trade_dates.append(
                    f"{buy_date} @ {buy_price:.2f} → "
                    f"{sell_date} @ {sell_price:.2f} "
                    f"[{trade['Exit Reason']}]"
                )


        trade_dates_text = " | ".join(
            trade_dates
        )


        # ======================================
        # 儲存結果
        # ======================================

        results.append({

            "Code": code,

            "ROI": metrics["ROI"],

            "Max Drawdown":
                metrics["Max Drawdown"],

            "Trades":
                metrics["Trades"],

            "Win Rate":
                metrics["Win Rate"],

            "Profit Factor":
                metrics["Profit Factor"],

            "Net Profit":
                metrics["Net Profit"],

            "Final Capital":
                metrics["Final Capital"],

            "Trade Dates":
                trade_dates_text,

        })

    except Exception as e:

        print()

        print(
            f"[ERROR] {code}: {e}"
        )


# ======================================
# 還原 Config
# ======================================

config.FAST_EMA = original_fast
config.SLOW_EMA = original_slow
config.EXIT_EMA = original_exit_ema
config.BUY_MODE = original_buy_mode
config.STRATEGY = original_strategy
config.VERBOSE = original_verbose


# ======================================
# 建立結果
# ======================================

ranking = pd.DataFrame(results)


if ranking.empty:

    print()
    print("沒有任何股票成功完成回測。")

    raise SystemExit


# ======================================
# 排名
# ======================================

ranking = ranking.sort_values(
    by="ROI",
    ascending=False
).reset_index(drop=True)


# ======================================
# Rank
# ======================================

ranking.insert(
    0,
    "Rank",
    range(1, len(ranking) + 1)
)


# ======================================
# 四捨五入
# ======================================

ranking["ROI"] = ranking["ROI"].round(2)

ranking["Max Drawdown"] = (
    ranking["Max Drawdown"].round(2)
)

ranking["Win Rate"] = (
    ranking["Win Rate"].round(2)
)

ranking["Profit Factor"] = (
    ranking["Profit Factor"].round(2)
)

ranking["Net Profit"] = (
    ranking["Net Profit"].round(0)
)

ranking["Final Capital"] = (
    ranking["Final Capital"].round(0)
)


# ======================================
# 顯示前 30 名
# ======================================

print()
print()
print("======================================")
print("       TW MARKET RANKING")
print("======================================")
print()

print(
    ranking.head(30).to_string(
        index=False
    )
)


# ======================================
# 輸出 CSV
# ======================================

os.makedirs(
    "output",
    exist_ok=True
)

ranking.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ======================================
# 完成
# ======================================

print()
print("======================================")
print("回測完成")
print("======================================")
print()

print(
    f"成功回測股票：{len(ranking)}"
)

print(
    f"結果已輸出：{OUTPUT_FILE}"
)