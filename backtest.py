import config
from utils import indicators
from reports import report
from strategies.loader import get_strategy

strategy = get_strategy()
info = strategy.get_info()
from core import engine as backtest_engine

filepath = "data/TW/2330.csv"

# 讀取資料
df = indicators.load_data(filepath)

# 轉換週期(日K / 周K)
df = indicators.convert_timeframe(df)

# 計算EMA
df = indicators.load_data(filepath)

df = indicators.convert_timeframe(df)

strategy = get_strategy()
info = strategy.get_info()

df = strategy.prepare(df)

df = strategy.generate_signal(df)

print(df[
    [
        "Date",
        "Close",
        "MACD",
        "MACD_SIGNAL",
        "MACD_HIST"
    ]
].tail())

df = strategy.prepare(df)

# 建立買賣訊號
df = strategy.generate_signal(df)

fast_name = f"EMA{config.FAST_EMA}"
slow_name = f"EMA{config.SLOW_EMA}"

# 顯示最後20筆資料
print(df[["Date", fast_name, slow_name, "BUY", "SELL"]].tail(20))

print("\n========== Strategy ==========")
print(f"Name       : {info['name']}")
print(f"Version    : {info['version']}")
print(f"Description: {info['description']}")

# 執行回測
trades = backtest_engine.run_backtest(
    df,
    verbose=config.VERBOSE
)

# 顯示交易紀錄
print()
print("===== 交易紀錄 =====")
print(trades)

# 顯示回測報告
report.show_report(trades)