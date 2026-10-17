"""BAIX - daily index level from a base date (TEST mode until the official launch)."""
import sys
import pandas as pd
import weights

BASE_VALUE = 1000.0
K = 1e9                      # notional index market value on the base date
OUT = "data/processed/baix_TEST.csv"


def main(base_date):
    weights.main(base_date)                              # weights on base-date prices
    w = pd.read_csv(weights.OUT).set_index("symbol")
    close = pd.read_csv("data/raw/prices/close.csv", index_col=0, parse_dates=True)
    base = close.index[close.index <= pd.Timestamp(base_date)].max()

    p0 = close.loc[base, w.index]
    index_shares = w["weight"] * K / p0                  # fixed until the next review
    divisor = K / BASE_VALUE                             # makes the index = 1,000 on base date

    px = close.loc[base:, w.index].ffill()
    level = (px * index_shares).sum(axis=1) / divisor

    out = pd.DataFrame({"BAIX": level.round(2)})
    for b in ("NIFTY50", "NIFTYIT"):                     # benchmarks rebased to 1,000
        if b in close:
            s = close.loc[base:, b].ffill()
            out[b] = (s / s.iloc[0] * BASE_VALUE).round(2)
    out.index.name = "date"
    out.to_csv(OUT)

    print(f"\nBase date: {base.date()} | divisor: {divisor:,.0f}")
    print(out.tail(5).to_string())
    print("\nReturn since base date:")
    for c in out.columns:
        print(f"  {c:8s} {out[c].iloc[-1] / BASE_VALUE - 1:+.2%}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python src/index_level.py YYYY-MM-DD   (base date)")
    main(sys.argv[1])
