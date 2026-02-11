import matplotlib.pyplot as plt

from .data import fetch_ohlc
from .strategy import StrategyParams
from .backtest import ExecutionParams, run_backtest


def plot_equity_curve(
    symbol="SOL-USD",
    period="6mo",
    interval="1h"
):
    df = fetch_ohlc(symbol, period, interval)

    sp = StrategyParams()
    ep = ExecutionParams()

    equity_df, trades, trade_returns = run_backtest(df, sp, ep)

    plt.figure(figsize=(10, 6))
    plt.plot(equity_df.index, equity_df["Equity"])
    plt.title(f"Equity Curve — {symbol}")
    plt.xlabel("Time")
    plt.ylabel("Portfolio Value ($)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("equity_curve.png", dpi=150)
    plt.show()

    print("Saved equity_curve.png")


if __name__ == "__main__":
    plot_equity_curve()
