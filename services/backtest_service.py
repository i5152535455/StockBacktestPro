import pandas as pd
import config

from utils import indicators
from reports import report
from strategies.loader import get_strategy
from core import engine as backtest_engine


def run(filepath, verbose=None):

    # 如果沒有指定，就使用 config.VERBOSE
    if verbose is None:
        verbose = config.VERBOSE

    strategy = get_strategy()
    info = strategy.get_info()

    # ======================================
    # 讀取完整歷史資料
    # ======================================

    df = indicators.load_data(filepath)

    # ======================================
    # 轉換時間週期
    # ======================================

    df = indicators.convert_timeframe(df)

    # ======================================
    # 計算 EMA
    # ======================================

    df = indicators.calculate_ema(df)

    # ======================================
    # MACD 策略才計算 MACD
    # ======================================

    if config.STRATEGY == "macd":
        df = indicators.calculate_macd(df)

    # ======================================
    # Strategy Prepare
    # ======================================

    df = strategy.prepare(df)

    # ======================================
    # 建立訊號
    # ======================================

    df = strategy.generate_signal(df)

    # ======================================
    # Debug
    # ======================================

    if verbose:

        print()
        print("========== Before Date Filter ==========")

        print(
            "Date:",
            df["Date"].min(),
            "->",
            df["Date"].max()
        )

        print(
            "BUY:",
            df["BUY"].sum(),
            "SELL:",
            df["SELL"].sum()
        )

    # ======================================
    # 回測日期
    # ======================================

    df = df[
        (df["Date"] >= pd.to_datetime(config.START_DATE)) &
        (df["Date"] <= pd.to_datetime(config.END_DATE))
    ].copy()

    if verbose:

        print()
        print("========== After Date Filter ==========")

        print(
            "Date:",
            df["Date"].min(),
            "->",
            df["Date"].max()
        )

        print(
            "BUY:",
            df["BUY"].sum(),
            "SELL:",
            df["SELL"].sum()
        )

    # ======================================
    # 回測
    # ======================================

    trades, equity_curve = backtest_engine.run_backtest(
        df,
        verbose=verbose
    )

    # ======================================
    # 績效
    # ======================================

    metrics = report.calculate_metrics(
        trades,
        equity_curve
    )

    return {
        "strategy": info,
        "data": df,
        "trades": trades,
        "metrics": metrics,
        "equity_curve": equity_curve,
    }