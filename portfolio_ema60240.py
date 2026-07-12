"""
Portfolio Module
資金管理
"""

import config


class Portfolio:

    def __init__(self):

        # 初始本金
        self.initial_cash = config.INITIAL_CAPITAL

        # 現金
        self.cash = config.INITIAL_CAPITAL

        # 持股數
        self.shares = 0

        # 持股成本
        self.buy_price = 0

        # 是否持股
        self.position = False
        
        # 已投入資金
        self.invested = 0

        # 已實現損益
        self.realized_profit = 0

        # 交易紀錄
        self.trades = []

    def buy(self, date, price):

        # 每次投入固定金額
        invest = min(config.POSITION_SIZE, self.cash)

        # 可買股數
        self.shares = invest / price

        # 扣除現金
        self.cash -= invest

        self.invested = invest

        self.position = True
        self.buy_price = price

    def sell(
        self,
        date,
        price,
        position=1.0,
        exit_reason=""
    ):

        sell_shares = self.shares * position

        sell_amount = sell_shares * price

        cost = self.invested * position

        profit_amount = sell_amount - cost

        self.cash += sell_amount

        self.realized_profit += profit_amount

        self.trades.append({

        "Buy Price": self.buy_price,

        "Sell Price": price,

        "Profit Amount": round(profit_amount, 2),

        "Exit Reason": exit_reason

    })

        self.shares -= sell_shares

        self.invested -= cost
        if self.shares <= 1e-8:

         self.position = False
         self.shares = 0
         self.buy_price = 0
         self.invested = 0

    def summary(self):

        print("========== Portfolio ==========")
        print(f"Initial Cash : {self.initial_cash}")
        print(f"Cash         : {self.cash:,.0f}")
        print(f"Shares       : {self.shares:.4f}")
        print(f"Realized P/L : {self.realized_profit:,.0f}")