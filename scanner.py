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

    if file.endswith(".csv"):

        filepath = os.path.join(folder, file)

        print(f"讀取：{filepath}")

    df = indicators.load_data(filepath)

    df = indicators.convert_timeframe(df)

    df = indicators.calculate_ema(df)

    df = strategy.generate_signal(df)

trades = backtest_engine.run_backtest(
    df,
    verbose=False
)
net_profit = trades["Profit Amount"].sum()

roi = float(net_profit / config.INITIAL_CAPITAL * 100)

results.append({

    "Stock": file.replace(".csv", ""),

    "ROI": round(roi, 2),

    "Trades": len(trades)

})

print()

print("========== Scanner Result ==========")

result_df = pd.DataFrame(results)

result_df = result_df.sort_values(
    by="ROI",
    ascending=False
)

print(result_df)