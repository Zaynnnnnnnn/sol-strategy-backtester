SOL Strategy Backtester

This project is a small but structured backtesting engine I built to evaluate rule-based trading strategies on historical crypto data.
The goal wasn’t to build a “money printer.” It was to build something clean, realistic, and easy to extend — while avoiding common beginner mistakes like look-ahead bias and unrealistic fills.
What the strategy does
The current implementation uses:
A short/long Simple Moving Average crossover
RSI as confirmation
Percentage-based take profit and stop loss
It’s long-only and fully deploys capital on entry.
Signals are generated on candle t, and trades execute on candle t+1 open.
That small detail is important — it prevents using information that wouldn’t have been available in live trading.
Fees and slippage are also modeled to make results more realistic.
What the engine tracks
Equity curve (mark-to-market)
Trade log
Trade-level returns
Sharpe ratio
Max drawdown
Profit factor
Win rate
The idea is to focus not just on return, but on risk and consistency.

Example run (SOL-USD, 6mo, 1h)
Final Value: $11,384.05
Return:      13.84%
Trades:      28
Win Rate:    32.14%
Max DD:      -56.25%
Sharpe:      3.38

The relatively high drawdown reflects the limitations of simple crossover systems, especially in choppy markets. That’s expected and highlights where further improvements could be made.
Project structure
src/
 ├── backtest.py      # Execution engine
 ├── strategy.py      # Signal logic
 ├── data.py          # Historical data loader
 ├── metrics.py       # Performance calculations
 ├── optimizer.py     # Grid search over parameters
 ├── cli.py           # Command-line interface
 ├── plot_equity.py   # Equity curve visualization

tests/
 └── test_backtest.py

The code is intentionally modular so components (strategy, execution model, metrics) can be swapped or extended independently.

How to run
Install dependencies:
pip install -r requirements.txt

Run a backtest:
python -m src.cli --symbol SOL-USD --period 6mo --interval 1h


Run the optimizer:
python -m src.cli --optimize


Generate an equity curve plot:
python -m src.plot_equity


Run tests:
python -m pytest -q

Limitations
This is intentionally simple. Some current limitations:
Long-only
No position sizing logic beyond full capital deployment
No walk-forward validation
No regime filtering
Not connected to live execution
If extended further, I would look into volatility filters, risk-adjusted sizing, and out-of-sample validation.

Why I built this
I wanted to better understand:
How execution assumptions affect performance
How easily backtests can become biased
How to structure a small research system cleanly
It’s a learning project, but built with realistic assumptions and testing in mind.

Disclaimer
For research and educational purposes only. Not financial advice.