import pandas as pd
import config
import portfolio

def calculate_profit(buy_price, sell_price):

    buy_cost = buy_price * (1 + config.BUY_COMMISSION)

    sell_income = sell_price * (
        1
        - config.SELL_COMMISSION
        - config.SELL_TAX
    )

    return (sell_income - buy_cost) / buy_cost * 100

def calculate_profit_amount(invest_amount, buy_price, sell_price):

    buy_cost = buy_price * (1 + config.BUY_COMMISSION)

    sell_income = sell_price * (
        1
        - config.SELL_COMMISSION
        - config.SELL_TAX
    )

    profit_ratio = (sell_income - buy_cost) / buy_cost
    return invest_amount * profit_ratio


def run_backtest(df, verbose=True):

    pf = portfolio.Portfolio()

    position = False
    position_size = 0

    buy_price = 0
    buy_date = None

    partial_exit = False

    trades = []

    for _, row in df.iterrows():

        # ===================
        # 買進
        # ===================
        if row["BUY"] and not position:

            position = True
            position_size = 1.0
            buy_price = row["Close"]
            buy_date = row["Date"]

            pf.buy(buy_date, buy_price)

            partial_exit = False


        # ===================
        # 跌破 EMA60 出場
        # ===================
        elif position and row["Close"] < row[f"EMA{config.FAST_EMA}"]:

            sell_price = row["Close"]
            sell_date = row["Date"]

            pf.sell(sell_date, sell_price)

            profit = calculate_profit(buy_price, sell_price)
 

            profit_amount = calculate_profit_amount(
            config.POSITION_SIZE,
            buy_price,
            sell_price
            )

            trades.append({
            "Buy Date": buy_date,
            "Buy Price": buy_price,
            "Sell Date": sell_date,
            "Sell Price": sell_price,
            "Profit %": round(profit, 2),
            "Profit Amount": round(profit_amount, 0),
            "Exit Reason": "EMA60 Exit"
            })
           

            position = False
            position_size = 0
            buy_price = 0
            buy_date = None

        # ===================
        # 第一次獲利：漲三倍賣 1/3
        # ===================
        elif (
             position
             and (not partial_exit)
             and row["Close"] >= buy_price * 3
            ):

         print(f"{buy_date} 三倍價達成，賣出 1/3")

         partial_exit = True
    # 下一步會真正實作賣出1/3
 

    # ===================
    # 最後一天平倉
    # ===================
    if position:

        sell_price = df.iloc[-1]["Close"]
        sell_date = df.iloc[-1]["Date"]

        pf.sell(sell_date, sell_price)

        profit = calculate_profit(buy_price, sell_price)

        profit_amount = calculate_profit_amount(
        config.POSITION_SIZE,
        buy_price,
        sell_price
        )

        trades.append({
        "Buy Date": buy_date,
        "Buy Price": buy_price,
        "Sell Date": sell_date,
        "Sell Price": sell_price,
        "Profit %": round(profit, 2),
        "Profit Amount": round(profit_amount, 0),
        "Exit Reason": "End of Backtest"
        })

    if verbose:
     pf.summary()
    
    return pd.DataFrame(trades)