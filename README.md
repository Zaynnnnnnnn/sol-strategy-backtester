# SOL Trading Strategy Backtester (SMA + RSI)

This repo contains a small Python backtester I wrote to sanity-check a simple rule-based strategy on **SOL-USD** using historical candles.

It does **not** place live trades. The goal was to practice:
- turning “trading intuition” into deterministic rules
- basic risk management (TP/SL)
- measuring outcomes (return, win-rate, trade count)

## Strategy (what it does)
**Data:** historical SOL-USD candles pulled via `yfinance` (configurable window).  
**Signals:**
- **Enter (buy):** short SMA crosses above long SMA **and** RSI is above a threshold (momentum filter).
- **Exit (sell):**
  - take-profit at **+5%**
  - stop-loss at **-1%**

The script walks candle-by-candle, simulates entries/exits, and prints a summary (final value, P/L, return %, win rate).

> Note: the default parameters reflect what I tested at the time. They’re easy to change in the script.

## Files
- `sol_bot.py` — runs the backtest for a single set of parameters
- `optimiser_sol.py` — runs simple parameter sweeps to compare outcomes

## How to run
1. Create a virtual environment (recommended)
2. Install dependencies:
   ```bash
   pip install yfinance pandas numpy
Run:
python sol_bot.py

What I learned

Backtests can look “great” for the wrong reasons (bad assumptions, look-ahead bias, unrealistic fills).
Small changes in thresholds (SMA windows, RSI cutoff, TP/SL) can change results a lot.
You need to validate both logic (is the rule correct?) and measurement (is ROI computed correctly?).

Limitations (current)
This is not live trading (no exchange connectivity, no order execution, no slippage/fees modeling by default).
It hasn’t been stress-tested on real-time streams; it’s a historical backtest sandbox.
Strategy is intentionally simple — it’s a baseline, not a production system.

Disclaimer
Educational project only. Not financial advice.
