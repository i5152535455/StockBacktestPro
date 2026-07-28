import os
import pandas as pd

import config
from services.backtest_service import run

filepath = "data/TW/2330.csv"

results = []

original_strategy = config.STRATEGY

for strategy_name in config.AVAILABLE_STRATEGIES:

    config.STRATEGY = strategy_name

    result = run(filepath)

    metrics = result["metrics"]
    info = result["strategy"]

    results.append({
        "Module": strategy_name,
        "Strategy": info["name"],
        "Description": info["description"],
        "ROI": metrics["ROI"],
        "Profit Factor": metrics["Profit Factor"],
        "Win Rate": metrics["Win Rate"],
        "Trades": metrics["Trades"],
        "Max Drawdown": metrics["Max Drawdown"],
    })

config.STRATEGY = original_strategy

# 建立 DataFrame
benchmark = pd.DataFrame(results)

# 依 ROI 排序
benchmark = benchmark.sort_values(
    by="ROI",
    ascending=False
).reset_index(drop=True)

print("\n========== Strategy Benchmark ==========\n")
print(benchmark)

# 建立 output 資料夾
os.makedirs("output", exist_ok=True)

# 輸出 CSV
benchmark.to_csv(
    "output/benchmark.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n已輸出：output/benchmark.csv")