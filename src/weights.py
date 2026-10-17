"""BAIX - calculate constituent weights (tier budgets 75/25, 20% cap)."""
import sys
import pandas as pd

PURE_BUDGET = 0.75
CAP = 0.20
CONSTITUENTS = "data/processed/constituents_DRAFT.csv"
OUT = "data/processed/weights_DRAFT.csv"


def cap_within_tier(w, cap):
    """Cut weights above the cap and share the excess among the others, repeat."""
    w = w.copy()
    for _ in range(100):
        over = w > cap + 1e-12
        if not over.any():
            break
        excess = (w[over] - cap).sum()
        w[over] = cap
        free = w < cap - 1e-12
        if not free.any():
            break
        w[free] += excess * w[free] / w[free].sum()
    return w


def main(price_date=None):
    cons = pd.read_csv(CONSTITUENTS)
    ff = pd.read_csv("data/raw/free_float.csv")[["symbol", "free_float_pct"]]
    sh = pd.read_csv("data/raw/shares_yahoo.csv")[["symbol", "shares_outstanding"]]
    close = pd.read_csv("data/raw/prices/close.csv", index_col=0, parse_dates=True)

    if price_date is None:
        price_date = close.index.max()
    else:
        price_date = close.index[close.index <= pd.Timestamp(price_date)].max()
    prices = close.loc[price_date].rename("price").rename_axis("symbol").reset_index()

    df = cons.merge(ff, on="symbol").merge(sh, on="symbol").merge(prices, on="symbol")
    if len(df) != len(cons):
        missing = set(cons.symbol) - set(df.symbol)
        sys.exit(f"Missing data for: {missing}")
    if df.price.isna().any():
        sys.exit(f"No price on {price_date.date()} for: {list(df[df.price.isna()].symbol)}")

    df["ff_mcap_cr"] = df.price * df.shares_outstanding * df.free_float_pct / 100 / 1e7
    df["raw"] = df.ff_mcap_cr * df.ai_score

    n = len(df)
    cap = max(CAP, 1 / n)                      # Section 7.3: if fewer than 5 stocks, cap = 1/N
    n_pure = (df.tier == "pure").sum()
    n_broad = (df.tier == "broad").sum()
    cap_p = max(cap, PURE_BUDGET / n_pure) if n_pure else cap   # Rule A: pure-tier cap safety net
    cap_pure, cap_broad = cap_p * n_pure, cap * n_broad   # most weight each tier can hold
    if n_broad == 0:
        b_pure, b_broad = 1.0, 0.0
    elif n_pure == 0:
        b_pure, b_broad = 0.0, 1.0
    else:
        b_pure = min(PURE_BUDGET, cap_pure)
        b_broad = 1 - b_pure
        if b_broad > cap_broad:
            b_broad = cap_broad
            b_pure = 1 - b_broad

    df["weight"] = 0.0
    for tier, budget in (("pure", b_pure), ("broad", b_broad)):
        m = df.tier == tier
        if m.any():
            w = budget * df.loc[m, "raw"] / df.loc[m, "raw"].sum()
            df.loc[m, "weight"] = cap_within_tier(w, cap_p if tier == "pure" else cap)

    df = df.sort_values(["tier", "weight"], ascending=[False, False])
    df[["symbol", "tier", "ai_score", "price", "free_float_pct", "ff_mcap_cr", "weight"]].to_csv(OUT, index=False)

    print(f"Price date: {price_date.date()} | stocks: {n} | cap: {cap:.0%} | pure-tier cap: {cap_p:.0%}")
    print(f"Tier budgets -> pure {b_pure:.1%}, broad {b_broad:.1%}\n")
    show = df[["symbol", "tier", "ai_score", "ff_mcap_cr", "weight"]].copy()
    show["ff_mcap_cr"] = show.ff_mcap_cr.round(0).astype(int)
    show["weight"] = (show.weight * 100).round(2).astype(str) + "%"
    print(show.to_string(index=False))
    print(f"\nTotal weight: {df.weight.sum():.4f}  (must be 1.0000)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
