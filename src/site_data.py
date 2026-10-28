"""BAIX - export index data as JSON for the website (docs/data/baix.json)."""
import json
from pathlib import Path
import pandas as pd

MODE = "TEST"                                   # becomes "LIVE" at launch
LEVELS = "data/processed/baix_TEST.csv"
WEIGHTS = "data/processed/weights_DRAFT.csv"
OUT = Path("docs/data/baix.json")

NAMES = {"E2E": "E2E Networks", "NETWEB": "Netweb Technologies", "FRACTAL": "Fractal Analytics",
         "LATENTVIEW": "LatentView Analytics", "TCS": "Tata Consultancy Services",
         "INFY": "Infosys", "LTM": "LTM (formerly LTIMindtree)"}


def main():
    lv = pd.read_csv(LEVELS, parse_dates=["date"]).dropna(axis=1, how="all")
    series = [c for c in lv.columns if c != "date"]          # BAIX + whichever benchmarks have data
    lv[series] = lv[series].ffill()
    w = pd.read_csv(WEIGHTS)
    last, prev = lv.iloc[-1], lv.iloc[-2]
    data = {
        "mode": MODE,
        "base_date": lv.date.iloc[0].strftime("%Y-%m-%d"),
        "as_of": last.date.strftime("%Y-%m-%d"),
        "level": round(float(last.BAIX), 2),
        "level_tr": round(float(last.BAIX_TR), 2) if "BAIX_TR" in lv else None,
        "day_change_pct": round(float(last.BAIX / prev.BAIX - 1) * 100, 2),
        "since_base_pct": {c: round(float(last[c] / 1000 - 1) * 100, 2)
                           for c in series},
        "series": {
            "dates": lv.date.dt.strftime("%Y-%m-%d").tolist(),
            **{c: lv[c].round(2).tolist() for c in series},
        },
        "constituents": [
            {"symbol": r.symbol, "name": NAMES.get(r.symbol, r.symbol), "tier": r.tier,
             "ai_score": r.ai_score, "weight_pct": round(r.weight * 100, 2)}
            for r in w.itertuples()
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1))
    print(f"Wrote {OUT}: BAIX {data['level']} on {data['as_of']} ({MODE}), "
          f"{len(data['constituents'])} constituents, {len(lv)} days")


if __name__ == "__main__":
    main()
