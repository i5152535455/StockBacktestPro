# ======================================
# StockBacktest Pro
# EMA60 / EMA240 Strategy Config
# ======================================

# ======================================
# Market
# ======================================

MARKET = "TW"          # TW / US

# D = Daily
# W = Weekly
TIMEFRAME = "W"

# ======================================
# Strategy
# ======================================

# EMA Length
FAST_EMA = 60
SLOW_EMA = 240

# BUY_MODE
# CROSS : EMA60 上穿 EMA240 時買進
# TREND : 只要 EMA60 > EMA240 且沒有持股就買進
BUY_MODE = "CROSS"

# ======================================
# Take Profit
# ======================================

# 幾倍停利
# 2.0 = 漲兩倍
# 3.0 = 漲三倍
TAKE_PROFIT_MULTIPLE = 3.0

# 第一次停利賣出比例
# 1/3 = 賣 33%
# 0.5 = 賣 50%
FIRST_TAKE_PROFIT_RATIO = 1 / 3

# ======================================
# Exit
# ======================================

EXIT_MODE = "EMA"

# 使用哪條EMA出場
EXIT_EMA = FAST_EMA

USE_STOP_LOSS = False
STOP_LOSS = 8

# True：跌破 EMA60 全部出場
USE_EMA_EXIT = True

# 保留舊功能，目前未使用
USE_STOP_LOSS = False
STOP_LOSS = 8

# 除錯設定
# ==========================
VERBOSE = False

# ======================================
# Transaction Cost
# ======================================

BUY_COMMISSION = 0.001425
SELL_COMMISSION = 0.001425
SELL_TAX = 0.003

# ======================================
# Volume Filter
# ======================================

USE_VOLUME_FILTER = False
MIN_VOLUME = 500

# ======================================
# Backtest
# ======================================

START_DATE = "2023-01-01"
END_DATE = "2026-07-01"

# ======================================
# Portfolio
# ======================================

INITIAL_CAPITAL = 1_000_000

# 預留多股票使用
MAX_POSITIONS = 10

# 每筆投入金額
POSITION_SIZE = 100_000

# ======================================
# Scanner Filter
# ======================================

MIN_ROI = 10

MIN_WIN_RATE = 50

MIN_PROFIT_FACTOR = 2

MAX_DRAWDOWN = 5

MIN_TRADES = 10

# ======================================
# Scanner Score
# ======================================

ROI_WEIGHT = 0.40
WINRATE_WEIGHT = 0.25
PF_WEIGHT = 0.25
DD_WEIGHT = 0.10

# ==========================================
# Strategy
# ==========================================

STRATEGY = "macd"