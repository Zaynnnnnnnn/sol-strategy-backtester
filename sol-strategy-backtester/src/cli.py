import argparse

from .data import fetch_ohlc
from .backtest import ExecutionParams, run_backtest
from .metrics import summarize
from .strategy import StrategyParams
from .optimizer import grid_search


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", default="SOL-USD")
    p.add_argument("--period", default="6mo")
    p.add_argument("--interval", default="1h")

    p.add_argument("--short", type=int, default=10)
    p.add_argument("--long", type=int, default=40)
    p.add_argument("--rsi_threshold", type=float, default=67.0)

    p.add_argument("--tp", type=float, default=0.05)
    p.add_argument("--sl", type=float, default=0.01)
    p.add_argument("--fee", type=float, default=0.001)
    p.add_argument("--slippage", type=float, default=0.0002)
    p.add_argument("--cash", type=float, default=10_000.0)

    p.add_argument("--optimize", action="store_true", help="Run a simple grid search")

    args = p.parse_args()

    df = fetch_ohlc(args.symbol, args.period, args.interval)

    if args.optimize:
        results = grid_search(df)
        print("\nTop 10 configs:")
        print(results.head(10).to_string(index=False))
        return

    sp = StrategyParams(short_window=args.short, long_window=args.long, rsi_threshold=args.rsi_threshold)
    ep = ExecutionParams(
        initial_cash=args.cash,
        take_profit_pct=args.tp,
        stop_loss_pct=args.sl,
        fee_pct=args.fee,
        slippage_pct=args.slippage,
    )

    equity_df, trades, trade_returns = run_backtest(df, sp, ep)
    perf = summarize(equity_df, trade_returns, ep.initial_cash)

    print("\n Backtest Summary")
    print(f"Symbol: {args.symbol} | period={args.period} interval={args.interval}")
    print(f"Final Value: ${perf.final_value:,.2f}")
    print(f"Profit:      ${perf.profit:,.2f}")
    print(f"Return:      {perf.return_pct:.2f}%")
    print(f"Trades:      {perf.trades}")
    print(f"Win Rate:    {perf.win_rate_pct:.2f}%")
    print(f"Avg Trade:   {perf.avg_trade_return_pct:.2f}%")
    print(f"Max DD:      {perf.max_drawdown_pct:.2f}%")
    print(f"ProfitFact:  {perf.profit_factor:.2f}")
    print(f"Sharpe:      {perf.sharpe:.2f}")
    print(f"Trade log entries: {len(trades)}")


if __name__ == "__main__":
    main()
