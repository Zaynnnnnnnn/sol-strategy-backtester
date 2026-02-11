from dataclasses import dataclass

import pandas as pd

from .indicators import sma, rsi


@dataclass(frozen=True)
class StrategyParams:
    short_window: int = 10
    long_window: int = 40
    rsi_window: int = 14
    rsi_threshold: float = 67.0


def compute_signals(df: pd.DataFrame, p: StrategyParams) -> pd.DataFrame:
    """
    Entry signal is created at candle t, but we will EXECUTE at candle t+1 open
    to avoid look-ahead bias.
    """
    out = df.copy()
    out["SMA_short"] = sma(out["Close"], p.short_window)
    out["SMA_long"] = sma(out["Close"], p.long_window)
    out["RSI"] = rsi(out["Close"], p.rsi_window)

    above = out["SMA_short"] > out["SMA_long"]
    crossover_up = (above.astype(int).diff() == 1)

    out["entry_signal"] = crossover_up & (out["RSI"] > p.rsi_threshold)
    return out
