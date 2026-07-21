"""
Stock List Manager
"""

import pandas as pd

STOCK_LIST_FILE = "data/metadata/tw_stock_list.csv"


def load_tw_stock_list():
    return pd.read_csv(STOCK_LIST_FILE)


def get_tw_stocks():
    """
    全部股票代號
    """
    df = load_tw_stock_list()
    return df["Code"].astype(str).tolist()


def get_stocks_only():
    """
    一般股票
    """
    df = load_tw_stock_list()

    df = df[df["Type"] == "Stock"]

    return df["Code"].astype(str).tolist()


def get_etfs():
    """
    ETF
    """
    df = load_tw_stock_list()

    df = df[df["Type"] == "ETF"]

    return df["Code"].astype(str).tolist()


def get_stock_name(code):
    """
    股票名稱
    """
    df = load_tw_stock_list()

    row = df[df["Code"].astype(str) == str(code)]

    if row.empty:
        return ""

    return row.iloc[0]["Name"]


def get_market(code):
    """
    市場別
    """
    df = load_tw_stock_list()

    row = df[df["Code"].astype(str) == str(code)]

    if row.empty:
        return ""

    return row.iloc[0]["Market"]