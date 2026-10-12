# Bharat AI Index (BAIX): Index Methodology

**Version 1.0 (draft) · October 2026**
Author: Harsha Patyal · Repository: github.com/Harshapp45/india-pure-ai-index

> For research and educational purposes only. Not investment advice. The index is not affiliated with NSE, BSE or any index provider.

---

## 1. Objective

The **Bharat AI Index (BAIX)** tracks Indian listed companies whose **own revenue** comes substantially from artificial intelligence: AI compute, AI systems, AI software and AI services.

It deliberately **excludes** companies that benefit from AI only indirectly, such as power equipment, cables, metals and telecom. Those "picks and shovels" sectors are already covered by broader AI-ecosystem benchmarks such as the Nifty AI Catalysts Index.

## 2. Index family

| Index | Code | Description |
|---|---|---|
| Bharat AI Index | **BAIX** | Headline pure-play index |
| Bharat AI Extended Index | **BAIX-E** | Broader version that also includes companies with a smaller AI share |
| Bharat AI Total Return Index | **BAIX TR** | BAIX with dividends reinvested |
| Bharat AI Extended Total Return Index | **BAIX-E TR** | BAIX-E with dividends reinvested |

The price return indices (BAIX and BAIX-E) are the headline figures.

## 3. Base date and base value

- **Base date:** 28 June 2024
- **Base value:** 1,000

The base date matches the Nifty AI Catalysts Index, which allows a like-for-like comparison.

## 4. Eligible universe

A stock is eligible at a review if it meets all of these conditions:

1. It is an equity share listed on the **NSE mainboard**. SME-platform stocks, ETFs, REITs and InvITs are excluded.
2. Its **free-float market capitalisation** is at least **₹1,000 crore**, measured as the 6-month average to the cut-off date.
3. Its **average daily traded value** is at least **₹5 crore**, measured over the 6 months to the cut-off date.
4. It has a **listing history** of at least **6 months** at the cut-off date.

## 5. AI exposure score

### 5.1 AI share buckets

Each eligible company is placed in a bucket based on the share of its revenue that comes from AI.

| AI share of revenue | AI score |
|---|---|
| ≥ 50%, or the company's entire business is AI (e.g. GPU cloud) | **1.00** |
| 20% to < 50% | **0.50** |
| 5% to < 20% | **0.25** |
| < 5% | **0** (not eligible) |

### 5.2 Evidence hierarchy

The AI share is determined using the best available evidence, in this order:

1. **Reported:** the company discloses an AI segment or an AI share of revenue. Also used where the company's entire business is AI, as described in its own filings.
2. **Derived:** the company discloses its AI revenue in absolute terms, and it is divided by total revenue.
3. **Estimated:** no disclosure exists. The share is estimated from annual reports, investor presentations and earnings-call transcripts.

### 5.3 Conservative rule (protection against "AI-washing")

Where the AI share is **estimated** (evidence level 3), the company is placed **one bucket lower** than the estimate suggests. A company estimated at 20–50% is treated as 5–20%.

### 5.4 Point-in-time rule

At each review, only information that was **publicly available on or before the cut-off date** is used. This prevents look-ahead bias in the backtest.

Every score is recorded with its evidence level and source in `data/processed/ai_scores.csv`.

## 6. Constituent selection

### 6.1 BAIX

- **New entrant:** AI share ≥ **20%** (score ≥ 0.50 after the conservative rule) **and** free-float market cap ≥ ₹1,000 crore.
- **Existing constituent stays if:** reported or derived AI share ≥ **15%** **and** free-float market cap ≥ **₹750 crore** (buffer rule).

### 6.2 BAIX-E

- All eligible companies with an AI score ≥ **0.25** (AI share ≥ 5%).
- **Existing constituent stays if:** free-float market cap ≥ ₹750 crore and it still meets the AI share requirement.

### 6.3 Minimum number of constituents

- BAIX must have at least **5** constituents. BAIX-E must have at least **10**.
- If fewer companies qualify, the index is topped up with the remaining eligible companies that have the **highest AI share**, until the minimum is reached.

## 7. Weighting

1. The **raw weight** of each constituent is its free-float market cap × AI score, divided by the sum of that product across all constituents.
2. **Capping:**
   - BAIX: no constituent may exceed **20%**.
   - BAIX-E: no constituent may exceed **10%**.
3. Any weight above the cap is removed and redistributed to the uncapped constituents in proportion to their weights. This is repeated until no constituent exceeds the cap.

## 8. Review schedule

- **Frequency:** semi-annual. Both reconstitution (which stocks are included) and rebalancing (resetting weights) happen at the same review.
- **Effective date:** after the close of the **last trading day of June and December**.
- **Cut-off date:** the last trading day of the month before (May and November).
- **Announcement:** at least **two weeks** before the effective date.
- **Weight drift:** between reviews, weights move with prices and may temporarily exceed the cap. This is an accepted trade-off for lower turnover.

## 9. Index calculation

The index is calculated using the standard free-float, market-capitalisation-weighted (Laspeyres-type) formula:

```
Index level(t) = Σ [ Price(i,t) × Index shares(i) ] / Divisor(t)
```

- **Index shares** are fixed at each review so that each constituent's value matches its target weight.
- The **divisor** is set so that the index equals 1,000 on the base date. It is adjusted at every review and corporate action, so the index level does not jump because of a change in composition.
- **Total return variants:** cash dividends are reinvested across the index on the ex-dividend date.
- Closing prices are taken from the NSE.

## 10. Corporate actions

Corporate actions are handled in line with standard NSE practice:

| Event | Treatment |
|---|---|
| Stock split or bonus issue | Index shares are adjusted. No divisor change. |
| Rights issue | Price adjustment, with a divisor change. |
| Merger, acquisition or delisting | The stock is removed and its weight is redistributed in proportion to the remaining constituents. If the count falls below the minimum, the index is topped up under Section 6.3. |
| Suspension or move to a restricted trading series | The stock is removed at the last traded price. |
| Special dividend | Price adjustment in the price return index. Reinvested in the total return index. |

## 11. Data sources

- **Prices:** NSE daily bhavcopy (Yahoo Finance as a backup)
- **Free float:** NSE shareholding pattern filings
- **AI share of revenue:** company annual reports, quarterly results, investor presentations and earnings-call transcripts

## 12. Known limitations

- **Small universe.** India has few listed pure-play AI companies, so BAIX is concentrated.
- **Inconsistent AI revenue definitions.** For example, TCS counts AI embedded across its services, while HCLTech counts only "Advanced AI". Scores are therefore not perfectly comparable.
- **Estimates require judgement.** The conservative rule limits but does not remove this.
- **Short history.** The backtest starts in June 2024.

## 13. Open items for v1.1

- AI share buffer for BAIX-E (staying threshold below 5%)
- Treatment of companies with both reported and estimated AI segments
- Whether to add a minimum trading-frequency rule

## 14. Version history

| Version | Date | Change |
|---|---|---|
| 1.0 (draft) | October 2026 | First version |
