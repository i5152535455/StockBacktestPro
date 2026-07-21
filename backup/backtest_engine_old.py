from utils import indicators
from strategies import ema60240 as strategy
from core import engine as backtest_engine
from reports import report

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

def record_sell(
    pf,
    trades,
    buy_date,
    buy_price,
    sell_date,
    sell_price,
    exit_reason
):

    pf.sell(
        sell_date,
        sell_price,
        exit_reason=exit_reason
    )

    profit = calculate_profit(
        buy_price,
        sell_price
    )

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
        "Exit Reason": exit_reason
    })


def run_backtest(df, verbose=True):

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

            pf.buy(buy_date, buy_price)

            stop_loss_price = buy_price * (1 - config.STOP_LOSS / 100)
            take_profit_price = buy_price * (1 + config.TAKE_PROFIT / 100)

        # ===================
        # 停損
        # ===================
        elif position and row["Close"] < row[f"EMA{config.FAST_EMA}"]:

            sell_price = row["Close"]
            sell_date = row["Date"]

            record_sell(
                pf,
                trades,
                buy_date,
                buy_price,
                sell_date,
                sell_price,
                "Stop Loss"
)
           

            position = False
            buy_price = 0
            buy_date = None

        # ===================
        # 停利
        # ===================
        elif position and row["Close"] >= take_profit_price:

            sell_price = row["Close"]
            sell_date = row["Date"]

            record_sell(
                pf,
                trades,
                buy_date,
                buy_price,
                sell_date,
                sell_price,
                "Take Profit"
            )

            position = False
            buy_price = 0
            buy_date = None    

        # ===================
        # EMA死亡交叉賣出
        # ===================
        elif row["SELL"] and position:

            sell_price = row["Close"]
            sell_date = row["Date"]

            record_sell(
                pf,
                trades,
                buy_date,
                buy_price,
                sell_date,
                sell_price,
                "EMA Sell"
            )

            position = False
            buy_price = 0
            buy_date = None

    # ===================
    # 最後一天平倉
    # ===================
    if position:

        sell_price = df.iloc[-1]["Close"]
        sell_date = df.iloc[-1]["Date"]

        record_sell(
            pf,
            trades,
            buy_date,
            buy_price,
            sell_date,
            sell_price,
            "End of Backtest"
        )

    if verbose:
     pf.summary()
    
    return pd.DataFrame(trades)