# Bharat AI Index (BAIX): Index Methodology

**Version 1.2 (draft) · October 2026**
Author: Harsha Patyal · Repository: github.com/Harshapp45/india-pure-ai-index

> For research and educational purposes only. Not investment advice. The index is not affiliated with NSE, BSE or any index provider.

---

## 1. Objective

The **Bharat AI Index (BAIX)** tracks Indian listed companies that **earn revenue from artificial intelligence**: AI compute, AI systems, AI software and AI services.

It deliberately **excludes** companies that benefit from AI only indirectly, such as power equipment, cables, metals, telecom towers and data-centre real estate. Those "picks and shovels" sectors are already covered by broader AI-ecosystem benchmarks such as the Nifty AI Catalysts Index, which applies no AI-revenue test.

## 2. Index family

| Index | Code | Description |
|---|---|---|
| Bharat AI Index | **BAIX** | Headline index (price return) |
| Bharat AI Total Return Index | **BAIX TR** | BAIX with dividends reinvested |

*v1.0 proposed two separate indices (BAIX and BAIX-E). Research showed the eligible universe was too small to support two indices, so v1.1 merges them into one index with two tiers (Section 7).*

## 3. Launch, base date and history

- **Base date and value:** **13 November 2026 = 1,000** (closing level).
- **First live trading day:** **16 November 2026**.
- **Why this date:** under SEBI LODR Regulation 33, listed companies must publish quarterly results within 45 days of quarter end. The deadline for July–September (H1 FY27) results is **14 November 2026** (a Saturday), so 13 November is the last trading day before it. It is the earliest date on which every eligible company's half-year results are guaranteed to be public, giving the launch composition a complete and current information set.
- **No notice period at launch:** notice periods exist so funds tracking an index can prepare. At launch no fund tracks BAIX, so the inaugural composition is published with the launch.
- **Why not earlier:** screening showed that before late 2025, almost no Indian listed company reported AI revenue. At every review from June 2024 to June 2026, only 1–2 companies met the pure-tier rules, and that count rests partly on an estimate. A point-in-time backtest over that period would not be a meaningful index. The 2024–2026 period is published instead as a **research section** (universe growth), not as performance history.
- **Comparison:** from launch, BAIX is compared with Nifty 50, Nifty IT and Nifty AI Catalysts, each rebased to 1,000 on the BAIX base date.

## 4. Eligible universe (screening funnel)

At each review:

1. **Listing:** equity shares (EQ series) on the **NSE mainboard**. SME-platform stocks, ETFs, REITs and InvITs are excluded.
2. **Size and liquidity:** free-float market capitalisation ≥ **₹1,000 crore** and average daily traded value ≥ **₹5 crore**, both measured over the 6 months to the cut-off date.
   - *v1.1 implementation note:* membership of the **Nifty Total Market Index** is used as a practical proxy for this filter. This is a known approximation, to be replaced by direct calculation.
3. **Listing history:** at least **6 months** at the cut-off date.
4. **Industry:** NSE industry classification of **Information Technology** or **Telecommunication**.
   - *Known limitation:* companies in other sectors are not screened. This rule is reviewed annually in case AI businesses emerge elsewhere (for example semiconductors under Capital Goods).
5. **AI revenue evidence:** the company must have AI revenue evidence under Section 5.

Funnel counts are published at every review. The October 2026 screen ran 2,620 → 2,351 → 755 → 52 → 12.

## 5. AI exposure score

### 5.1 AI share buckets

| AI share of revenue | AI score |
|---|---|
| ≥ 50% | **1.00** |
| 20% to < 50% | **0.50** |
| 5% to < 20% | **0.25** |
| < 5% | **0** (not eligible) |

### 5.2 Evidence hierarchy

1. **Reported:** the company discloses an AI segment or an AI share of revenue.
2. **Derived:** the company discloses AI revenue as an amount (actual or annualised run-rate), which is divided by total revenue for the matching period.
3. **Estimated:** no disclosure. The share is estimated from annual reports, investor presentations and earnings-call transcripts.

### 5.3 What counts as AI revenue

- **Counts:** revenue the company itself labels as AI. This means selling AI services, AI platforms, AI systems or AI compute.
- **Does not count:**
  - revenue from products that are merely **powered by** AI (for example AI-targeted advertising or AI-featured loyalty software)
  - **deal wins, order book, pipeline or TCV** shares (these are future contracts, not revenue)
  - **workforce metrics** (for example "% of employees AI-certified")
  - **AI patents**, partnerships, awards or qualitative statements
- **Bundled labels** that combine AI with non-AI work (for example "AI-led engineering, data and cloud services") are treated as **Estimated**, not Reported.

### 5.4 Conservative rule (protection against "AI-washing")

Where the AI share is **Estimated**, the company is placed **one bucket lower** than the estimate suggests.

### 5.5 Point-in-time rule

At each review, only information **published on or before the cut-off date** is used. The **disclosure date** matters as well as the number: a figure for an earlier period that was first published after the cut-off cannot be used.

Every score is recorded with its evidence level, source, publish date and notes in the AI scores worksheet.

## 6. Constituent selection

