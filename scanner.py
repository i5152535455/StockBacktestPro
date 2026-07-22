import os
import pandas as pd
import config

from utils import indicators
from strategies.loader import get_strategy

strategy = get_strategy()
from core import engine as backtest_engine
from reports import report

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

        df = strategy.prepare(df)

        df = strategy.generate_signal(df)

        trades = backtest_engine.run_backtest(
            df,
            verbose=False
        )

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

# 計算 Score
results_df["PF Score"] = results_df["Profit Factor"].clip(upper=10)

results_df["Score"] = (
    results_df["ROI"] * config.ROI_WEIGHT +
    results_df["Win Rate"] * config.WINRATE_WEIGHT +
    results_df["PF Score"] * 10 * config.PF_WEIGHT +
    (100 - results_df["Max DD"]) * config.DD_WEIGHT
)

# 先四捨五入
results_df["Score"] = results_df["Score"].round(2)

buy_df = results_df[
    (results_df["ROI"] >= config.MIN_ROI) &
    (results_df["Win Rate"] >= config.MIN_WIN_RATE) &
    (results_df["Profit Factor"] >= config.MIN_PROFIT_FACTOR) &
    (results_df["Max DD"] <= config.MAX_DRAWDOWN) &
    (results_df["Trades"] >= config.MIN_TRADES)
]


# Buy Candidates 依 Score 排序
buy_df = buy_df.sort_values(
    by="Score",
    ascending=False
).reset_index(drop=True)

print()
print("========== Scanner Result ==========")
print(results_df)

print()
print("========== Buy Candidates ==========")

print(buy_df)

os.makedirs("output", exist_ok=True)

results_df.to_csv(
    "output/scanner_result.csv",
    index=False,
    encoding="utf-8-sig"
)
buy_df.to_csv(
    "output/buy_candidates.csv",
    index=False,
    encoding="utf-8-sig"
)
print()
print("已輸出：output/scanner_result.csv")
print("已輸出：output/buy_candidates.csv")