import pandas as pd
import config
import portfolio


def run_backtest(df):

    pf = portfolio.Portfolio()
    position = False
    buy_price = 0
    buy_date = None
    stop_loss_price = 0

    trades = []

    for _, row in df.iterrows():

        # ===================
        # 買進
        # ===================
        if row["BUY"] and not position:

            position = True
            buy_price = row["Close"]
            buy_date = row["Date"]

            stop_loss_price = buy_price * (1 - config.STOP_LOSS / 100)
            take_profit_price = buy_price * (1 + config.TAKE_PROFIT / 100)

        # ===================
        # 停損
        # ===================
        elif position and row["Close"] <= stop_loss_price:

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

        # ===================
        # 停利
        # ===================
        elif position and row["Close"] >= take_profit_price:

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

        # ===================
        # EMA死亡交叉賣出
        # ===================
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

    # ===================
    # 最後一天平倉
    # ===================
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

    pf.summary()
    
    return pd.DataFrame(trades)