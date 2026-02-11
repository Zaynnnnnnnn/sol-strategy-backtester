import pandas as pd

from src.strategy import StrategyParams
from src.backtest import ExecutionParams, run_backtest


def test_backtest_runs():
    idx = pd.date_range("2024-01-01", periods=500, freq="h")
    close = pd.Series(range(1, len(idx) + 1), index=idx, dtype=float)

    df = pd.DataFrame({
        "Open": close.shift(1).fillna(close.iloc[0]),
        "High": close * 1.01,
        "Low": close * 0.99,
        "Close": close,
        "Volume": 1000
    }, index=idx)

    sp = StrategyParams(short_window=5, long_window=20, rsi_threshold=50.0)
    ep = ExecutionParams(initial_cash=10_000.0, fee_pct=0.0, slippage_pct=0.0)

    equity_df, trades, trade_returns = run_backtest(df, sp, ep)

    assert "Equity" in equity_df.columns
    assert len(equity_df) > 0
    assert equity_df["Equity"].iloc[-1] > 0
    assert isinstance(trades, list)
    assert isinstance(trade_returns, list)
