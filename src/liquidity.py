"""BAIX - size and liquidity check (methodology Section 4, rule 2).

For every candidate, over the 6 months to the cut-off date:
  - average daily traded value (price x shares traded on NSE) must be >= Rs 5 crore
  - free-float market cap must be >= Rs 1,000 crore
Writes data/processed/liquidity_check.csv. Run: python src/liquidity.py [cut-off YYYY-MM-DD]
"""
import sys
import pandas as pd
from prices import CANDIDATES

MIN_ADTV_CR = 5          # Rs crore a day
MIN_FFMCAP_CR = 1000     # Rs crore
CRORE = 1e7
OUT = "data/processed/liquidity_check.csv"


def main(cutoff=None):
    close = pd.read_csv("data/raw/prices/close.csv", index_col=0, parse_dates=True)
    vol = pd.read_csv("data/raw/prices/volume.csv", index_col=0, parse_dates=True)
    ff = pd.read_csv("data/raw/free_float.csv").set_index("symbol")["free_float_pct"]
    sh = pd.read_csv("data/raw/shares_yahoo.csv").set_index("symbol")["shares_outstanding"]

    end = close.index[close.index <= pd.Timestamp(cutoff)].max() if cutoff else close.index.max()
    start = end - pd.DateOffset(months=6)
    win = (close.index > start) & (close.index <= end)

    rows = []
    for s in CANDIDATES:
        if s not in close or s not in vol:
            continue
        tv = (close.loc[win, s] * vol.loc[win, s]).dropna()
        tv = tv[tv > 0]                                    # skip days with no trading
        adtv = tv.mean() / CRORE if len(tv) else float("nan")
        px = close.loc[:end, s].dropna().iloc[-1]
        ffm = px * sh.get(s, float("nan")) * ff.get(s, float("nan")) / 100 / CRORE
        rows.append({
            "symbol": s,
            "days": len(tv),
            "adtv_cr": round(adtv, 2),
            "median_tv_cr": round(tv.median() / CRORE, 2) if len(tv) else None,
            "ff_mcap_cr": round(ffm, 0),
            "pass_adtv": adtv >= MIN_ADTV_CR,
            "pass_ffmcap": ffm >= MIN_FFMCAP_CR,
        })
    df = pd.DataFrame(rows)
    df["result"] = (df.pass_adtv & df.pass_ffmcap).map({True: "PASS", False: "FAIL"})
    df = df.sort_values("adtv_cr")
    df.to_csv(OUT, index=False)

    print(f"Liquidity window: {start.date()} to {end.date()}")
    print(df.to_string(index=False))
    fails = df[df.result == "FAIL"].symbol.tolist()
    print("\nAll candidates pass." if not fails else f"\nFAIL: {fails}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