- **New entrant:** AI score ≥ **0.25** (AI share ≥ 5% after the conservative rule) and passes Section 4.
- **Existing constituent stays if** (buffer rule):
  - **Pure tier:** reported or derived AI share ≥ **15%**, and free-float market cap ≥ **₹750 crore**.
  - **Broad tier:** reported or derived AI share ≥ **4%**, and free-float market cap ≥ **₹750 crore**.
- **Minimum constituents:** the index targets at least **5** constituents. If fewer qualify, the index is still calculated, the single-stock cap is relaxed to 100% ÷ N (Section 7.3), and the shortfall is disclosed in the review announcement.

## 7. Weighting: two tiers with fixed budgets

### 7.1 Tiers

| Tier | Rule | Target budget |
|---|---|---|
| **Pure tier** | AI score ≥ 0.50 (AI share ≥ 20%) | **75%** of the index |
| **Broad tier** | AI score = 0.25 (AI share 5–20%) | **25%** of the index |

The tier budget stops very large, partly-AI companies (for example large IT services firms) from dominating companies whose business is mainly AI.

### 7.2 Weights within each tier

Within each tier, raw weight = free-float market cap × AI score. Weights are then scaled to the tier's budget.

### 7.3 Caps and budget adjustment

- **Single-stock cap:** **20%** of the index.
- **Budget adjustment:** a tier cannot hold more than 20% × (number of stocks in the tier). If the pure tier's capacity is below 75%, its budget shrinks to its capacity and the difference moves to the broad tier, and vice versa.
- **If a tier is empty,** the other tier receives 100%.
- **If total capacity is below 100%** (fewer than 5 stocks in total), the cap is raised to 100% ÷ N.
- Excess weight above a cap is redistributed within the same tier, in proportion to weight. This is repeated until no constituent exceeds the cap.

## 8. Review schedule

- **Frequency:** semi-annual. Both reconstitution and rebalancing happen at the same review.
- **Effective date:** after the close of the **last trading day of June and December**.
- **Cut-off date:** anchored to SEBI results-disclosure deadlines, not to the calendar month:
  - **June review:** **30 May**, the deadline for annual audited results (60 days after the financial year end)
  - **December review:** **14 November**, the deadline for July–September results (45 days after quarter end)
  - If the deadline is not a trading day, the previous trading day is used.
- **First regular review:** **June 2027**. The December 2026 review is not held, because the launch composition already uses the same information set (14 November 2026).
- **Announcement:** at least **two weeks** before the effective date.
- **Weight drift:** between reviews, weights move with prices and may exceed the caps or budgets. This is an accepted trade-off for lower turnover.

## 9. Index calculation

```
Index level(t) = Σ [ Price(i,t) × Index shares(i) ] / Divisor(t)
```

- **Index shares** are fixed at each review so that each constituent's value matches its target weight.
- The **divisor** keeps the index level continuous across reviews and corporate actions.
- **BAIX TR:** cash dividends are reinvested across the index on the ex-dividend date.
- Closing prices are taken from the NSE.

## 10. Corporate actions and identifiers

| Event | Treatment |
|---|---|
| Stock split or bonus issue | Index shares are adjusted. No divisor change. |
| Rights issue | Price adjustment, with a divisor change. |
| Merger, acquisition or delisting | The stock is removed and its weight is redistributed within its tier. |
| Suspension or move to a restricted series | The stock is removed at the last traded price. |
| Special dividend | Price adjustment in BAIX. Reinvested in BAIX TR. |
| **Name or symbol change** | The index follows the **company**, not the ticker. Changes are logged in `data/raw/symbol_changes.csv` (for example LTIM → LTM, 17-Mar-2026). |

## 11. Data sources

- **Prices:** NSE daily bhavcopy (Yahoo Finance as a backup)
- **Universe and industry:** NSE equity list (EQUITY_L.csv) and the Nifty Total Market constituent list
- **AI share of revenue:** company press releases, investor presentations, annual reports and earnings-call transcripts. **Primary sources are preferred.** AI-generated summaries are never recorded as sources.

## 12. Known limitations

- **Very small universe.** Expect 4–7 constituents at launch.
- **Inconsistent AI revenue definitions.** TCS reports an annualised run-rate of AI embedded across its services; HCLTech reports only "Advanced AI"; Infosys reports a percentage. Scores are not perfectly comparable.
- **Estimates require judgement.** Notably E2E Networks, which does not split GPU (AI) cloud revenue from other cloud revenue.
- **Segment definitions change.** For example, Netweb's "AI systems and enterprise workstations" segment later became "AI Systems".
- **Size proxy and present-day screening list.** The universe screen used today's Nifty Total Market list rather than historical lists.

## 13. Version history

| Version | Date | Change |
|---|---|---|
| 1.0 (draft) | October 2026 | First version |
| 1.1 (draft) | October 2026 | Merged BAIX and BAIX-E into one tiered index (75% pure / 25% broad). Live launch moved to the December 2026 review. Added the AI revenue definition rules (5.3), the disclosure-date rule, the broad-tier buffer and the symbol-change handling. |
| 1.2 (draft) | October 2026 | Launch moved to base date 13-Nov-2026 (first live day 16-Nov-2026). Review cut-offs anchored to SEBI LODR results deadlines (30 May / 14 Nov). December 2026 review not held. |
