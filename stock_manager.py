import pandas as pd


def load_stock_list():

    df = pd.read_csv("stock_list.csv")

    return df["StockID"].astype(str).tolist()