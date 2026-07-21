import stock_list

print("全部股票：", len(stock_list.get_tw_stocks()))

print("股票：", len(stock_list.get_stocks_only()))

print("ETF：", len(stock_list.get_etfs()))

print(stock_list.get_stock_name("2330"))

print(stock_list.get_market("2330"))