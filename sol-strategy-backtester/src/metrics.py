from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Performance:
    final_value: float
    profit: float
    return_pct: float
    trades: int
    win_rate_pct: float
    avg_trade_return_pct: float
    max_drawdown_pct: float
    profit_factor: float
    sharpe: float


def max_drawdown_pct(equity: pd.Series) -> float:
    peak = equity.cummax()
    dd = (equity / peak) - 1.0
    return float(dd.min() * 100.0)  # negative


def profit_factor(trade_returns: List[float]) -> float:
    gains = sum(r for r in trade_returns if r > 0)
    losses = -sum(r for r in trade_returns if r < 0)
    if losses == 0:
        return float("inf") if gains > 0 else 0.0
    return gains / losses


def sharpe_ratio(returns: pd.Series, annualization: float = 8760.0) -> float:
    r = returns.dropna()
    if len(r) < 2:
        return 0.0
    mu = r.mean()
    sigma = r.std(ddof=1)
    if sigma == 0 or np.isnan(sigma):
        return 0.0
    return float((mu / sigma) * np.sqrt(annualization))


def summarize(equity_df: pd.DataFrame, trade_returns: List[float], initial_cash: float) -> Performance:
    final_value = float(equity_df["Equity"].iloc[-1])
    profit = final_value - initial_cash
    return_pct = (profit / initial_cash) * 100.0

    trades = len(trade_returns)
    wins = sum(1 for r in trade_returns if r > 0)
    win_rate = (wins / trades) * 100.0 if trades else 0.0
    avg_trade = (sum(trade_returns) / trades) * 100.0 if trades else 0.0

    mdd = max_drawdown_pct(equity_df["Equity"])
    pf = profit_factor(trade_returns)

    returns = equity_df["Equity"].pct_change()
    sharpe = sharpe_ratio(returns)

    return Performance(
        final_value=final_value,
        profit=profit,
        return_pct=return_pct,
        trades=trades,
        win_rate_pct=win_rate,
        avg_trade_return_pct=avg_trade,
        max_drawdown_pct=mdd,
        profit_factor=pf,
        sharpe=sharpe,
    )
