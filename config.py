# ======================================
# StockBacktest Pro
# 全域設定
# ======================================

# ========= 市場 =========
MARKET = "TW"          # TW / US

# K棒週期
TIMEFRAME = "W"      # D=日K  W=周K

# EMA
FAST_EMA = 20
SLOW_EMA = 60

# 停損 (%)
STOP_LOSS = 8

# 停利 (%)
TAKE_PROFIT = 20

# ===========================
# 交易成本
# ===========================

# 手續費 (0.1425%)
BUY_COMMISSION = 0.001425
SELL_COMMISSION = 0.001425

# 證交稅 (0.3%)
SELL_TAX = 0.003

# ========= 成交量 =========
USE_VOLUME_FILTER = False
MIN_VOLUME = 500

# ========= 回測 =========
START_DATE = "2023-01-01"
END_DATE = "2026-07-01"

# ========= 資金 =========
INITIAL_CAPITAL = 1000000
MAX_POSITIONS = 10
POSITION_SIZE = 100000