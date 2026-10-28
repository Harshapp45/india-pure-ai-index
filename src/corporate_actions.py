"""BAIX - corporate actions: dividends for BAIX TR, and alarms for events that need a human.

Dividends are worked out from two prices Yahoo already gives us every day:
  Close      - the plain closing price (adjusted for splits and bonuses only)
  Adj Close  - the closing price also adjusted for dividends
On an ex-dividend date the gap between them changes. If f = Adj Close / Close, then
  dividend per share on day t = Close(t-1) x (1 - f(t-1) / f(t))

Alarms (methodology Section 10) - the robot never changes the index on its own:
  - a daily move beyond +/-25%     -> possible split or bonus that Yahoo has not adjusted
  - a dividend above 5% of price   -> possible special dividend (price adjustment needed)
  - no new price for 3+ days       -> possible suspension or delisting

Run: python src/corporate_actions.py YYYY-MM-DD   (base date)
"""
import sys
import pandas as pd

BIG_MOVE = 0.25
SPECIAL_DIV = 0.05
STALE_DAYS = 3
TOL = 1e-4                    # ignore tiny rounding changes in Yahoo's adjustment
LOG = "data/processed/corporate_actions.csv"


def load_prices():
    close = pd.read_csv("data/raw/prices/close.csv", index_col=0, parse_dates=True)
    adj = pd.read_csv("data/raw/prices/adj_close.csv", index_col=0, parse_dates=True)
    return close, adj


def dividends(close, adj, symbols):
    """Cash dividend per share on each ex-date (0 on other days), in rupees."""
    cols = [s for s in symbols if s in close and s in adj]
    f = (adj[cols] / close[cols]).ffill()
    step = f / f.shift(1)
    d = close[cols].ffill().shift(1) * (1 - 1 / step)
    return d.where(step - 1 > TOL, 0.0).fillna(0.0)


def check(close, adj, symbols, start):
    """Return a list of events since `start` (dividends and alarms)."""
    events = []
    px = close.loc[start:, [s for s in symbols if s in close]]
    div = dividends(close, adj, symbols).loc[start:]
    prev = close[px.columns].ffill().shift(1).loc[start:]

    for s in px.columns:
        for t, v in div[s][div[s] > 0].items():
            y = v / prev.at[t, s]
            kind = "ALARM: possible special dividend" if y > SPECIAL_DIV else "dividend"
            events.append({"date": t.date(), "symbol": s, "event": kind,
                           "detail": f"Rs {v:.2f} per share ({y:.2%} of price)"})
        r = px[s].pct_change(fill_method=None)
        for t, v in r[r.abs() > BIG_MOVE].items():
            events.append({"date": t.date(), "symbol": s, "event": "ALARM: possible split/bonus",
                           "detail": f"price moved {v:+.1%} in one day - check NSE corporate actions"})
        last = px[s].last_valid_index()
        behind = (px.index > last).sum() if last is not None else len(px)
        if behind >= STALE_DAYS:
            events.append({"date": px.index[-1].date(), "symbol": s, "event": "ALARM: no new price",
                           "detail": f"no price for {behind} trading days - possible suspension or delisting"})
    return pd.DataFrame(events, columns=["date", "symbol", "event", "detail"]).sort_values(["date", "symbol"])


def main(base_date):
    close, adj = load_prices()
    symbols = pd.read_csv("data/processed/weights_DRAFT.csv").symbol.tolist()
    start = close.index[close.index <= pd.Timestamp(base_date)].max()
    ev = check(close, adj, symbols, start)
    ev.to_csv(LOG, index=False)
    print(f"Corporate actions since {start.date()} for {len(symbols)} constituents:")
    print(ev.to_string(index=False) if len(ev) else "  none")
    alarms = ev[ev.event.str.startswith("ALARM")]
    print(f"\n{len(alarms)} alarm(s) - review by hand." if len(alarms) else "\nNo alarms.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python src/corporate_actions.py YYYY-MM-DD   (base date)")
    main(sys.argv[1])
