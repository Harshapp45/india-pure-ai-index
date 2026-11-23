"""BAIX - daily index level.

LIVE (the official index):  python src/index_level.py 2026-11-13 live
    uses the frozen base-date index shares and divisor, so history can never be rewritten.
TEST (engine testing only): python src/index_level.py 2026-07-01
    recalculates weights from today's data files; never official history.
"""
import json
import sys
import pandas as pd
import weights
import corporate_actions as ca
from pathlib import Path
from prices import BENCHMARKS, GLOBAL

BASE_VALUE = 1000.0
K = 1e9                      # notional index market value on the base date
OUT_TEST = "data/processed/baix_TEST.csv"
OUT_LIVE = "data/processed/baix_LIVE.csv"
WEIGHTS_LIVE = "data/processed/weights_LIVE.csv"      # today's weights, after price drift


def main(base_date, live=False):
    close = pd.read_csv("data/raw/prices/close.csv", index_col=0, parse_dates=True)

    if live:
        folder = Path("data/frozen") / base_date
        w = pd.read_csv(folder / "index_shares.csv").set_index("symbol")
        meta = json.loads((folder / "index_meta.json").read_text())
        base = pd.Timestamp(base_date)
        index_shares = w["index_shares"]
        divisor = meta["divisor"]
        out_path = OUT_LIVE
    else:
        weights.main(base_date)                          # weights on base-date prices
        w = pd.read_csv(weights.OUT).set_index("symbol")
        base = close.index[close.index <= pd.Timestamp(base_date)].max()
        p0 = close.loc[base, w.index]
        index_shares = w["weight"] * K / p0              # fixed until the next review
        divisor = K / BASE_VALUE                         # makes the index = 1,000 on base date
        out_path = OUT_TEST

    px = close.loc[base:, w.index].ffill()
    level = (px * index_shares).sum(axis=1) / divisor

    if live and abs(level.iloc[0] - BASE_VALUE) > 0.01:
        # The stored base-date prices no longer match the freeze: almost always a split or bonus
        # that the price source has adjusted backwards. A human must adjust the index shares.
        sys.exit(f"STOP: BAIX on the base date is {level.iloc[0]:.2f}, not 1,000. "
                 "Base-date prices have changed since the freeze (split or bonus?). "
                 "Check data/processed/corporate_actions.csv before publishing.")

    # BAIX TR: dividends reinvested across the whole index on the ex-date (methodology Section 9)
    #   TR(t) = TR(t-1) x [PR(t) + dividend points(t)] / PR(t-1)
    adj = pd.read_csv("data/raw/prices/adj_close.csv", index_col=0, parse_dates=True)
    div = ca.dividends(close, adj, list(w.index)).reindex(px.index).fillna(0.0)
    div.iloc[0] = 0.0                                    # nothing reinvested on the base date itself
    div_points = (div[w.index] * index_shares).sum(axis=1) / divisor
    growth = (level + div_points) / level.shift(1)
    tr = BASE_VALUE * growth.fillna(1.0).cumprod()

    out = pd.DataFrame({"BAIX": level.round(2), "BAIX_TR": tr.round(2)})
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
    out.to_csv(out_path)

    if live:                                             # today's weights: base weights moved by prices
        value = px.iloc[-1] * index_shares
        cw = w[["tier", "ai_score"]].copy()
        cw["weight"] = value / value.sum()
        cw.reset_index().to_csv(WEIGHTS_LIVE, index=False)

    print(f"\n{'LIVE' if live else 'TEST'} | base date: {base.date()} | divisor: {divisor:,.0f}")
    print(out.tail(5).to_string())
    print("\nReturn since base date:")
    for c in out.columns:
        print(f"  {c:8s} {out[c].iloc[-1] / BASE_VALUE - 1:+.2%}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python src/index_level.py YYYY-MM-DD [live]   (base date)")
    main(sys.argv[1], live=len(sys.argv) > 2 and sys.argv[2].lower() == "live")
