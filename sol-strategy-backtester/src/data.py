import pandas as pd
import yfinance as yf


def fetch_ohlc(symbol: str, period: str, interval: str) -> pd.DataFrame:
    """
    Downloads OHLCV data using yfinance.
    Returns columns: Open, High, Low, Close, Volume.
    """
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False)
    if df is None or df.empty:
        raise ValueError(f"No data returned for {symbol} period={period} interval={interval}")

    keep = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
    df = df[keep].dropna()

    if "Open" not in df.columns or "Close" not in df.columns:
        raise ValueError("Expected OHLC columns not found in downloaded data.")

    return df
