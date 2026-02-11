import pandas as pd
from src.indicators import sma, rsi


def test_sma():
    s = pd.Series([1, 2, 3, 4, 5], dtype=float)
    out = sma(s, 3)
    assert pd.isna(out.iloc[0])
    assert out.iloc[2] == 2.0
    assert out.iloc[4] == 4.0


def test_rsi_bounds():
    s = pd.Series([1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5], dtype=float)
    out = rsi(s, 14)
    val = out.iloc[-1]
    assert pd.isna(val) or (0.0 <= float(val) <= 100.0)
