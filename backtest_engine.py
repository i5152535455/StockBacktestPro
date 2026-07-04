import pandas as pd


def run_backtest(df):

    position = False
    buy_price = 0
    buy_date = None

    trades = []

    for _, row in df.iterrows():

        # 買進
        if row["BUY"] and not position:
            position = True
            buy_price = row["Close"]
            buy_date = row["Date"]

        # 賣出
        elif row["SELL"] and position:

            sell_price = row["Close"]
            sell_date = row["Date"]

            profit = (sell_price - buy_price) / buy_price * 100

            trades.append({
                "Buy Date": buy_date,
                "Buy Price": buy_price,
                "Sell Date": sell_date,
                "Sell Price": sell_price,
                "Profit %": round(profit, 2)
            })

            position = False
            buy_price = 0
            buy_date = None

    # ===========================
    # 最後還有持股就平倉
    # ===========================
    if position:

        sell_price = df.iloc[-1]["Close"]
        sell_date = df.iloc[-1]["Date"]

        profit = (sell_price - buy_price) / buy_price * 100

        trades.append({
            "Buy Date": buy_date,
            "Buy Price": buy_price,
            "Sell Date": sell_date,
            "Sell Price": sell_price,
            "Profit %": round(profit, 2)
        })

    return pd.DataFrame(trades)