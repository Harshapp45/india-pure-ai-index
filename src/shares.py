"""BAIX - fetch shares outstanding and free-float estimates from Yahoo Finance."""
import pandas as pd
import yfinance as yf
from prices import CANDIDATES


def main():
    rows = []
    for s in CANDIDATES:
        info = yf.Ticker(s + ".NS").info
        rows.append({
            "symbol": s,
            "shares_outstanding": info.get("sharesOutstanding"),
            "float_shares": info.get("floatShares"),
            "insider_pct": info.get("heldPercentInsiders"),
        })
    df = pd.DataFrame(rows)
    df["free_float_pct"] = (df["float_shares"] / df["shares_outstanding"]).round(3)
    df.to_csv("data/raw/shares_yahoo.csv", index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
