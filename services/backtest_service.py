import config

from utils import indicators
from reports import report
from strategies.loader import get_strategy
from core import engine as backtest_engine


def run(filepath):
    """
    執行一次完整回測
    """

    strategy = get_strategy()
    info = strategy.get_info()

    # 讀資料
    df = indicators.load_data(filepath)

    # 轉換時間週期
    df = indicators.convert_timeframe(df)

    # 計算策略需要的指標
    df = strategy.prepare(df)

    # 建立買賣訊號
    df = strategy.generate_signal(df)

    # 執行回測
    trades = backtest_engine.run_backtest(
        df,
        verbose=config.VERBOSE
    )

    # 計算績效
    metrics = report.calculate_metrics(trades)

    return {
        "strategy": info,
        "data": df,
        "trades": trades,
        "metrics": metrics,
    }