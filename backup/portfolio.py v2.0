"""
Portfolio Module
資金管理
"""

import config


class Portfolio:

    def __init__(self):

        # 初始本金
        self.initial_cash = config.INITIAL_CAPITAL

        self.reset()

        # 已實現損益
        self.realized_profit = 0

        # 交易紀錄
        self.trades = []

    def reset(self):
        """重設整個投資組合"""

        self.cash = self.initial_cash

        self.position = False
        self.shares = 0.0
        self.buy_price = 0.0
        self.invested = 0.0

    def buy(self, date, price):

        # 每次投入固定金額
        invest = min(config.POSITION_SIZE, self.cash)

        if invest <= 0:
            return 0

        # 可買股數
        self.shares = invest / price

        self.cash -= invest

        self.invested = invest

        self.position = True
        self.buy_price = price

        return self.shares

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

        trade = self._create_trade(
            buy_price=self.buy_price,
            sell_price=price,
            profit_amount=profit_amount,
            exit_reason=exit_reason,
        )

        self.trades.append(trade)

        self.shares -= sell_shares
        self.invested -= cost

        if self.shares <= 1e-8:
            self._reset_position()

        return profit_amount

    def _create_trade(
        self,
        buy_price,
        sell_price,
        profit_amount,
        exit_reason,
    ):

        return {
            "Buy Price": buy_price,
            "Sell Price": sell_price,
            "Profit Amount": round(profit_amount, 2),
            "Exit Reason": exit_reason,
        }

    def _reset_position(self):

        self.position = False
        self.shares = 0.0
        self.buy_price = 0.0
        self.invested = 0.0

    def summary(self):

        print("========== Portfolio ==========")
        print(f"Initial Cash : {self.initial_cash}")
        print(f"Cash         : {self.cash:,.0f}")
        print(f"Shares       : {self.shares:.4f}")
        print(f"Realized P/L : {self.realized_profit:,.0f}")