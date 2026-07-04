import config
import indicators
import strategy
import backtest_engine
import report

filepath = "data/TW/2330.csv"

# 讀取資料
df = indicators.load_data(filepath)

# 轉換週期(日K / 周K)
df = indicators.convert_timeframe(df)

# 計算EMA
df = indicators.calculate_ema(df)

# 建立買賣訊號
df = strategy.generate_signal(df)

fast_name = f"EMA{config.FAST_EMA}"
slow_name = f"EMA{config.SLOW_EMA}"

# 顯示最後20筆資料
print(df[["Date", fast_name, slow_name, "BUY", "SELL"]].tail(20))

# 執行回測
trades = backtest_engine.run_backtest(df)

# 顯示交易紀錄
print()
print("===== 交易紀錄 =====")
print(trades)

# 顯示回測報告
report.show_report(trades)