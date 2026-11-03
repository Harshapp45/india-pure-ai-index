"""BAIX - share counts. Official figures from company filings override Yahoo's."""
from pathlib import Path
import pandas as pd

YAHOO = "data/raw/shares_yahoo.csv"
OFFICIAL = "data/raw/shares_official.csv"


def load_shares():
    """Shares outstanding by symbol: the official file wins, Yahoo fills the rest."""
    sh = pd.read_csv(YAHOO).set_index("symbol")["shares_outstanding"].astype(float)
    if Path(OFFICIAL).exists():
        off = pd.read_csv(OFFICIAL).set_index("symbol")["shares_outstanding"].astype(float)
        sh = off.combine_first(sh)
    return sh
