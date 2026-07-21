# StockBacktestPro

A modular Python backtesting framework for Taiwan and US stock markets.

---

## Features

- EMA60/240 Trend Following Strategy
- Taiwan & US Stock Support
- Daily / Weekly Timeframe
- Portfolio Backtesting
- Stock Scanner
- Performance Report
- Modular Architecture

---

## Project Structure

```text
StockBacktestPro/
│
├── backtest.py
├── scanner.py
├── config.py
│
├── core/
│   ├── engine.py
│   └── portfolio.py
│
├── strategies/
│   └── ema60240.py
│
├── utils/
│   └── indicators.py
│
├── reports/
│   └── report.py
│
├── data/
├── output/
└── backup/
```

---

## Installation

```bash
git clone https://github.com/i5152535455/StockBacktestPro.git
cd StockBacktestPro
pip install -r requirements.txt
```

---

## Usage

Run Backtest

```bash
python backtest.py
```

Run Scanner

```bash
python scanner.py
```

---

## Current Strategy Performance

| Metric | Result |
|--------|-------:|
| ROI | 26.55% |
| Profit Factor | 7.57 |
| Max Drawdown | 1.86% |
| Trades | 26 |

---

## Roadmap

### v1.0

- [x] EMA60/240 Strategy
- [x] Portfolio Backtesting
- [x] Scanner
- [x] Modular Architecture

### v1.1

- [ ] ATR Stop Loss
- [ ] ATR Trailing Stop

### v1.2

- [ ] RSI Strategy
- [ ] MACD Strategy
- [ ] Bollinger Bands

### v2.0

- [ ] Parameter Optimization
- [ ] Walk Forward Analysis
- [ ] Monte Carlo Simulation

---

## License

MIT License