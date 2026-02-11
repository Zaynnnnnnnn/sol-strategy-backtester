from dataclasses import dataclass
from typing import Any, List, Tuple

import pandas as pd

from .strategy import StrategyParams, compute_signals


# ==============================
# Execution Parameters
# ==============================

@dataclass(frozen=True)
class ExecutionParams:
    initial_cash: float = 10_000.0
    take_profit_pct: float = 0.05
    stop_loss_pct: float = 0.01
    fee_pct: float = 0.001        # 0.1% fee per trade side
    slippage_pct: float = 0.0002  # 0.02% slippage per trade side


@dataclass
class Trade:
    side: str   # BUY or SELL
    time: Any
    price: float
    qty: float
    fee: float


# ==============================
# Helper
# ==============================

def _effective_price(price: float, side: str, slippage_pct: float) -> float:
    """
    Applies simple slippage model:
      - BUY pays slightly more
      - SELL receives slightly less
    """
    if side == "BUY":
        return price * (1.0 + slippage_pct)
    return price * (1.0 - slippage_pct)


# ==============================
# Backtest Engine
# ==============================

def run_backtest(
    df: pd.DataFrame,
    sp: StrategyParams,
    ep: ExecutionParams
) -> Tuple[pd.DataFrame, List[Trade], List[float]]:
    """
    Long-only backtest:
      - Entry signal computed on candle t
      - Order executes on candle t+1 OPEN (reduces look-ahead bias)
      - Exit trigger checks candle t CLOSE vs entry
        and executes on t+1 OPEN
    """

    data = compute_signals(df, sp).dropna().copy()
    if len(data) < 2:
     data = compute_signals(df, sp).copy()
     data["Equity"] = pd.Series(dtype=float)
    

    cash = ep.initial_cash  
    qty = 0.0
    entry_price = None

    equity: List[float] = []
    trades: List[Trade] = []
    trade_returns: List[float] = []

    for i in range(len(data) - 1):

        close_i = data["Close"].iloc[i].item()
        next_open = data["Open"].iloc[i + 1].item()
        entry_signal = bool(data["entry_signal"].iloc[i])

        # Mark-to-market equity at close
        equity.append(cash + qty * close_i)

        # =======================
        # EXIT LOGIC
        # =======================
        if qty > 0.0 and entry_price is not None:

            current_return = (close_i - entry_price) / entry_price
            hit_tp = current_return >= ep.take_profit_pct
            hit_sl = current_return <= -ep.stop_loss_pct

            if hit_tp or hit_sl:
                sell_price = _effective_price(next_open, "SELL", ep.slippage_pct)

                notional = qty * sell_price
                fee = notional * ep.fee_pct

                cash = notional - fee

                trades.append(
                    Trade("SELL", data.index[i + 1], sell_price, qty, fee)
                )

                trade_returns.append(
                    (sell_price - entry_price) / entry_price
                )

                qty = 0.0
                entry_price = None

        # =======================
        # ENTRY LOGIC
        # =======================
        if qty == 0.0 and entry_signal:

            buy_price = _effective_price(next_open, "BUY", ep.slippage_pct)

            qty = cash / buy_price
            notional = qty * buy_price
            fee = notional * ep.fee_pct

            cash = cash - fee

            trades.append(
                Trade("BUY", data.index[i + 1], buy_price, qty, fee)
            )

            entry_price = buy_price

    # Final equity calculation
    last_close = data["Close"].iloc[-1].item()
    final_value = cash + qty * last_close
    equity.append(final_value)

    data = data.iloc[: len(equity)].copy()
    data["Equity"] = pd.Series(equity, index=data.index)

    return data, trades, trade_returns
