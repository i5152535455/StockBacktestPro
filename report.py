import pandas as pd
import config
import os
import matplotlib.pyplot as plt


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
        # ==========================
    # Profit Factor
    # ==========================

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

    # ==========================
    # Portfolio
    # ==========================

    net_profit = trades["Profit Amount"].sum()
        # ==========================
    # Equity Curve
    # ==========================

    equity = [config.INITIAL_CAPITAL]

    current = config.INITIAL_CAPITAL

    for profit in trades["Profit Amount"]:

        current += profit

        equity.append(current)

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
    print(f"Profit Factor：{profit_factor:.2f}")
    print(f"最大回撤：{max_drawdown:.2f}%")

    print()
    print("========== Portfolio ==========")

    print(f"初始本金：{config.INITIAL_CAPITAL:,.0f}")
    print(f"總獲利：{net_profit:,.0f}")
    print(f"最終本金：{final_capital:,.0f}")
    print(f"ROI：{roi:.2f}%")
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