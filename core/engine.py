import pandas as pd
import config
from core import portfolio


def calculate_profit(buy_price, sell_price):

    buy_cost = buy_price * (1 + config.BUY_COMMISSION)

    sell_income = sell_price * (
        1
        - config.SELL_COMMISSION
        - config.SELL_TAX
    )

    return (sell_income - buy_cost) / buy_cost * 100


def calculate_profit_amount(
    invest_amount,
    buy_price,
    sell_price
):

    buy_cost = buy_price * (1 + config.BUY_COMMISSION)

    sell_income = sell_price * (
        1
        - config.SELL_COMMISSION
        - config.SELL_TAX
    )

    profit_ratio = (
        sell_income - buy_cost
    ) / buy_cost

    return invest_amount * profit_ratio


def record_sell(
    pf,
    trades,
    buy_date,
    buy_price,
    sell_date,
    sell_price,
    position,
    exit_reason
):

    pf.sell(
        sell_date,
        sell_price,
        position=position,
        exit_reason=exit_reason
    )

    profit = calculate_profit(
        buy_price,
        sell_price
    )

    profit_amount = calculate_profit_amount(
        config.POSITION_SIZE * position,
        buy_price,
        sell_price
    )

    trades.append({

        "Buy Date": buy_date,
        "Buy Price": buy_price,

        "Sell Date": sell_date,
        "Sell Price": sell_price,

        "Position": position,

        "Profit %": round(profit, 2),
        "Profit Amount": round(profit_amount, 0),

        "Exit Reason": exit_reason

    })


def run_backtest(df, verbose=True):

    pf = portfolio.Portfolio()

    # ======================================
    # Position State
    # ======================================

    position = False

    position_size = 0

    buy_price = 0
    buy_date = None

    partial_exit = False

    trades = []

    # ======================================
    # Equity Curve
    # ======================================

    equity_curve = []

    initial_capital = config.INITIAL_CAPITAL

    # ======================================
    # 回測
    # ======================================

    for _, row in df.iterrows():

        # ==================================
        # BUY
        # ==================================

        if row["BUY"] and not position:

            position = True

            position_size = 1.0

            buy_price = row["Close"]

            buy_date = row["Date"]

            partial_exit = False

            pf.buy(
                buy_date,
                buy_price
            )

        # ==================================
        # 三倍停利
        # 賣出 1/3
        # ==================================

        if position and not partial_exit:

            target_price = (
                buy_price *
                config.TAKE_PROFIT_MULTIPLE
            )

            if verbose:

                print(
                    row["Date"],
                    "Buy:",
                    round(buy_price, 2),
                    "Now:",
                    round(row["Close"], 2),
                    "Target:",
                    round(target_price, 2)
                )

            if row["Close"] >= target_price:

                if verbose:
                    print(
                        ">>> Triple Target Hit <<<"
                    )

                record_sell(

                    pf,
                    trades,

                    buy_date,
                    buy_price,

                    row["Date"],
                    row["Close"],

                    1 / 3,

                    "Triple Target 1/3"
                )

                # 剩餘 2/3
                position_size = 2 / 3

                partial_exit = True

        # ==================================
        # EMA 出場
        # ==================================

        if position and row["SELL"]:

            sell_price = row["Close"]

            sell_date = row["Date"]

            # ----------------------------------
            # 如果還沒三倍停利
            # → 全部 100% 出場
            # ----------------------------------

            if not partial_exit:

                record_sell(

                    pf,
                    trades,

                    buy_date,
                    buy_price,

                    sell_date,
                    sell_price,

                    1.0,

                    row["EXIT_REASON"]
                )

            # ----------------------------------
            # 已經三倍停利
            # → 剩餘 2/3 出場
            # ----------------------------------

            else:

                record_sell(

                    pf,
                    trades,

                    buy_date,
                    buy_price,

                    sell_date,
                    sell_price,

                    2 / 3,

                    f"{row['EXIT_REASON']} 2/3"
                )

            # 清除持倉
            position = False
            position_size = 0

            buy_price = 0
            buy_date = None

            partial_exit = False

        # ==================================
        # Equity Curve
        #
        # 注意：
        # 這裡仍然可以記錄浮動 Equity
        # 但最大回撤不使用它
        # ==================================

        realized_profit = sum(
            trade["Profit Amount"]
            for trade in trades
        )

        unrealized_profit = 0

        if position:

            unrealized_profit = calculate_profit_amount(

                config.POSITION_SIZE * position_size,

                buy_price,

                row["Close"]
            )

        equity = (
            initial_capital
            + realized_profit
            + unrealized_profit
        )

        equity_curve.append({

            "Date": row["Date"],

            "Equity": equity

        })

    # ======================================
    # 回測結束
    # ======================================

    if position:

        sell_price = df.iloc[-1]["Close"]

        sell_date = df.iloc[-1]["Date"]

        # ----------------------------------
        # 尚未三倍停利
        # → 全部出場
        # ----------------------------------

        if not partial_exit:

            record_sell(

                pf,
                trades,

                buy_date,
                buy_price,

                sell_date,
                sell_price,

                1.0,

                "End of Backtest"
            )

        # ----------------------------------
        # 已三倍停利
        # → 剩餘 2/3 出場
        # ----------------------------------

        else:

            record_sell(

                pf,
                trades,

                buy_date,
                buy_price,

                sell_date,
                sell_price,

                2 / 3,

                "End of Backtest 2/3"
            )

        # 最終平倉後 Equity
        realized_profit = sum(
            trade["Profit Amount"]
            for trade in trades
        )

        equity_curve.append({

            "Date": sell_date,

            "Equity":
                initial_capital
                + realized_profit

        })

    # ======================================
    # Portfolio
    # ======================================

    if verbose:
        pf.summary()

    # ======================================
    # Trades DataFrame
    # ======================================

    trades_df = pd.DataFrame(trades)

    # ======================================
    # Equity Curve DataFrame
    # ======================================

    equity_df = pd.DataFrame(
        equity_curve
    )

    return trades_df, equity_df