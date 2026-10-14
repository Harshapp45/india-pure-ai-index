"""BAIX - download daily closing prices for candidates and benchmarks."""
from pathlib import Path
import yfinance as yf

CANDIDATES = ["NETWEB", "E2E", "FRACTAL", "TCS", "INFY", "HCLTECH", "LTM",
              "LATENTVIEW", "PERSISTENT", "HAPPSTMNDS", "INTELLECT", "COFORGE"]
BENCHMARKS = {"NIFTY50": "^NSEI", "NIFTYIT": "^CNXIT"}
START = "2024-06-01"
OUT = Path("data/raw/prices")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tickers = {s: s + ".NS" for s in CANDIDATES}
    tickers.update(BENCHMARKS)
    data = yf.download(list(tickers.values()), start=START,
                       auto_adjust=False, progress=False)
    names = {v: k for k, v in tickers.items()}
    close = data["Close"].rename(columns=names)
    adj = data["Adj Close"].rename(columns=names)
    close.to_csv(OUT / "close.csv")
    adj.to_csv(OUT / "adj_close.csv")

    print(f"Saved {len(close)} days, {close.index.min().date()} to {close.index.max().date()}")
    for name in tickers:
        n = close[name].notna().sum() if name in close else 0
        flag = "  <-- NO DATA, check ticker" if n == 0 else ""
        print(f"{name:12s} {n:4d} days{flag}")


if __name__ == "__main__":
    main()
