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

        # 交易紀錄
        self.trades = []

    def buy(self, date, price):

        self.position = True
        self.buy_price = price

    def sell(self, date, price):

        self.position = False

    def summary(self):

        print("========== Portfolio ==========")
        print(f"Initial Cash : {self.initial_cash}")
        print(f"Cash         : {self.cash}")
        print(f"Shares       : {self.shares}")