from itertools import product

import pandas as pd

from .backtest import ExecutionParams, run_backtest
from .metrics import summarize
from .strategy import StrategyParams


def grid_search(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple parameter sweep (not fancy).
    Returns a DataFrame sorted by return and then by max drawdown.
    """
    short_windows = [5, 10, 15]
    long_windows = [30, 40, 60]
    rsi_thresholds = [55.0, 60.0, 67.0]
    tps = [0.03, 0.05, 0.10]
    sls = [0.01, 0.02]

    rows = []

    for sw, lw, rsi_t, tp, sl in product(short_windows, long_windows, rsi_thresholds, tps, sls):
        if sw >= lw:
            continue

        sp = StrategyParams(short_window=sw, long_window=lw, rsi_threshold=rsi_t)
        ep = ExecutionParams(take_profit_pct=tp, stop_loss_pct=sl)

        equity_df, _, trade_returns = run_backtest(df, sp, ep)
        perf = summarize(equity_df, trade_returns, ep.initial_cash)

        rows.append({
            "short": sw,
            "long": lw,
            "rsi_thr": rsi_t,
            "tp": tp,
            "sl": sl,
            "return_pct": perf.return_pct,
            "max_dd_pct": perf.max_drawdown_pct,
            "trades": perf.trades,
            "win_rate_pct": perf.win_rate_pct,
            "sharpe": perf.sharpe,
        })

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    return out.sort_values(by=["return_pct", "max_dd_pct"], ascending=[False, False]).reset_index(drop=True)
