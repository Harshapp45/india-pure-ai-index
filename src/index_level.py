"""BAIX - daily index level from a base date (TEST mode until the official launch)."""
import sys
import pandas as pd
import weights
from pathlib import Path
from prices import BENCHMARKS, GLOBAL

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
    for b in BENCHMARKS:                                 # benchmarks rebased to 1,000
        if b not in close:
            continue
        s = close.loc[base:, b].ffill()
        if pd.isna(s.iloc[0]):                           # no price on the base date: skip, don't break the site
            print(f"  WARNING: {b} has no price on the base date - left out")
            continue
        out[b] = (s / s.iloc[0] * BASE_VALUE).round(2)
    gpath = Path("data/raw/prices/global.csv")             # global benchmarks, in rupees
    if gpath.exists():
        g = pd.read_csv(gpath, index_col=0, parse_dates=True)
        for k in GLOBAL:
            col = k + "_INR"
            if col not in g or g[col].dropna().empty:
                continue
            s = g[col].dropna()
            s.index = s.index + pd.Timedelta(days=1)       # US closes after India: use the previous US close
            s = s.reindex(s.index.union(out.index)).ffill().reindex(out.index)
            if pd.isna(s.iloc[0]):
                print(f"  WARNING: {k} has no price on the base date - left out")
                continue
            out[k] = (s / s.iloc[0] * BASE_VALUE).round(2)
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
