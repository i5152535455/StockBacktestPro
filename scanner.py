import os
import config
import indicators
import strategy
import backtest_engine
import report
import pandas as pd

folder = "data/TW"
results = []

print("開始掃描...")

for file in os.listdir(folder):

    if not file.endswith(".csv"):
        continue

    filepath = os.path.join(folder, file)

    print(f"讀取：{filepath}")

try:

    df = indicators.load_data(filepath)

    df = indicators.convert_timeframe(df)

    df = indicators.calculate_ema(df)

    df = strategy.generate_signal(df)

    trades = backtest_engine.run_backtest(df)

    metrics = report.calculate_metrics(trades)

    results.append({
        "Stock": file.replace(".csv", ""),
        "ROI": round(metrics["ROI"], 2),
        "Win Rate": round(metrics["Win Rate"], 2),
        "Profit Factor": round(metrics["Profit Factor"], 2),
        "Max DD": round(metrics["Max Drawdown"], 2),
        "Risk Reward": round(metrics["Risk Reward"], 2),
        "Trades": metrics["Trades"]
    })

    print(f"{file} 完成")

except Exception as e:

    print(f"{file} 發生錯誤：{e}")

print()


results_df = pd.DataFrame(results)

# ROI由大到小排序
results_df = results_df.sort_values(
    by="ROI",
    ascending=False
).reset_index(drop=True)

print()
print("========== Scanner Result ==========")
print(results_df)

os.makedirs("output", exist_ok=True)

results_df.to_csv(
    "output/scanner_result.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("已輸出：output/scanner_result.csv")