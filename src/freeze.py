"""BAIX - one-time freeze of the base-date weights, index shares and divisor.

Run once, after the base date's closing prices have arrived:
    python src/freeze.py 2026-11-13
It refuses to overwrite an existing freeze, because index history must never be rewritten.
"""
import json
import sys
from pathlib import Path
import pandas as pd
import weights

BASE_VALUE = 1000.0
K = 1e9                      # notional index market value on the base date


def main(base_date):
    folder = Path("data/frozen") / base_date
    out = folder / "index_shares.csv"
    if out.exists():
        sys.exit(f"{out} already exists. A freeze is never overwritten.")

    # The inputs must be exactly the ones saved on the base date
    pairs = [(folder / "constituents.csv", Path(weights.CONSTITUENTS)),
             (folder / "free_float.csv", Path("data/raw/free_float.csv")),
             (folder / "shares_official.csv", Path("data/raw/shares_official.csv")),
             (folder / "shares_yahoo.csv", Path("data/raw/shares_yahoo.csv"))]
    for frozen, current in pairs:
        if frozen.read_text() != current.read_text():
            sys.exit(f"{current} has changed since the base date. Restore it from {frozen} first.")

    close = pd.read_csv("data/raw/prices/close.csv", index_col=0, parse_dates=True)
    base = pd.Timestamp(base_date)
    if base not in close.index:
        sys.exit(f"No prices for {base_date} yet. Try again once the data has arrived.")

    weights.main(base_date)                                   # weights on base-date closing prices
    w = pd.read_csv(weights.OUT).set_index("symbol")
    p0 = close.loc[base, w.index]
    if p0.isna().any():
        sys.exit(f"Missing base-date price for: {list(p0[p0.isna()].index)}")

    w["base_price"] = p0
    w["index_shares"] = w["weight"] * K / p0                  # fixed until the next review
    divisor = K / BASE_VALUE                                  # makes BAIX = 1,000 at the base-date close
    w.reset_index()[["symbol", "tier", "ai_score", "base_price", "ff_mcap_cr", "weight", "index_shares"]] \
        .to_csv(out, index=False)
    (folder / "index_meta.json").write_text(json.dumps(
        {"base_date": base_date, "base_value": BASE_VALUE, "notional": K, "divisor": divisor}, indent=1))

    check = (p0 * w["index_shares"]).sum() / divisor
    print(f"\nFrozen {len(w)} constituents for base date {base_date}")
    print(f"Divisor: {divisor:,.0f} | BAIX at the base-date close: {check:,.2f}")
    print(f"Saved {out} and {folder / 'index_meta.json'}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python src/freeze.py YYYY-MM-DD   (base date)")
    main(sys.argv[1])
