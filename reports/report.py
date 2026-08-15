import pandas as pd
import config
import os
import matplotlib.pyplot as plt

def calculate_metrics(trades, equity_curve=None):

    if trades.empty:
        return {
            "Trades": 0,
            "Win Rate": 0,
            "Average Profit": 0,
            "Average Win": 0,
            "Average Loss": 0,
            "Risk Reward": 0,
            "Profit Factor": 0,
            "Best Trade": 0,
            "Worst Trade": 0,
            "Total Profit": 0,
            "Max Drawdown": 0,
            "Net Profit": 0,
            "Final Capital": config.INITIAL_CAPITAL,
            "ROI": 0
        }

    total_trade = len(trades)

    win_trade = len(trades[trades["Profit %"] > 0])

    lose_trade = len(trades[trades["Profit %"] <= 0])

    win_rate = win_trade / total_trade * 100

    avg_profit = trades["Profit %"].mean()

    avg_win = trades.loc[
        trades["Profit %"] > 0,
        "Profit %"
    ].mean()

    avg_loss = abs(
        trades.loc[
            trades["Profit %"] < 0,
            "Profit %"
        ].mean()
    )
    avg_win = 0 if pd.isna(avg_win) else avg_win
    avg_loss = 0 if pd.isna(avg_loss) else avg_loss

    if avg_loss == 0:
        risk_reward = float("inf")
    else:
        risk_reward = avg_win / avg_loss

    gross_profit = trades.loc[
        trades["Profit Amount"] > 0,
        "Profit Amount"
    ].sum()

    gross_loss = abs(
        trades.loc[
            trades["Profit Amount"] < 0,
            "Profit Amount"
        ].sum()
    )

    if gross_loss == 0:
        profit_factor = float("inf")
    else:
        profit_factor = gross_profit / gross_loss

    best_trade = trades["Profit %"].max()

    worst_trade = trades["Profit %"].min()

    total_profit = trades["Profit %"].sum()

    net_profit = trades["Profit Amount"].sum()

    final_capital = config.INITIAL_CAPITAL + net_profit

    roi = net_profit / config.INITIAL_CAPITAL * 100

# ======================================
# ======================================
# Max Drawdown
# 只使用「平倉後」的已實現資金
# 不計算持倉期間浮動損益
# ======================================

    equity_values = [config.INITIAL_CAPITAL]

    for profit in trades["Profit Amount"]:

        equity_values.append(
            equity_values[-1] + profit
        )

    peak = equity_values[0]
    max_drawdown = 0

    for value in equity_values:

        if value > peak:
            peak = value

        drawdown = (
            (peak - value)
            / peak
            * 100
        )

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return {
        "Trades": total_trade,
        "Win Rate": win_rate,
        "Average Profit": avg_profit,
        "Average Win": avg_win,
        "Average Loss": avg_loss,
        "Risk Reward": risk_reward,
        "Profit Factor": profit_factor,
        "Best Trade": best_trade,
        "Worst Trade": worst_trade,
        "Total Profit": total_profit,
        "Max Drawdown": max_drawdown,
        "Net Profit": net_profit,
        "Final Capital": final_capital,
        "ROI": roi
    }

def show_report(trades):

    if trades.empty:
        print("沒有交易")
        return

    # ==========================
    # 基本統計
    # ==========================

    metrics = calculate_metrics(trades)

    # ==========================
    # 顯示結果
    # ==========================

    print(f"交易次數：{metrics['Trades']}")
    print(f"勝率：{metrics['Win Rate']:.2f}%")
    print(f"平均獲利：{metrics['Average Win']:.2f}%")
    print(f"平均虧損：{metrics['Average Loss']:.2f}%")
    print(f"盈虧比：{metrics['Risk Reward']:.2f}")
    print(f"平均報酬：{metrics['Average Profit']:.2f}%")
    print(f"最佳交易：{metrics['Best Trade']:.2f}%")
    print(f"最差交易：{metrics['Worst Trade']:.2f}%")
    print(f"累積報酬：{metrics['Total Profit']:.2f}%")
    print(f"Profit Factor：{metrics['Profit Factor']:.2f}")
    print(f"最大回撤：{metrics['Max Drawdown']:.2f}%")

    print(f"初始本金：{config.INITIAL_CAPITAL:,.0f}")
    print(f"總獲利：{metrics['Net Profit']:,.0f}")
    print(f"最終本金：{metrics['Final Capital']:,.0f}")
    print(f"ROI：{metrics['ROI']:.2f}%")

    equity = [config.INITIAL_CAPITAL]

    for profit in trades["Profit Amount"]:
        equity.append(equity[-1] + profit)
            # ==========================
    # 輸出 Equity Curve
    # ==========================

    os.makedirs("output", exist_ok=True)

    equity_df = pd.DataFrame({

        "Trade": range(len(equity)),
        "Equity": equity

    })

    equity_df.to_csv(
        "output/equity_curve.csv",
        index=False,
        encoding="utf-8-sig"
    )
        # ==========================
    # 畫資金曲線
    # ==========================

    plt.figure(figsize=(10, 5))

    plt.plot(
        equity_df["Trade"],
        equity_df["Equity"]
    )

    plt.title("Equity Curve")

    plt.xlabel("Trade")

    plt.ylabel("Equity")

    plt.grid(True)

    plt.savefig(
        "output/equity_curve.png",
        dpi=150
    )

    plt.close()

    print()
    print("已輸出：output/equity_curve.csv")
    print("已輸出：output/equity_curve.png")