import pandas as pd
import config


def show_report(trades):

    if trades.empty:
        print("沒有交易")
        return

    # ==========================
    # 基本統計
    # ==========================

    total_trade = len(trades)

    win_trade = len(trades[trades["Profit %"] > 0])

    lose_trade = len(trades[trades["Profit %"] <= 0])

    win_rate = win_trade / total_trade * 100

    avg_profit = trades["Profit %"].mean()

    best_trade = trades["Profit %"].max()

    worst_trade = trades["Profit %"].min()

    total_profit = trades["Profit %"].sum()

    # ==========================
    # Portfolio
    # ==========================

    net_profit = trades["Profit Amount"].sum()

    final_capital = config.INITIAL_CAPITAL + net_profit

    roi = net_profit / config.INITIAL_CAPITAL * 100

    # ==========================
    # 最大回撤 (Max Drawdown)
    # ==========================

    equity = [config.INITIAL_CAPITAL]

    for profit in trades["Profit Amount"]:
        equity.append(equity[-1] + profit)

    peak = equity[0]
    max_drawdown = 0

    for value in equity:

        if value > peak:
            peak = value

        drawdown = (peak - value) / peak * 100

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    # ==========================
    # 顯示結果
    # ==========================

    print()
    print("========== 回測報告 ==========")

    print(f"交易次數：{total_trade}")
    print(f"勝率：{win_rate:.2f}%")
    print(f"平均報酬：{avg_profit:.2f}%")
    print(f"最佳交易：{best_trade:.2f}%")
    print(f"最差交易：{worst_trade:.2f}%")
    print(f"累積報酬：{total_profit:.2f}%")
    print(f"最大回撤：{max_drawdown:.2f}%")

    print()
    print("========== Portfolio ==========")

    print(f"初始本金：{config.INITIAL_CAPITAL:,.0f}")
    print(f"總獲利：{net_profit:,.0f}")
    print(f"最終本金：{final_capital:,.0f}")
    print(f"ROI：{roi:.2f}%")