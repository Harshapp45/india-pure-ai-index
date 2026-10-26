"""BAIX - download daily closing prices for candidates and benchmarks."""
from pathlib import Path
import pandas as pd

CANDIDATES = ["NETWEB", "E2E", "FRACTAL", "TCS", "INFY", "HCLTECH", "LTM",
              "LATENTVIEW", "PERSISTENT", "HAPPSTMNDS", "INTELLECT", "COFORGE"]
BENCHMARKS = {"NIFTY50": "^NSEI", "NIFTYIT": "^CNXIT", "SMALLCAP250": "NIFTYSMLCAP250.NS"}
GLOBAL = {"GLOBALAI": "AIQ"}             # Global X Artificial Intelligence & Technology ETF (US, in USD)
FX = "INR=X"                              # US dollar in rupees
START = "2024-06-01"
OUT = Path("data/raw/prices")


def keep_old(new, name):
    """Fill gaps in today's download from the last good file, so one failed ticker never wipes its history."""
    path = OUT / name
    if path.exists():
        old = pd.read_csv(path, index_col=0, parse_dates=True)
        new = new.combine_first(old)          # today's values win; anything missing comes from before
    new.to_csv(path)
    return new


def main():
    import yfinance as yf                    # imported here so other scripts can read the lists without it
    OUT.mkdir(parents=True, exist_ok=True)
    tickers = {s: s + ".NS" for s in CANDIDATES}
    tickers.update(BENCHMARKS)
    data = yf.download(list(tickers.values()), start=START,
                       auto_adjust=False, progress=False)
    names = {v: k for k, v in tickers.items()}
    close = data["Close"].rename(columns=names)
    adj = data["Adj Close"].rename(columns=names)
    vol = data["Volume"].rename(columns=names)                       # shares traded on NSE each day

    # Yahoo sometimes returns nothing for one ticker in a batch: try those once more on their own
    for name, t in tickers.items():
        if name in close and close[name].notna().any():
            continue
        try:
            one = yf.download(t, start=START, auto_adjust=False, progress=False)
            if isinstance(one.columns, pd.MultiIndex):
                one.columns = one.columns.get_level_values(0)
            if not one.empty:
                close[name], adj[name], vol[name] = one["Close"], one["Adj Close"], one["Volume"]
                print(f"  retry worked for {name}")
        except Exception as e:
            print(f"  retry failed for {name}: {e}")

    close = keep_old(close, "close.csv")
    adj = keep_old(adj, "adj_close.csv")
    keep_old(vol, "volume.csv")

    print(f"Saved {len(close)} days, {close.index.min().date()} to {close.index.max().date()}")
    for name in tickers:
        n = close[name].notna().sum() if name in close else 0
        flag = "  <-- NO DATA, check ticker" if n == 0 else ""
        print(f"{name:12s} {n:4d} days{flag}")

    # Global benchmarks are saved separately: US trading days differ from Indian ones,
    # and mixing them into close.csv would add fake BAIX days on Indian holidays.
    try:
        g = yf.download(list(GLOBAL.values()) + [FX], start=START, auto_adjust=False, progress=False)["Close"]
        g = g.rename(columns={v: k for k, v in GLOBAL.items()}).rename(columns={FX: "USDINR"}).ffill()
        for k in GLOBAL:
            g[k + "_INR"] = g[k] * g["USDINR"]
        g.dropna(how="all").to_csv(OUT / "global.csv")
        print(f"Global: saved {len(g)} days to {(OUT / 'global.csv')}")
    except Exception as e:                # never let a global hiccup stop the Indian index update
        print(f"  WARNING: global download failed ({e}) - kept the previous global.csv")


if __name__ == "__main__":
    main()
