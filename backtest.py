import config

from services.backtest_service import run
from reports import report


# ======================================
# Stock
# ======================================

filepath = "data/TW/2330.csv"


# ======================================
# Run Backtest
# ======================================

result = run(filepath)

strategy = result["strategy"]
df = result["data"]
trades = result["trades"]


# ======================================
# Strategy
# ======================================

print()
print("========== Strategy ==========")

print(f"Name       : {strategy['name']}")
print(f"Version    : {strategy['version']}")
print(f"Description: {strategy['description']}")


# ======================================
# Debug
# ======================================

if config.VERBOSE:

    fast_name = f"EMA{config.FAST_EMA}"
    slow_name = f"EMA{config.SLOW_EMA}"

    print()

    print(
        df[
            [
                "Date",
                fast_name,
                slow_name,
                "BUY",
                "SELL"
            ]
        ].tail(20)
    )

    # ======================================
# 顯示所有真正 Golden Cross
# ======================================

crosses = df[df["BUY"]].copy()

print()
print("========== Golden Cross ==========")

if crosses.empty:

    print("沒有 Golden Cross")

else:

    print(
        crosses[
            [
                "Date",
                "Close",
                fast_name,
                slow_name
            ]
        ].to_string(index=False)
    )


# ======================================
# Trade Records
# ======================================

print()
print("===== 交易紀錄 =====")
print(trades)


# ======================================
# Report
# ======================================

report.show_report(trades)