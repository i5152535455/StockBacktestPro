import pandas as pd


def show_report(trades):

    if trades.empty:
        print("沒有交易")
        return

    total_trade = len(trades)

    win_trade = len(trades[trades["Profit %"] > 0])

    lose_trade = len(trades[trades["Profit %"] <= 0])

    win_rate = win_trade / total_trade * 100

    avg_profit = trades["Profit %"].mean()

    best_trade = trades["Profit %"].max()

    worst_trade = trades["Profit %"].min()

    total_profit = trades["Profit %"].sum()

    print()
    print("========== 回測報告 ==========")

    print(f"交易次數：{total_trade}")

    print(f"勝率：{win_rate:.2f}%")

    print(f"平均報酬：{avg_profit:.2f}%")

    print(f"最佳交易：{best_trade:.2f}%")

    print(f"最差交易：{worst_trade:.2f}%")

    print(f"累積報酬：{total_profit:.2f}%")