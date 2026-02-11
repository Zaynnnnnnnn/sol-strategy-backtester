# SOL Strategy Backtester

A small, structured backtesting engine I built to evaluate rule-based trading strategies on historical crypto data.

The goal wasn’t to build a “money printer.” It was to build something clean and realistic — while avoiding common beginner mistakes like look-ahead bias and unrealistic fills.

## What the strategy does

The current implementation uses:

- Short/long Simple Moving Average (SMA) crossover  
- RSI confirmation  
- Percentage-based take profit and stop loss  
- Long-only (deploys capital on entry)

**Execution model:** signals are generated on candle *t*, and trades execute on candle *t+1 open* (to reduce look-ahead bias).  
Fees and slippage are also modeled.

## What the engine tracks

- Equity curve (mark-to-market)
- Trade log
- Trade-level returns
- Sharpe ratio
- Max drawdown
- Profit factor
- Win rate

## Equity curve

![Equity curve](equity_curve.png)

## How to run

Install:

```bash
pip install -r requirements.txt
Run a backtest:

python -m src.cli --symbol SOL-USD --period 6mo --interval 1h
Run the optimizer:

python -m src.cli --optimize
Run tests:

python -m pytest -q
Limitations
Long-only

Simple position sizing (full capital)

No walk-forward validation / out-of-sample testing

Not connected to live execution

Disclaimer
For research and educational purposes only. Not financial advice.


Commit:
```powershell
git add README.md
git commit -m "docs: improve README formatting and add usage"
git push
