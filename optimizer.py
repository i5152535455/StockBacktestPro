import os
import pandas as pd

import config
from services.backtest_service import run


# ======================================
# Optimizer Settings
# ======================================

filepath = "data/TW/2330.csv"


# Fast EMA
FAST_EMAS = [
    10,
    20,
    30,
    40,
    50,
    60,
    80,
    100,
]


# Slow EMA
SLOW_EMAS = [
    100,
    120,
    150,
    180,
    200,
    240,
    300,
    360,
]


# ======================================
# Save original settings
# ======================================

original_fast = config.FAST_EMA
original_slow = config.SLOW_EMA
original_exit_ema = config.EXIT_EMA
original_strategy = config.STRATEGY
original_buy_mode = config.BUY_MODE


# ======================================
# Optimization
# ======================================

results = []

# 強制使用 EMA CROSS 策略
config.STRATEGY = "ema60240"

# 強制使用真正黃金交叉
config.BUY_MODE = "CROSS"


for fast in FAST_EMAS:

    for slow in SLOW_EMAS:

        # ==================================
        # FAST 不可以 >= SLOW
        # ==================================

        if fast >= slow:
            continue

        print(
            f"Testing EMA{fast}/{slow}..."
        )

        # ==================================
        # 套用目前參數
        # ==================================

        config.FAST_EMA = fast
        config.SLOW_EMA = slow

        # 出場 EMA 使用 Fast EMA
        config.EXIT_EMA = fast

        try:

            # ==================================
            # 執行回測
            # ==================================

            try:

                result = run(
                    filepath,
                    verbose=False
                )

                metrics = result["metrics"]
                df = result["data"]

                buy_count = int(df["BUY"].sum())
                sell_count = int(df["SELL"].sum())

                print(
                    f"EMA{fast}/{slow} "
                    f"BUY={buy_count} "
                    f"SELL={sell_count} "
                    f"ROI={metrics['ROI']:.2f}% "
                    f"DD={metrics['Max Drawdown']:.2f}% "
                    f"Trades={metrics['Trades']}"
                )

                results.append({
                    "Fast EMA": fast,
                    "Slow EMA": slow,
                    "Strategy": f"EMA{fast}/{slow}",
                    "ROI": metrics["ROI"],
                    "Profit Factor": metrics["Profit Factor"],
                    "Win Rate": metrics["Win Rate"],
                    "Max Drawdown": metrics["Max Drawdown"],
                    "Trades": metrics["Trades"],
                })

            except Exception as e:

                print(
                    f"EMA{fast}/{slow} 發生錯誤：{e}"
                )


            # ==================================
            # 儲存結果
            # ==================================



        except Exception as e:

            print(
                f"EMA{fast}/{slow} 發生錯誤：{e}"
            )


# ======================================
# Restore config
# ======================================

config.FAST_EMA = original_fast
config.SLOW_EMA = original_slow
config.EXIT_EMA = original_exit_ema
config.STRATEGY = original_strategy
config.BUY_MODE = original_buy_mode


# ======================================
# Results
# ======================================

optimization = pd.DataFrame(results)


if not optimization.empty:

    # 先按照 ROI 排序
    optimization = optimization.sort_values(
        by="ROI",
        ascending=False
    ).reset_index(drop=True)


# ======================================
# 顯示結果
# ======================================

print()
print("========== EMA CROSS Optimization ==========")
print()

print(optimization)


# ======================================
# Save CSV
# ======================================

os.makedirs(
    "output",
    exist_ok=True
)

optimization.to_csv(
    "output/optimization.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print(
    "已輸出：output/optimization.csv"
)