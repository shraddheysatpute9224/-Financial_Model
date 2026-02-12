# StockPulse Data Extraction System — Complete Technical Blueprint

**Version:** 2.0
**Based On:** V2 Complete Data Requirements Specification (160 Fields)
**Platform:** StockPulse — Indian Stock Analysis Platform
**Purpose:** Implementation-ready system documentation for building a robust data extraction and web scraping system
**Last Updated:** 2026-02-12

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Data Source Mapping](#2-data-source-mapping)
3. [Extraction Strategy by Category](#3-extraction-strategy-by-category)
4. [Data Pipeline Architecture](#4-data-pipeline-architecture)
5. [Data Processing & Calculations](#5-data-processing--calculations)
6. [Reliability & Anti-Failure Mechanisms](#6-reliability--anti-failure-mechanisms)
7. [Storage & Structuring](#7-storage--structuring)
8. [Update & Scheduling Logic](#8-update--scheduling-logic)
9. [Quality Control Framework](#9-quality-control-framework)
10. [System Features](#10-system-features)
11. [Data Processing & Structuring](#11-data-processing--structuring)
12. [Data Storage & Organization](#12-data-storage--organization)
13. [Scalability & Future Expansion](#13-scalability--future-expansion)
14. [Features of the System](#14-features-of-the-system)

**Appendices:**
- [Appendix A: Complete 160-Field Reference](#appendix-a-complete-160-field-reference)
- [Appendix B: Primary Data Sources Summary](#appendix-b-primary-data-sources-summary)
- [Appendix C: Complete Calculation Formulas Reference](#appendix-c-complete-calculation-formulas-reference)
- [Appendix D: Validation Rules Quick Reference](#appendix-d-validation-rules-quick-reference)

---

## 1. System Overview

### 1.1 What We Are Building

The StockPulse Data Extraction System is a comprehensive, automated data pipeline designed to collect, process, validate, and store **all 160 data fields** required by the StockPulse Indian Stock Analysis Platform. The system ingests data from **8 primary sources** — including web scraping, file downloads, API calls, RSS feeds, and internal calculations — to produce a complete, structured, and reliable dataset for every tracked Indian stock.

### 1.2 Scope of Extraction

The system covers **13 categories** of data:

| # | Category | Fields | Primary Source | History | Update Frequency |
|---|----------|--------|---------------|---------|-----------------|
| 1 | Stock Master Data | 14 | NSE/BSE, Screener.in | N/A | On Change |
| 2 | Price & Volume (OHLCV) | 13 | NSE Bhavcopy | 10 Years | Daily |
| 3 | Derived Price Metrics | 11 | Calculated | 10 Years | Daily |
| 4 | Income Statement | 18 | Screener.in | 10 Years | Quarterly |
| 5 | Balance Sheet | 17 | Screener.in | 10 Years | Annual |
| 6 | Cash Flow Statement | 8 | Screener.in | 10 Years | Annual |
| 7 | Financial Ratios | 11 | Calculated | 10 Years | Quarterly |
| 8 | Valuation Metrics | 17 | Calculated | 10 Years | Daily |
| 9 | Shareholding Pattern | 10 | BSE Filings | 5–7 Years | Quarterly |
| 10 | Corporate Actions & Events | 10 | BSE/NSE | 10 Years | On Event |
| 11 | News & Sentiment | 8 | RSS Feeds | 30 Days | Real-time |
| 12 | Technical Indicators | 15 | pandas-ta (Calculated) | 10 Years | Daily |
| 13 | Qualitative & Metadata | 8 | Manual/System | Current | On Event |
| | **TOTAL** | **160** | | | |

**Priority Breakdown:**
- 🔴 CRITICAL: 58 fields — System cannot function without these
- 🟡 IMPORTANT: 52 fields — Significantly improves analysis quality
- 🟢 STANDARD: 35 fields — Enhances specific features and ML
- ⚪ OPTIONAL: 7 fields — Future advanced features
- 🔵 METADATA: 3 fields — System tracking for confidence scoring
- 💭 QUALITATIVE: 5 fields — Manual assessment or LLM-generated

### 1.3 Data Completeness Expectations

- **100% coverage** of all 160 defined fields must be attempted for every tracked stock
- **Critical fields (58):** Must achieve ≥99% fill rate across all tracked stocks
- **Important fields (52):** Must achieve ≥95% fill rate
- **Standard fields (35):** Must achieve ≥90% fill rate
- **Optional & Qualitative fields (12):** Best-effort; ≥70% fill rate target
- **Metadata fields (3):** 100% — these are system-generated and always available

### 1.4 Reliability Requirements

- **Uptime:** The extraction pipeline must run reliably on scheduled intervals without manual intervention
- **Fault Tolerance:** Failure in one data source or category must not block other categories
- **Data Freshness:** Daily-update fields must reflect trading day data by end of day; quarterly fields within 48 hours of filing
- **Accuracy:** Cross-verification between sources where possible; no stale data served without flagging
- **Recoverability:** All extraction jobs must be idempotent and re-runnable without duplicating data
- **Auditability:** Every extraction event must be logged with timestamp, source, status, and field count

---

## 2. Data Source Mapping

### 2.1 Primary Data Sources

| Source | Data Provided | Field Count | Cost | Method |
|--------|--------------|-------------|------|--------|
| **Screener.in** | All fundamentals, ratios, 10-year history, peer data | 60+ | Free / ₹4k/yr | Web Scraping |
| **NSE Bhavcopy** | Official EOD OHLCV, delivery data, bulk deals | 15 | Free | CSV Download |
| **BSE Filings** | Shareholding, corporate announcements, results | 15 | Free | Web Scraping / API |
| **Trendlyne** | FII/DII changes, pledging trends, forward PE | 8 | Free (limited) | Web Scraping |
| **yfinance** | Adjusted close, backup prices | 10 | Free | Python API |
| **RSS Feeds** | News from Moneycontrol, ET, BS | 4 | Free | RSS Parsing |
| **Rating Agencies** | Credit ratings (CRISIL, ICRA, CARE) | 3 | Free | Web Scraping |
| **pandas-ta** | All technical indicators (calculated) | 15 | Free (library) | Local Calculation |

### 2.2 Source-to-Category Mapping

#### Category 1: Stock Master Data (14 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| symbol | NSE/BSE | Scrape/Download | NSE equity list CSV |
| company_name | NSE/BSE | Scrape/Download | Screener.in |
| isin | NSE/BSE | Scrape/Download | BSE equity list |
| nse_code | NSE | Download (equity list) | Screener.in |
| bse_code | BSE | Download (equity list) | Screener.in |
| sector | Screener.in | Web Scrape | Trendlyne |
| industry | Screener.in | Web Scrape | Trendlyne |
| market_cap_category | Calculated | Internal (from market_cap) | — |
| listing_date | NSE/BSE | Download | Screener.in |
| face_value | NSE/BSE | Download | Screener.in |
| shares_outstanding | BSE Filings | Web Scrape | Screener.in |
| free_float_shares | BSE Filings | Web Scrape | Trendlyne |
| website | Screener.in | Web Scrape | BSE |
| registered_office | BSE | Web Scrape | Annual Report |

#### Category 2: Price & Volume Data (13 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| date | NSE Bhavcopy | CSV Download | yfinance |
| open | NSE Bhavcopy | CSV Download | yfinance |
| high | NSE Bhavcopy | CSV Download | yfinance |
| low | NSE Bhavcopy | CSV Download | yfinance |
| close | NSE Bhavcopy | CSV Download | yfinance |
| adjusted_close | yfinance | Python API | Calculated from corp actions |
| volume | NSE Bhavcopy | CSV Download | yfinance |
| delivery_volume | NSE Bhavcopy | CSV Download | NSE delivery data |
| delivery_percentage | NSE Bhavcopy | CSV Download | Calculated |
| turnover | NSE Bhavcopy | CSV Download | — |
| trades_count | NSE Bhavcopy | CSV Download | — |
| prev_close | NSE Bhavcopy | CSV Download | Calculated |
| vwap | NSE | Web Scrape / Download | Calculated |

#### Category 3: Derived Price Metrics (11 Fields)

All 11 fields are **internally calculated** from OHLCV data — no external source needed:
- daily_return_pct, return_5d_pct, return_20d_pct, return_60d_pct
- day_range_pct, gap_percentage
- 52_week_high, 52_week_low, distance_from_52w_high
- volume_ratio, avg_volume_20d

#### Category 4: Income Statement (18 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| revenue | Screener.in | Web Scrape | Trendlyne |
| revenue_growth_yoy | Calculated | Internal | — |
| revenue_growth_qoq | Calculated | Internal | — |
| operating_profit | Screener.in | Web Scrape | Trendlyne |
| operating_margin | Screener.in | Web Scrape | Calculated |
| gross_profit | Screener.in | Web Scrape | — |
| gross_margin | Calculated | Internal | — |
| net_profit | Screener.in | Web Scrape | Trendlyne |
| net_profit_margin | Calculated | Internal | — |
| eps | Screener.in | Web Scrape | Calculated |
| eps_growth_yoy | Calculated | Internal | — |
| interest_expense | Screener.in | Web Scrape | — |
| depreciation | Screener.in | Web Scrape | — |
| ebitda | Screener.in | Web Scrape | Calculated |
| ebit | Calculated | Internal | — |
| other_income | Screener.in | Web Scrape | — |
| tax_expense | Screener.in | Web Scrape | — |
| effective_tax_rate | Calculated | Internal | — |

#### Category 5: Balance Sheet (17 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| total_assets | Screener.in | Web Scrape | — |
| total_equity | Screener.in | Web Scrape | — |
| total_debt | Screener.in | Web Scrape | — |
| long_term_debt | Screener.in | Web Scrape | — |
| short_term_debt | Screener.in | Web Scrape | — |
| cash_and_equivalents | Screener.in | Web Scrape | — |
| net_debt | Calculated | Internal (total_debt − cash) | — |
| current_assets | Screener.in | Web Scrape | — |
| current_liabilities | Screener.in | Web Scrape | — |
| inventory | Screener.in | Web Scrape | — |
| receivables | Screener.in | Web Scrape | — |
| payables | Screener.in | Web Scrape | — |
| fixed_assets | Screener.in | Web Scrape | — |
| intangible_assets | Screener.in | Web Scrape | — |
| reserves_and_surplus | Screener.in | Web Scrape | — |
| book_value_per_share | Screener.in | Web Scrape | Calculated |
| contingent_liabilities | Annual Report | Web Scrape | Screener.in |

#### Category 6: Cash Flow Statement (8 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| operating_cash_flow | Screener.in | Web Scrape | — |
| investing_cash_flow | Screener.in | Web Scrape | — |
| financing_cash_flow | Screener.in | Web Scrape | — |
| capital_expenditure | Screener.in | Web Scrape | — |
| free_cash_flow | Calculated | OCF − CapEx | — |
| dividends_paid | Screener.in | Web Scrape | — |
| debt_repayment | Screener.in | Web Scrape | — |
| equity_raised | Screener.in | Web Scrape | — |

#### Category 7: Financial Ratios (11 Fields)

All 11 fields are **calculated** from financial statement data:
- roe, roa, roic, debt_to_equity, interest_coverage
- current_ratio, quick_ratio, asset_turnover
- inventory_turnover, receivables_turnover, dividend_payout_ratio

#### Category 8: Valuation Metrics (17 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| market_cap | Calculated | Price × Shares Outstanding | Screener.in |
| enterprise_value | Calculated | Market Cap + Net Debt | — |
| pe_ratio | Calculated | Price / EPS (TTM) | Screener.in |
| pe_ratio_forward | Trendlyne | Web Scrape | — |
| peg_ratio | Calculated | P/E / EPS Growth Rate | — |
| pb_ratio | Calculated | Price / Book Value/Share | — |
| ps_ratio | Calculated | Price / Revenue/Share | — |
| ev_to_ebitda | Calculated | EV / EBITDA | — |
| ev_to_sales | Calculated | EV / Revenue | — |
| dividend_yield | Calculated | Annual Div / Price × 100 | Screener.in |
| fcf_yield | Calculated | FCF/Share / Price × 100 | — |
| earnings_yield | Calculated | EPS / Price × 100 | — |
| sector_avg_pe | Screener.in | Web Scrape | Trendlyne |
| sector_avg_roe | Screener.in | Web Scrape | Trendlyne |
| industry_avg_pe | Screener.in | Web Scrape | — |
| historical_pe_median | Calculated | Median P/E over 5 years | — |
| sector_performance | NSE Indices | Download / Scrape | — |

#### Category 9: Shareholding Pattern (10 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| promoter_holding | BSE Filings | Web Scrape | Trendlyne |
| promoter_pledging | BSE/Trendlyne | Web Scrape | — |
| fii_holding | BSE Filings | Web Scrape | Trendlyne |
| dii_holding | BSE Filings | Web Scrape | Trendlyne |
| public_holding | BSE Filings | Web Scrape | — |
| promoter_holding_change | Calculated | Quarter-over-quarter diff | — |
| fii_holding_change | Calculated | Quarter-over-quarter diff | — |
| num_shareholders | BSE Filings | Web Scrape | — |
| mf_holding | BSE Filings | Web Scrape | Trendlyne |
| insurance_holding | BSE Filings | Web Scrape | — |

#### Category 10: Corporate Actions & Events (10 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| dividend_per_share | BSE/NSE | Web Scrape | Screener.in |
| ex_dividend_date | BSE/NSE | Web Scrape | — |
| stock_split_ratio | BSE/NSE | Web Scrape | — |
| bonus_ratio | BSE/NSE | Web Scrape | — |
| rights_issue_ratio | BSE/NSE | Web Scrape | — |
| buyback_details | BSE/NSE | Web Scrape | — |
| next_earnings_date | BSE Announcements | Web Scrape | Trendlyne |
| pending_events | BSE Announcements | Web Scrape | — |
| stock_status | NSE/BSE | Scrape / Download | — |
| sebi_investigation | SEBI/News | Web Scrape / RSS | — |

#### Category 11: News & Sentiment (8 Fields)

| Field | Source | Method | Backup Source |
|-------|--------|--------|---------------|
| news_headline | RSS Feeds | RSS Parsing | — |
| news_body_text | RSS Feeds → linked URL | HTTP Fetch + Parse | — |
| news_source | RSS Feeds | RSS Parsing | — |
| news_timestamp | RSS Feeds | RSS Parsing | — |
| news_sentiment_score | Calculated | NLP / LLM Analysis | — |
| stock_tickers_mentioned | Calculated | NLP Entity Extraction | — |
| credit_rating | Rating Agencies (CRISIL, ICRA, CARE) | Web Scrape | News |
| credit_outlook | Rating Agencies | Web Scrape | News |

#### Category 12: Technical Indicators (15 Fields)

All 15 fields are **calculated** using pandas-ta from OHLCV data:
- sma_20, sma_50, sma_200, ema_12, ema_26
- rsi_14, macd, macd_signal
- bollinger_upper, bollinger_lower, atr_14, adx_14, obv
- support_level (custom pivot low), resistance_level (custom pivot high)

#### Category 13: Qualitative & Metadata (8 Fields)

| Field | Source | Method |
|-------|--------|--------|
| moat_assessment | Manual / LLM | User input or LLM inference |
| management_assessment | Manual / LLM | User input or LLM inference |
| industry_growth_assessment | Manual / LLM | User input or LLM inference |
| disruption_risk | Manual / LLM | User input or LLM inference |
| fraud_history | Manual / News | Manual flag or news mining |
| field_availability | System | Auto-generated tracking dict |
| field_last_updated | System | Auto-generated timestamp dict |
| multi_source_values | System | Auto-generated cross-source dict |

### 2.3 Multi-Source Validation Matrix

Fields available from multiple sources for cross-verification:

| Field | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| close price | NSE Bhavcopy | yfinance | BSE |
| market_cap | Calculated | Screener.in | — |
| pe_ratio | Calculated | Screener.in | Trendlyne |
| promoter_holding | BSE Filings | Trendlyne | Screener.in |
| eps | Screener.in | Calculated | Trendlyne |
| net_profit | Screener.in | BSE Results | Trendlyne |
| dividend_yield | Calculated | Screener.in | Trendlyne |
| sector/industry | Screener.in | Trendlyne | BSE |

---

## 3. Extraction Strategy by Category

### 3.1 Category 1: Stock Master Data (14 Fields)

**Extraction Method:** A combination of CSV downloads (NSE/BSE equity lists) and web scraping (Screener.in).

**Approach:**
- **NSE Equity List Download:** NSE publishes a CSV file listing all actively traded equities. Download this file to extract `symbol`, `company_name`, `isin`, `nse_code`, `listing_date`, and `face_value`.
- **BSE Equity List Download:** BSE provides a similar equity list for `bse_code` and cross-verification of ISIN.
- **Screener.in Scraping:** For each stock's company page, scrape `sector`, `industry`, `website`, `shares_outstanding`, and `free_float_shares` from the company overview section.
- **BSE Filings:** Extract `shares_outstanding` and `free_float_shares` from quarterly shareholding filings as the authoritative source.
- **Calculated Field:** `market_cap_category` is derived from `market_cap` using thresholds (Large Cap ≥ ₹20,000 Cr; Mid Cap ₹5,000–20,000 Cr; Small Cap < ₹5,000 Cr).

**Frequency:** On change (effectively checked weekly; NSE/BSE lists checked daily for new listings or delistings).

**Historical Depth:** Not applicable — this is reference data representing the current state.

**Edge Cases:**
- Stocks listed on only one exchange (NSE or BSE but not both)
- Symbol changes (e.g., company name changes post-merger)
- Demerged entities needing new master records
- Suspended stocks still requiring master data retention

---

### 3.2 Category 2: Price & Volume Data (13 Fields)

**Extraction Method:** Primary — NSE Bhavcopy CSV download; Secondary — yfinance Python API.

**Approach:**
- **NSE Bhavcopy:** NSE publishes a daily Bhavcopy file (CSV/ZIP) after market close. Download and parse this file to extract `date`, `open`, `high`, `low`, `close`, `volume`, `delivery_volume`, `delivery_percentage`, `turnover`, `trades_count`, `prev_close`, and `vwap` for each stock.
- **yfinance API:** Use the yfinance Python library to fetch `adjusted_close` (which accounts for splits, bonuses, and dividends). Also use yfinance as a backup source for all OHLCV data if Bhavcopy download fails.
- **Historical Backfill:** For 10-year history, batch-download historical Bhavcopy archives from NSE data archives (available as monthly ZIP files). Use yfinance for adjusted_close history.

**Frequency:** Daily — triggered after NSE market close (approximately 15:45 IST, with download available by 18:00–19:00 IST).

**Historical Depth:** 10 years of trading data (~2,500 trading days per stock).

**Edge Cases:**
- Market holidays — no Bhavcopy generated; system must skip gracefully
- Stock trading suspensions — may have missing days; record as gap, not error
- Corporate action days (ex-dividend, split) — raw price discontinuities expected; adjusted_close handles this
- Bhavcopy format changes by NSE — parser must be resilient
- Delivery data may be absent for some stocks on some days

---

### 3.3 Category 3: Derived Price Metrics (11 Fields)

**Extraction Method:** 100% internally calculated from OHLCV data (Category 2). No external source needed.

**Approach:**
- All 11 fields are computed after daily OHLCV ingestion completes
- **daily_return_pct:** `((close - prev_close) / prev_close) × 100`
- **return_5d_pct / return_20d_pct / return_60d_pct:** Rolling lookback returns using close prices from 5, 20, and 60 trading days ago
- **day_range_pct:** `((high - low) / low) × 100`
- **gap_percentage:** `((open - prev_close) / prev_close) × 100`
- **52_week_high / 52_week_low:** Rolling MAX(high) and MIN(low) over 252 trading days
- **distance_from_52w_high:** `((52w_high - close) / 52w_high) × 100`
- **volume_ratio:** `volume / avg_volume_20d`
- **avg_volume_20d:** Simple 20-day moving average of volume

**Frequency:** Daily — calculated immediately after Category 2 data ingestion.

**Historical Depth:** 10 years (calculated retroactively for backfill).

**Edge Cases:**
- Insufficient history for a newly listed stock (e.g., < 252 days for 52-week calculations) — use available data and flag as incomplete
- Zero-volume days (trading halts) — exclude from average calculations
- Stock splits creating price discontinuities — use adjusted_close for return calculations

---

### 3.4 Category 4: Income Statement (18 Fields)

**Extraction Method:** Web scraping from Screener.in quarterly and annual profit & loss pages.

**Approach:**
- **Screener.in Scraping:** Navigate to each stock's page on Screener.in (e.g., `screener.in/company/RELIANCE/`). Scrape the quarterly results table and annual P&L table for: `revenue`, `operating_profit`, `operating_margin`, `gross_profit`, `net_profit`, `eps`, `interest_expense`, `depreciation`, `ebitda`, `other_income`, `tax_expense`.
- **Calculated Fields:** From scraped data, compute: `revenue_growth_yoy`, `revenue_growth_qoq`, `gross_margin`, `net_profit_margin`, `eps_growth_yoy`, `ebit` (operating_profit − depreciation + depreciation = operating_profit, or derived as EBITDA − depreciation), `effective_tax_rate` (tax_expense / pre-tax profit × 100).

**Frequency:** Quarterly — triggered when new quarterly results are published (typically within 45 days of quarter end). Run daily checks during results season (Jan, Apr, Jul, Oct).

**Historical Depth:** 10 years of quarterly data (~40 quarters) and annual data.

**Edge Cases:**
- Banking/financial companies have different P&L structures (NII instead of revenue, no COGS)
- Exceptional items may distort single-quarter numbers
- Restated financials — use the latest available restated figures
- Some companies report consolidated vs standalone — prefer consolidated; track both if available

---

### 3.5 Category 5: Balance Sheet (17 Fields)

**Extraction Method:** Web scraping from Screener.in annual balance sheet pages.

**Approach:**
- **Screener.in Scraping:** Scrape the balance sheet table on each stock's page for: `total_assets`, `total_equity`, `total_debt`, `long_term_debt`, `short_term_debt`, `cash_and_equivalents`, `current_assets`, `current_liabilities`, `inventory`, `receivables`, `payables`, `fixed_assets`, `intangible_assets`, `reserves_and_surplus`, `book_value_per_share`.
- **Calculated Fields:** `net_debt` = `total_debt` − `cash_and_equivalents`.
- **Annual Reports:** `contingent_liabilities` may not always be on Screener.in; attempt to extract from BSE-filed annual reports or notes to accounts.

**Frequency:** Annually — primary update after annual results filing. Some fields (total_debt, cash_and_equivalents) updated quarterly if available.

**Historical Depth:** 10 years of annual data.

**Edge Cases:**
- Banking companies have fundamentally different balance sheets (no inventory, different asset classes)
- Merged/demerged entities may have discontinuous historical data
- Screener.in may show both standalone and consolidated — prefer consolidated
- `contingent_liabilities` may require parsing notes, not always in structured tables

---

### 3.6 Category 6: Cash Flow Statement (8 Fields)

**Extraction Method:** Web scraping from Screener.in annual cash flow pages.

**Approach:**
- **Screener.in Scraping:** Scrape cash flow table for: `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow`, `capital_expenditure`, `dividends_paid`, `debt_repayment`, `equity_raised`.
- **Calculated Field:** `free_cash_flow` = `operating_cash_flow` − `capital_expenditure`.

**Frequency:** Annually — updated after annual results filing.

**Historical Depth:** 10 years of annual data.

**Edge Cases:**
- CapEx may be reported as negative in investing cash flow — ensure sign convention is consistent (store as positive value)
- Some companies may not separately report debt_repayment and equity_raised in summary tables

---

### 3.7 Category 7: Financial Ratios (11 Fields)

**Extraction Method:** 100% internally calculated from Income Statement (Cat 4), Balance Sheet (Cat 5), and Cash Flow (Cat 6) data.

**Approach (with formulas):**
- **roe:** `Net Profit / Total Equity × 100`
- **roa:** `Net Profit / Total Assets × 100`
- **roic:** `NOPAT / Invested Capital × 100` (where NOPAT = Operating Profit × (1 − Tax Rate); Invested Capital = Total Equity + Total Debt − Cash)
- **debt_to_equity:** `Total Debt / Total Equity`
- **interest_coverage:** `EBIT / Interest Expense`
- **current_ratio:** `Current Assets / Current Liabilities`
- **quick_ratio:** `(Current Assets − Inventory) / Current Liabilities`
- **asset_turnover:** `Revenue / Total Assets`
- **inventory_turnover:** `COGS / Average Inventory` (COGS = Revenue − Gross Profit)
- **receivables_turnover:** `Revenue / Average Receivables`
- **dividend_payout_ratio:** `Dividends Paid / Net Profit × 100`

**Frequency:** Quarterly for roe, debt_to_equity, interest_coverage; Annually for remaining ratios.

**Historical Depth:** 10 years.

**Edge Cases:**
- Division by zero (zero equity, zero interest expense) — output as null with metadata flag
- Negative equity companies — D/E ratio becomes negative; flag as high risk
- Companies with zero inventory — inventory_turnover is not applicable; mark as N/A

---

### 3.8 Category 8: Valuation Metrics (17 Fields)

**Extraction Method:** Primarily calculated; with `pe_ratio_forward` scraped from Trendlyne and peer averages from Screener.in.

**Approach:**
- **Calculated fields** (13 of 17): `market_cap`, `enterprise_value`, `pe_ratio`, `peg_ratio`, `pb_ratio`, `ps_ratio`, `ev_to_ebitda`, `ev_to_sales`, `dividend_yield`, `fcf_yield`, `earnings_yield`, `historical_pe_median`.
- **Scraped fields:**
  - `pe_ratio_forward`: Scrape from Trendlyne's consensus estimates page
  - `sector_avg_pe`, `sector_avg_roe`, `industry_avg_pe`: Scrape from Screener.in peer comparison tables
  - `sector_performance`: Download NSE sector index data

**Frequency:** Daily for price-dependent metrics (market_cap, pe_ratio, pb_ratio, ps_ratio, dividend_yield, earnings_yield); Quarterly for earnings-dependent metrics (peg_ratio, ev_to_ebitda); Weekly for peer averages.

**Historical Depth:** 10 years for most; 3 years for forward PE and peer averages; 1 year for sector_performance.

**Edge Cases:**
- Negative earnings make P/E meaningless — store as null with flag
- Companies with no dividends — dividend_yield = 0 (not null)
- EPS growth = 0 makes PEG undefined — handle with null and flag
- Very high P/E (>200) may indicate anomalous earnings — flag for review

---

### 3.9 Category 9: Shareholding Pattern (10 Fields)

**Extraction Method:** Web scraping from BSE filings (XBRL/HTML shareholding pattern filings); backup from Trendlyne.

**Approach:**
- **BSE Filings Scraping:** Navigate to BSE's corporate filings section for each company. Download or scrape quarterly shareholding pattern filings (Regulation 31). Extract: `promoter_holding`, `promoter_pledging`, `fii_holding`, `dii_holding`, `public_holding`, `num_shareholders`, `mf_holding`, `insurance_holding`.
- **Trendlyne Backup:** Use Trendlyne's shareholding pages as a backup/verification source, especially for `promoter_pledging` trends.
- **Calculated Fields:** `promoter_holding_change` and `fii_holding_change` — compute quarter-over-quarter differences from historical data.

**Frequency:** Quarterly — filings due within 21 days of quarter end.

**Historical Depth:** 5–7 years of quarterly data.

**Edge Cases:**
- Government companies may have "Government" instead of "Promoter" category
- Companies with zero promoter holding (widely held)
- XBRL format changes between filing periods
- Partial filings or delayed filings

---

### 3.10 Category 10: Corporate Actions & Events (10 Fields)

**Extraction Method:** Web scraping from BSE/NSE announcements pages and corporate actions databases.

**Approach:**
- **BSE Announcements Scraping:** Scrape BSE's announcement section filtered by company for: `dividend_per_share`, `ex_dividend_date`, `stock_split_ratio`, `bonus_ratio`, `rights_issue_ratio`, `buyback_details`, `next_earnings_date`, `pending_events`.
- **NSE Corporate Actions:** Download NSE's corporate actions page/CSV for cross-verification.
- **Stock Status:** Check NSE/BSE equity lists for trading status (`ACTIVE`, `SUSPENDED`, `DELISTED`) via `stock_status`.
- **SEBI Investigation:** Monitor SEBI orders page and financial news RSS feeds for `sebi_investigation` flags.

**Frequency:** On Event — continuous monitoring with daily sweep of announcement pages.

**Historical Depth:** 10 years for dividends, splits, bonuses; Current only for next_earnings_date, pending_events, stock_status, sebi_investigation.

**Edge Cases:**
- Multiple dividends in a year (interim + final)
- Complex corporate actions (demergers, scheme of arrangement)
- Pending corporate actions that get cancelled
- SEBI investigation status may not have a single definitive source

---

### 3.11 Category 11: News & Sentiment (8 Fields)

**Extraction Method:** RSS feed parsing, HTTP page fetching, NLP analysis, and web scraping of rating agencies.

**Approach:**
- **RSS Feed Parsing:** Subscribe to RSS feeds from Moneycontrol, Economic Times, Business Standard, LiveMint, and NDTV Profit. Parse feeds to extract: `news_headline`, `news_source`, `news_timestamp`.
- **Full Article Fetch:** Follow article URLs from RSS entries. Fetch the HTML page and parse the article body to extract `news_body_text`. Clean HTML tags, ads, and navigation elements to retain pure article text.
- **NLP/LLM Sentiment:** Run `news_body_text` through a sentiment analysis module (NLP model or LLM) to produce `news_sentiment_score` (range −1 to +1).
- **Entity Extraction:** Use NLP entity recognition or ticker-matching dictionaries to populate `stock_tickers_mentioned` for each article.
- **Credit Ratings:** Scrape rating agency websites (CRISIL, ICRA, CARE, India Ratings) for `credit_rating` and `credit_outlook`. Also monitor press releases and news for rating changes.

**Frequency:** Real-time for news (RSS polling every 5–15 minutes); On Change for credit ratings (daily check).

**Historical Depth:** 30 days of rolling news; Current for credit ratings.

**Edge Cases:**
- RSS feed downtime or format changes
- Paywalled articles — extract what is available from RSS summary
- Multi-stock articles needing correct ticker attribution
- Sentiment model errors on sarcasm or ambiguous language
- Rating agencies may not have a presence for all companies (primarily rated debt issuers)

---

### 3.12 Category 12: Technical Indicators (15 Fields)

**Extraction Method:** 100% calculated locally using the pandas-ta library from OHLCV data.

**Approach:**
- After daily OHLCV ingestion, compute all 15 indicators:
  - **Moving Averages:** `sma_20`, `sma_50`, `sma_200` (Simple Moving Averages); `ema_12`, `ema_26` (Exponential Moving Averages)
  - **Momentum:** `rsi_14` (Relative Strength Index, 14-period); `macd` (EMA12 − EMA26); `macd_signal` (EMA of MACD, 9-period)
  - **Volatility:** `bollinger_upper` (SMA20 + 2×StdDev); `bollinger_lower` (SMA20 − 2×StdDev); `atr_14` (Average True Range, 14-period)
  - **Trend/Volume:** `adx_14` (Average Directional Index, 14-period); `obv` (On Balance Volume)
  - **Support/Resistance:** `support_level` (pivot low calculation — custom implementation); `resistance_level` (pivot high calculation — custom implementation)

**Frequency:** Daily — calculated immediately after OHLCV and derived metrics.

**Historical Depth:** 10 years (1 year for support/resistance levels).

**Edge Cases:**
- Insufficient data for long-period indicators (e.g., SMA 200 needs 200 days)
- Newly listed stocks with limited history — calculate what is possible, flag as incomplete
- Extreme price moves may cause indicator saturation (RSI pegged at 0 or 100)

---

### 3.13 Category 13: Qualitative & Metadata (8 Fields)

**Extraction Method:** Manual input, LLM inference, and automatic system tracking.

**Approach:**
- **Qualitative Fields (5):**
  - `moat_assessment`, `management_assessment`, `industry_growth_assessment`, `disruption_risk`: Enum values (Strong/Moderate/Weak or High/Medium/Low) entered manually by analysts or generated by an LLM analyzing company reports and news.
  - `fraud_history`: Boolean flag set manually or triggered by news pattern detection (keywords: "fraud", "SEBI penalty", "accounting irregularity").

- **Metadata Fields (3) — All system-automated:**
  - `field_availability`: A dictionary tracking which of the 160 fields are populated for each stock. Auto-updated after every extraction cycle.
  - `field_last_updated`: A dictionary mapping each field name to its last-updated timestamp. Auto-updated on every write.
  - `multi_source_values`: For fields available from multiple sources, store all source values to enable agreement scoring (e.g., `{"pe_ratio": {"calculated": 25.3, "screener": 25.1, "trendlyne": 25.4}}`).

**Frequency:** On Event for qualitative fields; continuously updated for metadata.

**Historical Depth:** Current snapshot only.

**Edge Cases:**
- LLM-generated assessments may be inconsistent across runs — version and timestamp all assessments
- field_availability must gracefully handle newly added fields

---

## 4. Data Pipeline Architecture

### 4.1 High-Level System Architecture

The system follows a modular, layered architecture with five distinct layers:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                         │
│           Scheduler · Job Queue · Dependency Manager               │
├─────────────────────────────────────────────────────────────────────┤
│                        EXTRACTION LAYER                            │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────────┐   │
│  │ Screener  │ │    NSE    │ │    BSE    │ │ Trendlyne/yfinance│   │
│  │ Scraper   │ │ Bhavcopy  │ │  Filings  │ │  /RSS/Rating/SEBI │   │
│  │ Module    │ │ Downloader│ │  Scraper  │ │     Modules       │   │
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └────────┬──────────┘   │
│        │              │              │                │              │
├────────┴──────────────┴──────────────┴────────────────┴─────────────┤
│                     RAW DATA STAGING LAYER                          │
│                  Temporary storage for raw extracts                 │
├─────────────────────────────────────────────────────────────────────┤
│                     PROCESSING LAYER                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌───────────────────┐  │
│  │  Parser  │ │ Cleaner  │ │  Calculator  │ │    Validator      │  │
│  │  Engine  │ │ & Normalizer│ │  Engine     │ │    Engine         │  │
│  └────┬─────┘ └────┬─────┘ └──────┬───────┘ └────────┬──────────┘  │
│       │             │              │                   │             │
├───────┴─────────────┴──────────────┴───────────────────┴────────────┤
│                     STORAGE LAYER                                   │
│           Primary Database · Time-Series Store · File Archive       │
├─────────────────────────────────────────────────────────────────────┤
│                     MONITORING & QUALITY LAYER                      │
│        Logging · Alerting · Completeness Tracking · Metadata        │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Modular Design

Each extraction source is encapsulated as an independent module:

| Module | Sources Handled | Categories Covered |
|--------|----------------|-------------------|
| **Screener Module** | Screener.in | Cat 4, 5, 6 (partial 1, 8) |
| **Bhavcopy Module** | NSE Bhavcopy | Cat 2 |
| **BSE Module** | BSE Filings, BSE Announcements | Cat 9, 10 (partial 1) |
| **Trendlyne Module** | Trendlyne | Cat 8 (forward PE), Cat 9 (backup) |
| **yfinance Module** | yfinance API | Cat 2 (adjusted_close, backup) |
| **RSS Module** | Moneycontrol, ET, BS, LiveMint | Cat 11 (news) |
| **Rating Module** | CRISIL, ICRA, CARE, India Ratings | Cat 11 (credit) |
| **Calculation Engine** | Internal | Cat 3, 7, 8 (partial), 12 |
| **NLP/Sentiment Module** | Internal | Cat 11 (sentiment, entities) |
| **Metadata Module** | Internal | Cat 13 |

### 4.3 Data Flow

```
Source → Raw Extract → Staging → Parse → Clean → Validate → Store (Processed DB)
                                                    ↓
                                              Calculate Derived Fields
                                                    ↓
                                              Validate Calculations
                                                    ↓
                                              Store (Derived DB)
                                                    ↓
                                              Update Metadata
```

**Detailed flow for each extraction type:**

1. **Download-based (Bhavcopy, equity lists):** Download file → Store raw file in archive → Parse CSV → Clean & normalize → Validate values → Insert into database → Trigger derived calculations.

2. **Scrape-based (Screener, BSE, Trendlyne):** Build request → Fetch page HTML → Parse DOM/tables → Extract structured data → Clean & normalize → Validate → Insert into database.

3. **API-based (yfinance):** Call API → Receive structured response → Validate → Insert into database.

4. **RSS-based (News):** Poll RSS feed → Parse entries → Fetch full article → Clean text → Run NLP → Store article + sentiment.

5. **Calculation-based (Derived, Ratios, Technical):** Read dependency data from database → Apply formulas → Validate output ranges → Store results.

### 4.4 Separation of Data Types

| Data Type | Description | Storage |
|-----------|-------------|---------|
| **Raw Data** | Unprocessed files and HTML as received from sources | File archive (date-partitioned folders) |
| **Processed Data** | Parsed, cleaned, normalized data from external sources | Primary database tables |
| **Calculated Data** | Derived metrics, ratios, technical indicators | Separate database tables with dependency tracking |
| **Metadata** | field_availability, field_last_updated, multi_source_values | Metadata tables with per-stock tracking |

### 4.5 Incremental Update Handling

- **Daily OHLCV:** Append-only — each day adds new rows. Check for duplicates by (symbol, date) key.
- **Quarterly Financials:** Upsert by (symbol, period_end_date). If Screener.in updates restated figures, overwrite and log the change.
- **Shareholding:** Upsert by (symbol, quarter). Store the filing date to track late updates.
- **News:** Append-only with deduplication by (source, URL).
- **Calculated Fields:** Recalculate from dependencies whenever upstream data changes. For daily fields, recalculate the latest and preceding few days. For quarterly, recalculate the current period.

---

## 5. Data Processing & Calculations

### 5.1 Calculation Dependency Map

The following diagram shows how calculated fields depend on source data and each other:

```
OHLCV (Cat 2)
  ├─→ Derived Price Metrics (Cat 3): daily_return, returns, ranges, 52-week, volume metrics
  ├─→ Technical Indicators (Cat 12): SMA, EMA, RSI, MACD, Bollinger, ATR, ADX, OBV, S/R
  └─→ Valuation Metrics (Cat 8): market_cap → enterprise_value → EV ratios

Income Statement (Cat 4)
  ├─→ Growth Metrics: revenue_growth_yoy/qoq, eps_growth_yoy
  ├─→ Margins: gross_margin, net_profit_margin, effective_tax_rate
  ├─→ EBIT (calculated)
  └─→ Financial Ratios (Cat 7): roe, interest_coverage, dividend_payout_ratio
        └─→ Valuation (Cat 8): pe_ratio, peg_ratio, earnings_yield

Balance Sheet (Cat 5)
  ├─→ net_debt (calculated)
  ├─→ Financial Ratios (Cat 7): roa, roic, debt_to_equity, current_ratio, quick_ratio, asset_turnover, turnover ratios
  └─→ Valuation (Cat 8): pb_ratio, enterprise_value

Cash Flow (Cat 6)
  ├─→ free_cash_flow (calculated)
  └─→ Valuation (Cat 8): fcf_yield

Shareholding (Cat 9)
  └─→ promoter_holding_change, fii_holding_change (calculated)

Price + Shares Outstanding
  └─→ market_cap → market_cap_category
       └─→ enterprise_value (market_cap + net_debt)
```

### 5.2 Order of Computation

Calculations must follow this strict order to satisfy dependencies:

**Daily Calculation Pipeline:**
1. Ingest OHLCV data (Category 2)
2. Calculate Derived Price Metrics (Category 3) — depends on Cat 2
3. Calculate Technical Indicators (Category 12) — depends on Cat 2
4. Calculate daily Valuation Metrics (market_cap, pe_ratio, pb_ratio, ps_ratio, dividend_yield, earnings_yield) — depends on Cat 2 + latest financials
5. Update metadata fields (Category 13)

**Quarterly Calculation Pipeline (after financial data update):**
1. Scrape new financial data (Categories 4, 5, 6)
2. Calculate growth metrics (revenue_growth_yoy/qoq, eps_growth_yoy)
3. Calculate margins (gross_margin, net_profit_margin, effective_tax_rate)
4. Calculate EBIT, net_debt, free_cash_flow
5. Calculate Financial Ratios (Category 7) — depends on Cat 4, 5, 6
6. Recalculate quarterly Valuation Metrics (peg_ratio, ev_to_ebitda, ev_to_sales, fcf_yield) — depends on Cat 7 + Cat 2
7. Update historical_pe_median
8. Calculate peer averages (sector_avg_pe, sector_avg_roe, industry_avg_pe)
9. Update metadata

**Quarterly Shareholding Pipeline:**
1. Scrape shareholding data (Category 9)
2. Calculate promoter_holding_change, fii_holding_change

### 5.3 Ensuring Accuracy and Consistency

- **TTM (Trailing Twelve Months) calculations:** For ratios using annual data with quarterly updates (e.g., P/E using TTM EPS), sum the last 4 quarters for EPS instead of using the last annual figure. This ensures P/E reflects the most recent earnings.
- **Annualization:** Quarterly figures like operating_profit used in annual ratios must be annualized (×4) or preferably use TTM sums.
- **Consistent denominators:** For per-share metrics, use the same shares_outstanding figure across all calculations for a given date.
- **Currency consistency:** All monetary values in ₹ Crores. Per-share values in ₹.
- **Sign conventions:** Revenue, profit, assets = positive. Losses, debts, investing cash outflows = negative where appropriate. CapEx stored as positive for FCF calculation.
- **Null propagation:** If any dependency is null, the calculated field should also be null (not zero), with a metadata flag indicating the reason.

---

## 6. Reliability & Anti-Failure Mechanisms

### 6.1 Handling Website Structure Changes

- **DOM-based scraping with multiple selectors:** For each scraped data point, maintain a primary CSS/XPath selector and at least one fallback selector. If the primary selector returns zero results, attempt fallbacks before flagging failure.
- **Table-position fallback:** For financial data tables (Screener.in), use both column-header text matching and positional indexing. If column headers change labels, the positional fallback may still work.
- **Structural change detection:** After each scrape, compare the number of fields extracted against the expected count. If significantly fewer fields are found, log a warning and trigger an alert for manual selector review.
- **Page fingerprinting:** Store a hash of key structural elements (table count, header texts). Compare against stored fingerprint to detect structural changes early.
- **Version-controlled selectors:** Store all CSS/XPath selectors in a configuration file (not hard-coded) so they can be updated without changing system logic.

### 6.2 Retry Mechanisms

- **Exponential backoff:** Failed requests are retried with exponentially increasing delays (e.g., 2s, 4s, 8s, 16s, max 5 retries).
- **Source-level circuit breaker:** If a source fails 3 consecutive times within 1 hour, mark it as "degraded" and switch to backup sources. Resume attempts after a cooldown period.
- **Request-level timeout:** Each HTTP request has a configurable timeout (default 30 seconds for scraping, 60 seconds for file downloads).
- **Stale data acceptance:** If retries exhaust, serve the last known good data with a "stale" flag and freshness timestamp.

### 6.3 Logging and Monitoring

- **Structured logging:** Every extraction event logs: timestamp, source, module, stock symbol, fields extracted, fields missing, duration, status (success/partial/failure), error details.
- **Monitoring dashboard:** Aggregate logs into a monitoring view showing: extraction success rates by source, data freshness per category, field completeness percentages, error trends.
- **Alert triggers:**
  - Source failure rate > 10% → WARNING
  - Source failure rate > 50% → CRITICAL
  - Data staleness > 2 days for daily fields → WARNING
  - Data staleness > 7 days for daily fields → CRITICAL
  - Field completeness drops below threshold → WARNING

### 6.4 Data Completeness Checks

- After each extraction cycle, run a completeness audit per stock:
  - Count populated fields vs. expected 160
  - Flag stocks with < 80% completeness for investigation
  - Generate a coverage report by category
- **field_availability** (metadata field #158) — automatically tracks which fields are populated per stock

### 6.5 Detecting Missing Fields

- Each extraction module returns a manifest of expected fields vs. extracted fields
- Missing fields are categorized: (a) Field not available on source (expected), (b) Field available but extraction failed (error), (c) Field available but value is null/empty (data gap)
- Category (b) triggers retries and alerts; category (c) is logged as a data quality issue

### 6.6 Cross-Verification Between Sources

- For fields available from multiple sources (see Section 2.3): extract from all sources, compare values, and flag discrepancies
- **Tolerance thresholds:** Numerical values within 2% → accept primary; > 2% divergence → flag for review and store all values in `multi_source_values` metadata
- **Preference hierarchy:** Calculated > Official Source (NSE/BSE) > Screener.in > Trendlyne > yfinance

---

## 7. Storage & Structuring

### 7.1 Logical Database Schema (Conceptual)

The 160 fields are organized across the following logical entities:

**Entity: Stock Master**
- Primary Key: `symbol` (or internal numeric ID)
- Contains: All 14 fields from Category 1
- Type: Slowly changing dimension (SCD Type 2 for fields like sector, shares_outstanding)

**Entity: Daily Price Data**
- Primary Key: (`symbol`, `date`)
- Contains: 13 fields from Category 2 + 11 fields from Category 3 + 15 fields from Category 12
- Total: 39 daily fields per stock per trading day
- Type: Time-series, append-only

**Entity: Quarterly Financials**
- Primary Key: (`symbol`, `period_end_date`, `period_type` [Q1/Q2/Q3/Q4/Annual])
- Contains: 18 fields from Category 4
- Type: Slowly changing (restated financials overwrite)

**Entity: Annual Financials**
- Primary Key: (`symbol`, `financial_year`)
- Contains: 17 fields from Category 5 + 8 fields from Category 6
- Total: 25 annual fields
- Type: Slowly changing (restated financials overwrite)

**Entity: Financial Ratios**
- Primary Key: (`symbol`, `period_end_date`)
- Contains: 11 fields from Category 7
- Type: Versioned

**Entity: Valuation Metrics**
- Primary Key: (`symbol`, `date`)
- Contains: 17 fields from Category 8
- Type: Mixed (daily price-based + quarterly earnings-based)

**Entity: Shareholding Pattern**
- Primary Key: (`symbol`, `quarter_end_date`)
- Contains: 10 fields from Category 9
- Type: Time-series, quarterly append

**Entity: Corporate Actions**
- Primary Key: (`symbol`, `action_type`, `action_date`)
- Contains: 10 fields from Category 10
- Type: Event-driven, append-only

**Entity: News Articles**
- Primary Key: (`article_id` or `source_url`)
- Contains: 8 fields from Category 11 (news related)
- Type: Append-only with 30-day retention

**Entity: Credit Ratings**
- Primary Key: (`symbol`, `rating_agency`, `effective_date`)
- Contains: credit_rating, credit_outlook from Category 11
- Type: Event-driven

**Entity: Qualitative Assessments**
- Primary Key: (`symbol`, `assessment_date`)
- Contains: 5 qualitative fields from Category 13
- Type: Versioned

**Entity: Data Metadata**
- Primary Key: (`symbol`)
- Contains: 3 metadata fields from Category 13
- Type: Continuously updated

### 7.2 Time-Series Handling

- Daily data (OHLCV, technical indicators, daily valuations): Stored in time-series optimized tables partitioned by year or month
- Quarterly data (financials, shareholding): Stored with period-end-date indexing
- Maintain a trading calendar table to distinguish trading days from holidays
- All timestamps in IST (Indian Standard Time) with UTC offset stored

### 7.3 Version Tracking

- For data that can be restated (financials), maintain version columns: `version_number`, `created_at`, `updated_at`, `source_of_update`
- For qualitative assessments, maintain full version history (every assessment is a new row, with latest flagged as `is_current = true`)
- For master data, track changes using SCD Type 2 (effective_from, effective_to dates)

### 7.4 Metadata Tracking

For every stock, track:
- `field_availability`: Boolean map of all 160 fields → populated or not
- `field_last_updated`: Timestamp map of all 160 fields → when last successfully updated
- `multi_source_values`: For multi-source fields, store all source values with timestamps
- `extraction_log`: Per-stock log of extraction attempts, successes, and failures
- `data_quality_score`: Composite score based on completeness, freshness, and source agreement

---

## 8. Update & Scheduling Logic

### 8.1 Daily Updates (Trading Days Only)

**Triggered at:** 18:00 IST (after market close, when Bhavcopy becomes available)

| Sequence | Action | Fields Updated |
|----------|--------|---------------|
| 1 | Download NSE Bhavcopy | Cat 2: open, high, low, close, volume, delivery_volume, delivery_percentage, turnover, trades_count, prev_close, vwap |
| 2 | Fetch adjusted_close from yfinance | Cat 2: adjusted_close |
| 3 | Calculate derived price metrics | Cat 3: All 11 fields |
| 4 | Calculate technical indicators | Cat 12: All 15 fields |
| 5 | Calculate daily valuation metrics | Cat 8: market_cap, pe_ratio, pb_ratio, ps_ratio, dividend_yield, earnings_yield, historical_pe_median |
| 6 | Update market_cap_category | Cat 1: market_cap_category |
| 7 | Check NSE/BSE for corporate actions | Cat 10: dividend, split, bonus events |
| 8 | Download sector index data | Cat 8: sector_performance |
| 9 | Update metadata | Cat 13: field_availability, field_last_updated |

### 8.2 Quarterly Updates

**Triggered by:** Calendar-based (results season: Jan 15–Feb 28, Apr 15–May 31, Jul 15–Aug 31, Oct 15–Nov 30)

| Sequence | Action | Fields Updated |
|----------|--------|---------------|
| 1 | Scrape Screener.in for quarterly results | Cat 4: All 18 income statement fields |
| 2 | Scrape Screener.in for balance sheet updates | Cat 5: total_debt, cash_and_equivalents (quarterly fields) |
| 3 | Calculate quarterly growth metrics | Cat 4: revenue_growth_yoy/qoq, eps_growth_yoy |
| 4 | Calculate/recalculate financial ratios | Cat 7: roe, debt_to_equity, interest_coverage |
| 5 | Recalculate quarterly valuation metrics | Cat 8: peg_ratio, ev_to_ebitda, pe_ratio_forward |
| 6 | Scrape BSE for shareholding pattern | Cat 9: All 10 fields |
| 7 | Calculate shareholding changes | Cat 9: promoter_holding_change, fii_holding_change |
| 8 | Update shares_outstanding | Cat 1: shares_outstanding, free_float_shares |
| 9 | Scrape peer averages | Cat 8: sector_avg_pe, sector_avg_roe, industry_avg_pe |

### 8.3 Annual Updates

**Triggered by:** Calendar-based (after annual results season, typically May–September)

| Sequence | Action | Fields Updated |
|----------|--------|---------------|
| 1 | Scrape Screener.in for annual financials | Cat 5: All 17 balance sheet fields |
| 2 | Scrape Screener.in for cash flow statement | Cat 6: All 8 fields |
| 3 | Calculate annual ratios | Cat 7: roa, roic, current_ratio, quick_ratio, asset_turnover, inventory_turnover, receivables_turnover, dividend_payout_ratio |
| 4 | Calculate FCF, net_debt | Cat 6: free_cash_flow; Cat 5: net_debt |
| 5 | Recalculate annual valuation metrics | Cat 8: fcf_yield, ev_to_sales |
| 6 | Extract contingent_liabilities from annual report | Cat 5: contingent_liabilities |
| 7 | Update book_value_per_share | Cat 5: book_value_per_share |

### 8.4 Event-Based Triggers

| Event | Detection Method | Fields Updated |
|-------|-----------------|---------------|
| New corporate action (dividend/split/bonus) | Daily BSE/NSE scan | Cat 10: relevant action fields |
| Earnings date announced | BSE announcement scrape | Cat 10: next_earnings_date |
| Stock suspended/delisted | NSE/BSE equity list check | Cat 10: stock_status |
| SEBI investigation | News RSS + SEBI orders page | Cat 10: sebi_investigation |
| Credit rating change | Rating agency website scan | Cat 11: credit_rating, credit_outlook |
| New listing | NSE/BSE equity list diff | Cat 1: New stock master record |
| Symbol/name change | NSE/BSE equity list diff | Cat 1: symbol, company_name |

### 8.5 Real-Time Ingestion (News)

- **RSS polling frequency:** Every 5–15 minutes during market hours; every 30 minutes off-hours
- **Processing pipeline:** Poll → Parse → Dedup → Fetch full article → Sentiment analysis → Store
- **Retention:** 30-day rolling window; older articles archived or deleted
- **Volume management:** Cap at 100 articles per stock per 30-day window; prioritize by source credibility

---

## 9. Quality Control Framework

### 9.1 Validation Rules by Category

**Category 1 — Stock Master Data:**
- `symbol` must be non-empty and match [A-Z&-] pattern
- `isin` must match `INE[0-9A-Z]{9}` (12 characters)
- `sector` and `industry` must be from a controlled vocabulary list
- `market_cap_category` must be one of: Large Cap, Mid Cap, Small Cap, Micro Cap
- `shares_outstanding` must be > 0

**Category 2 — Price & Volume:**
- `open`, `high`, `low`, `close` must satisfy: low ≤ open ≤ high AND low ≤ close ≤ high
- All prices must be > 0
- `volume` must be ≥ 0 (0 only for trading halts)
- `delivery_percentage` must be 0–100%
- `vwap` must be between `low` and `high`

**Category 3 — Derived Metrics:**
- `daily_return_pct` must be within ±50% (flag extremes beyond ±20% for stocks with circuit limits)
- `52_week_high` ≥ `52_week_low`
- `volume_ratio` must be ≥ 0

**Category 4 — Income Statement:**
- `revenue` should generally be > 0 (negative revenue is extremely rare and should be flagged)
- `operating_margin` typically −100% to +100%
- `eps` can be negative (loss-making companies)
- `effective_tax_rate` should be 0–50% range; values outside flagged

**Category 5 — Balance Sheet:**
- `total_assets` = approximately `total_equity` + total liabilities (sanity check)
- `current_ratio` values < 0.1 or > 50 are suspicious
- `total_debt` ≥ 0

**Category 6 — Cash Flow:**
- `free_cash_flow` = `operating_cash_flow` − `capital_expenditure` must hold exactly
- Sign conventions must be validated

**Category 7 — Financial Ratios:**
- `roe` > 100% or < −100% → flag as anomalous
- `debt_to_equity` > 10 → flag as highly leveraged
- `interest_coverage` < 0 → flag; < 1 → critical alerting

**Category 8 — Valuation:**
- `pe_ratio` should not be negative (store as null for loss-making)
- `pe_ratio` > 500 → flag as extreme
- `dividend_yield` must be ≥ 0
- `market_cap` must equal `close` × `shares_outstanding` (within rounding tolerance)

**Category 9 — Shareholding:**
- `promoter_holding` + `fii_holding` + `dii_holding` + `public_holding` ≈ 100% (tolerance ±2%)
- All holding percentages must be 0–100%
- `promoter_pledging` must be 0–100% of promoter holding

**Category 10 — Corporate Actions:**
- `stock_status` must be from: ACTIVE, SUSPENDED, DELISTED, ASM, GSM
- `sebi_investigation` must be a boolean

**Category 11 — News:**
- `news_sentiment_score` must be within [−1, +1]
- `news_timestamp` must not be in the future
- `credit_rating` must match known agency rating scales

**Category 12 — Technical Indicators:**
- `rsi_14` must be 0–100
- `sma_200` must be > 0
- `bollinger_upper` > `sma_20` > `bollinger_lower`

### 9.2 Threshold Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| Negative revenue | revenue < 0 | WARNING |
| Extreme P/E | pe_ratio > 500 or pe_ratio < 0 | WARNING |
| D/E explosion | debt_to_equity > 5 | CRITICAL (D8 deal-breaker) |
| Interest coverage collapse | interest_coverage < 2 | CRITICAL (D1 deal-breaker) |
| Promoter pledging high | promoter_pledging > 80% | CRITICAL (D7 deal-breaker) |
| Volume anomaly | volume_ratio > 10 | WARNING |
| Shareholding mismatch | Sum of holdings ≠ 100% (±2%) | DATA_ERROR |
| Price gap > 20% | gap_percentage > 20% | WARNING |
| RSI extreme | rsi_14 < 10 or rsi_14 > 90 | INFO |

### 9.3 Data Freshness Tracking

For each field, track `field_last_updated` (metadata field #159). Define staleness thresholds:

| Update Frequency | Stale After | Critical After |
|-----------------|-------------|----------------|
| Daily | 2 trading days | 5 trading days |
| Weekly | 10 days | 21 days |
| Quarterly | 60 days from quarter end | 90 days |
| Annual | 6 months from FY end | 12 months |
| Real-time (news) | 1 hour | 6 hours |
| On Event | N/A (checked on access) | N/A |

### 9.4 Confidence Scoring System

Each stock receives a **Data Confidence Score** (0–100) based on three components derived from metadata fields #158, #159, and #160:

1. **Data Completeness (40% weight):** Percentage of 160 fields that are populated (from `field_availability`)
2. **Data Freshness (30% weight):** Percentage of fields updated within their expected staleness threshold (from `field_last_updated`)
3. **Source Agreement (15% weight):** For multi-source fields, percentage where sources agree within tolerance (from `multi_source_values`)
4. **Priority Coverage (15% weight):** Weighted completeness giving more weight to Critical (🔴) and Important (🟡) fields

**Score interpretation:**
- 90–100: Excellent — All major data available and fresh
- 70–89: Good — Minor gaps or some stale data
- 50–69: Fair — Significant gaps; analysis may be unreliable
- Below 50: Poor — Insufficient data for meaningful analysis; flag prominently in UI

---

## 10. System Features

### 10.1 Complete 160-Field Extraction

The system guarantees extraction attempts for **all 160 data fields** across 13 categories. Every field listed in the V2 requirements specification has a defined extraction method, source, backup source (where available), and validation rule.

### 10.2 Automatic Calculation of Derived Metrics

**52 fields** are automatically calculated from extracted data:
- 11 Derived Price Metrics (Category 3)
- 7 calculated fields within Income Statement (Category 4)
- 2 calculated fields within Balance Sheet (Category 5)
- 1 calculated field within Cash Flow (Category 6)
- 11 Financial Ratios (Category 7)
- ~13 Valuation Metrics (Category 8)
- 2 Shareholding changes (Category 9)
- 15 Technical Indicators (Category 12)
- 3 Metadata fields (Category 13)

All calculations follow explicit formulas with defined dependency ordering.

### 10.3 Organized and Structured Storage

Data is stored in 12 logical entities (see Section 7.1) with clear separation between:
- Reference data (stock master)
- Time-series data (daily prices, indicators)
- Periodic data (quarterly/annual financials)
- Event data (corporate actions, news)
- Metadata (quality tracking)

### 10.4 Historical Depth Management

| Data Type | Required Depth | Storage Strategy |
|-----------|---------------|-----------------|
| OHLCV + Derived + Technical | 10 years (~2,500 days/stock) | Partitioned time-series tables |
| Income Statement | 10 years (~40 quarters) | Quarterly period tables |
| Balance Sheet + Cash Flow | 10 years (10 annual records) | Annual period tables |
| Financial Ratios | 10 years | Period-indexed tables |
| Valuation Metrics | 10 years daily | Time-series tables |
| Shareholding | 5–7 years (~20–28 quarters) | Quarterly tables |
| Corporate Actions | 10 years | Event tables |
| News & Sentiment | 30 days rolling | Append-only with TTL |
| Technical (S/R levels) | 1 year | Daily tables |
| Qualitative | Current only | Versioned snapshots |

**Backfill Strategy:** On initial system setup, perform a one-time historical backfill:
- OHLCV: Batch-download 10 years of Bhavcopy archives + yfinance historical data
- Financials: Scrape all available historical data from Screener.in (typically 10+ years)
- Shareholding: Scrape BSE filings archive (5–7 years available)
- Corporate actions: Scrape BSE/NSE historical corporate actions pages

### 10.5 Multi-Source Validation

For fields available from multiple sources, the system:
1. Extracts from all available sources
2. Compares values within defined tolerance (2% for numerical)
3. Selects the primary source value as canonical
4. Stores all source values in `multi_source_values` metadata
5. Flags discrepancies for review
6. Contributes to the confidence score

### 10.6 Fault Tolerance

- Independent module execution: failure in one module does not block others
- Circuit breaker pattern for degraded sources
- Exponential backoff retry with configurable limits
- Graceful degradation: stale data served with freshness flags when sources are down
- Idempotent extraction jobs: safe to re-run without data corruption

### 10.7 Scalable Design

- Adding new stocks: Only requires adding symbol to the tracking list; all extraction logic is symbol-agnostic
- Adding new sources: New extraction modules can be plugged in following the module interface pattern
- Adding new fields: Add field definition to configuration; update relevant extraction module and validation rules
- Performance: Extraction is parallelizable across stocks; rate limiting is per-source, not per-stock

---

## 11. Data Processing & Structuring

### 11.1 Data Cleaning

**Numerical Data:**
- Remove currency symbols (₹), commas, and percentage signs from scraped values
- Convert text representations to appropriate numeric types (Decimal for monetary, Integer for counts)
- Handle "Cr" / "Lakh" abbreviations in scraped data — normalize to Crores
- Detect and handle special values: "N/A", "NA", "-", empty strings → convert to null

**Text Data:**
- Strip leading/trailing whitespace
- Normalize Unicode characters (e.g., fancy quotes to standard quotes)
- For news body text: Remove HTML tags, scripts, navigation elements, ads
- For company names: Standardize suffixes (Ltd, Limited, Ltd.)

**Date/Time Data:**
- Parse multiple date formats commonly used by Indian sources (DD-MM-YYYY, DD/MM/YYYY, YYYY-MM-DD)
- Normalize all dates to ISO 8601 format (YYYY-MM-DD)
- Convert all timestamps to IST with UTC offset

### 11.2 Validation Mechanisms

**Schema Validation:**
- Every field has a defined type (String, Decimal, Integer, Date, Boolean, Enum, List, Dict)
- Type mismatches are logged and the value is rejected

**Range Validation:**
- Numerical fields are checked against acceptable ranges (see Section 9.1)
- Out-of-range values are flagged but stored with a quality warning

**Relational Validation:**
- Cross-field consistency checks (e.g., low ≤ close ≤ high; total_assets ≈ equity + liabilities)
- Temporal consistency (new quarterly data dates must be after previous quarter)

### 11.3 Deduplication

**Daily Price Data:** Deduplicate by composite key (`symbol`, `date`). If duplicate found, prefer the newer extraction's data.

**News Articles:** Deduplicate by (`source_url`). Also perform fuzzy headline matching (>90% similarity) to catch same-story duplicates from different RSS entries.

**Financial Data:** Deduplicate by (`symbol`, `period_end_date`). Latest extraction overwrites previous (to handle restated figures).

**Corporate Actions:** Deduplicate by (`symbol`, `action_type`, `record_date`/`ex_date`).

### 11.4 Normalization

**Monetary Normalization:**
- All monetary values standardized to ₹ Crores
- Per-share values in ₹ (not paise)
- Convert Lakh/Thousand values to Crores where encountered

**Percentage Normalization:**
- All percentage values stored as decimals (e.g., 15.67 not 0.1567)
- Ensure consistent convention across all categories

**Entity Normalization:**
- Sector/Industry names mapped to controlled vocabulary
- Company names matched against master list for consistency
- Stock symbols normalized to NSE convention (uppercase, no spaces)

### 11.5 Data Structuring and Categorization

Extracted data is organized into the 13 defined categories before storage:
1. Each extraction module outputs data tagged with category and field identifiers
2. The processing layer routes data to the appropriate storage entity
3. Calculated fields are generated in dependency order and tagged with their category
4. Metadata fields are updated last, reflecting the final state of all other categories

---

## 12. Data Storage & Organization

### 12.1 Database Structure (Conceptual)

The system uses a **relational database** as the primary store with the following logical schema groupings:

**Core Reference Tables:**
- `stock_master` — 14 fields (Category 1), one row per stock with SCD Type 2 history
- `trading_calendar` — IST trading days, holidays, settlement dates

**Time-Series Tables (Partitioned by Year):**
- `daily_price_data` — 13 OHLCV fields (Cat 2) + 11 derived metrics (Cat 3) + 15 technical indicators (Cat 12) = 39 fields per row
- `daily_valuation` — 17 valuation fields (Cat 8) where daily updates apply (market_cap, pe_ratio, pb_ratio, ps_ratio, dividend_yield, earnings_yield, sector_performance, historical_pe_median)

**Periodic Tables:**
- `quarterly_income` — 18 income statement fields (Cat 4), keyed by (symbol, period_end, period_type)
- `annual_balance_sheet` — 17 balance sheet fields (Cat 5), keyed by (symbol, financial_year)
- `annual_cash_flow` — 8 cash flow fields (Cat 6), keyed by (symbol, financial_year)
- `financial_ratios` — 11 ratio fields (Cat 7), keyed by (symbol, period_end)
- `shareholding_pattern` — 10 shareholding fields (Cat 9), keyed by (symbol, quarter_end)

**Event Tables:**
- `corporate_actions` — 10 fields (Cat 10), keyed by (symbol, action_type, action_date)
- `news_articles` — 6 news fields (Cat 11), keyed by (article_id)
- `credit_ratings` — 2 credit fields (Cat 11), keyed by (symbol, agency, effective_date)

**Assessment & Metadata Tables:**
- `qualitative_assessments` — 5 qualitative fields (Cat 13), keyed by (symbol, assessment_date)
- `data_metadata` — 3 metadata fields (Cat 13), keyed by (symbol)
- `extraction_logs` — Audit trail of all extraction events

### 12.2 Folder Organization (Raw Data Archive)

```
data/
├── raw/
│   ├── bhavcopy/
│   │   ├── 2025/
│   │   │   ├── 01/
│   │   │   │   ├── cm10JAN2025bhav.csv
│   │   │   │   └── ...
│   │   │   └── 02/
│   │   └── 2024/
│   ├── screener/
│   │   ├── RELIANCE/
│   │   │   ├── quarterly_2025-01.html
│   │   │   ├── balance_sheet_2025.html
│   │   │   └── cash_flow_2025.html
│   │   └── TCS/
│   ├── bse_filings/
│   │   ├── shareholding/
│   │   └── announcements/
│   ├── rss/
│   │   ├── moneycontrol/
│   │   ├── economic_times/
│   │   └── business_standard/
│   └── equity_lists/
│       ├── nse_equity_list_2025-02-12.csv
│       └── bse_equity_list_2025-02-12.csv
├── processed/
│   └── (database files or connection)
├── config/
│   ├── selectors.yaml
│   ├── field_definitions.yaml
│   ├── validation_rules.yaml
│   └── source_config.yaml
└── logs/
    ├── extraction/
    ├── processing/
    └── alerts/
```

### 12.3 Metadata Management

Each record in the database carries system metadata columns:
- `created_at` — Timestamp when the record was first inserted
- `updated_at` — Timestamp of last modification
- `source` — Which extraction module produced this data
- `extraction_run_id` — Links to the extraction_logs table
- `data_quality_flag` — GOOD / WARNING / ERROR

Per-stock metadata (in `data_metadata` table):
- `field_availability` — JSON dictionary of 160 field names → boolean (populated or not)
- `field_last_updated` — JSON dictionary of 160 field names → ISO timestamp
- `multi_source_values` — JSON dictionary of multi-source fields → { source: value, ... }
- `confidence_score` — Computed 0–100 score (see Section 9.4)
- `last_full_extraction` — Timestamp of last complete extraction cycle

### 12.4 Versioning and Update Tracking

- **Financial data versioning:** When restated financials are detected, the old row is soft-deleted (flagged `is_superseded = true`) and a new row is inserted. This preserves the audit trail.
- **Master data versioning (SCD Type 2):** For fields like `sector`, `shares_outstanding`, `face_value` — when a change is detected, the old row gets an `effective_to` date and a new row is created with `effective_from` = today.
- **Qualitative assessment versioning:** Every manual or LLM assessment creates a new versioned row; the latest is flagged `is_current = true`.
- **Extraction audit trail:** Every extraction run is logged with: run_id, module, start_time, end_time, stocks_processed, fields_extracted, fields_failed, status.

---

## 13. Scalability & Future Expansion

### 13.1 Scaling Stock Coverage

The system is designed to be **stock-agnostic** — all extraction logic is parameterized by symbol. To add more stocks:
1. Add the stock symbol and ISIN to the `stock_master` table
2. The scheduled extraction jobs will automatically pick up new entries
3. Historical backfill runs once for the new stock
4. No changes to extraction logic or configuration required

**Current target:** All NSE-listed equities (~2,000 stocks)
**Expandable to:** BSE-only stocks, SME listings (~5,000+ total)

### 13.2 Adding New Data Sources

The modular extraction architecture makes adding new sources straightforward:
1. Create a new extraction module following the standard module interface (input: stock list, output: structured field data)
2. Register the module in the orchestration layer with its schedule and category coverage
3. Add source-specific configuration (URLs, selectors, rate limits) to `source_config.yaml`
4. Update `field_definitions.yaml` to include the new source as primary or backup for relevant fields
5. Add validation rules for data from the new source

**Potential future sources:**
- NSE API (when available) — for real-time or near-real-time data
- Bloomberg/Reuters terminals — for institutional-grade data
- SEBI EDGAR-like systems — for regulatory filings
- Social media APIs (Twitter/X, StockTwits) — for alternative sentiment
- Broker APIs — for real-time quotes
- MCA (Ministry of Corporate Affairs) — for annual return filings

### 13.3 Extending Data Types

To add new data fields beyond the current 160:
1. Define the field in `field_definitions.yaml` with: name, type, category, source, update frequency, priority, validation rules
2. Update the relevant extraction module to extract the new field
3. If calculated, add the formula to the calculation engine with dependency mapping
4. Update `field_availability` tracking to include the new field
5. Update validation rules and threshold alerts as needed

**Potential future data types:**
- Intraday tick data (requires real-time infrastructure)
- Options chain data (OI, IV, Greeks)
- Mutual fund holdings breakdown
- Insider trading data (SAST filings)
- ESG scores and sustainability metrics
- Alternative data (satellite imagery, web traffic)

### 13.4 Performance Optimization Strategies

**Extraction Performance:**
- Parallel extraction across stocks (configurable concurrency per source to respect rate limits)
- Connection pooling for HTTP requests
- Caching of static/slow-changing data (sector/industry lists, equity lists)
- Differential scraping: only re-scrape pages where data is expected to have changed

**Storage Performance:**
- Time-series table partitioning by year (10 partitions for 10-year history)
- Indexing on (symbol, date) for all time-series queries
- Materialized views for frequently accessed aggregate data (sector averages, peer groups)
- Archive old news data beyond 30 days to separate cold storage

**Calculation Performance:**
- Batch calculation: compute derived metrics for all stocks in one pass rather than per-stock
- Incremental calculation: only recalculate what changed (e.g., today's technical indicators, not full 10-year recalculation)
- Caching intermediate results (TTM values, rolling averages)

**Rate Limiting & Politeness:**
- Per-source rate limiting: Screener.in (2 req/sec), BSE (1 req/sec), Trendlyne (1 req/2sec)
- Random delays between requests to avoid pattern detection
- Rotate User-Agent strings
- Respect robots.txt directives

---

## 14. Features of the System

### 14.1 Complete Data Extraction

- **160 fields** fully specified with extraction methods, sources, and validation
- **13 categories** of data covering the entire spectrum of stock analysis needs
- **8 primary data sources** integrated with backup sources for critical fields
- **58 Critical fields** (🔴) guaranteed ≥99% fill rate
- Every field in the V2 specification is mapped to at least one extraction method

### 14.2 Automatic Structuring and Categorization

- Extracted data is automatically routed to the correct storage entity based on category
- Field types are enforced (String, Decimal, Integer, Date, Boolean, Enum, List, Dict)
- Data is normalized (currency to ₹ Cr, dates to ISO 8601, percentages to consistent format)
- Each record carries metadata tags for source, extraction time, and quality status

### 14.3 Organized, Presentation-Ready Output

- Data stored in 12 logical entities optimized for different query patterns
- Time-series data partitioned for efficient range queries (e.g., "show me 5-year P/E history")
- Peer comparison data pre-computed (sector averages, industry averages)
- Confidence scores available per stock for data reliability signaling
- Latest values readily accessible with historical depth available on demand

### 14.4 Multi-Method Extraction Support

The system employs **5 distinct extraction methods** to ensure complete coverage:

| Method | Used For | Sources |
|--------|---------|---------|
| **Web Scraping** | Financial statements, shareholding, corporate actions, ratings, peer data | Screener.in, BSE, Trendlyne, Rating Agencies |
| **File Download** | Daily OHLCV, equity lists | NSE Bhavcopy, NSE/BSE CSV files |
| **API Calls** | Adjusted prices, backup OHLCV | yfinance |
| **RSS Parsing** | News headlines, articles | Moneycontrol, ET, BS, LiveMint |
| **Internal Calculation** | Derived metrics, ratios, technical indicators, valuations | pandas-ta, custom formulas |

### 14.5 Intelligent Website Format Handling

- **Multi-selector strategy:** Primary + fallback CSS/XPath selectors for each data point
- **Table parsing intelligence:** Header-text matching and positional fallback for Screener.in financial tables
- **Format-adaptive parsing:** Handles varying date formats, number formats, and currency representations across sources
- **Structural change detection:** Page fingerprinting to detect and alert on website redesigns
- **Configuration-driven selectors:** All selectors externalized to YAML config for easy updates without logic changes

### 14.6 Summary of All 160 Fields by Extraction Method

| Extraction Method | Field Count | Percentage |
|------------------|-------------|------------|
| Web Scraping (Screener.in) | ~45 | 28% |
| File Download (NSE Bhavcopy) | ~12 | 8% |
| Web Scraping (BSE Filings) | ~12 | 8% |
| Web Scraping (BSE/NSE Announcements) | ~10 | 6% |
| Web Scraping (Trendlyne) | ~3 | 2% |
| API (yfinance) | ~1 | 1% |
| RSS Parsing + NLP | ~6 | 4% |
| Web Scraping (Rating Agencies) | ~2 | 1% |
| Internal Calculation | ~57 | 36% |
| Manual / LLM | ~5 | 3% |
| System Auto-generated | ~3 | 2% |
| Download (NSE/BSE Equity Lists) | ~4 | 3% |
| **TOTAL** | **160** | **100%** |

### 14.7 StockPulse Scoring System — Field Mapping

The V2 requirements reference a scoring system where specific fields serve as inputs to **Deal-Breakers (D)**, **Red Flags (R)**, and **Quality Boosters (Q)**. The extraction system must guarantee these fields are available, fresh, and accurate because they directly drive investment scoring.

#### Deal-Breakers (D1–D10) — Automatic Rejection if Triggered

| Code | Rule | Field(s) Required | Threshold |
|------|------|--------------------|-----------|
| D1 | Interest Coverage Too Low | `interest_coverage` (#86) | < 2x |
| D2 | SEBI Investigation Active | `sebi_investigation` (#129) | = true |
| D3 | Revenue Declining | `revenue` (#39), `revenue_growth_yoy` (#40) | Negative YoY for 3+ quarters |
| D4 | Negative Operating Cash Flow | `operating_cash_flow` (#74) | < 0 for 2+ years |
| D5 | Negative Free Cash Flow | `free_cash_flow` (#78) | < 0 for 3+ years |
| D6 | Stock Suspended/Delisted | `stock_status` (#128) | ≠ ACTIVE |
| D7 | Excessive Promoter Pledging | `promoter_pledging` (#111) | > 80% |
| D8 | Extreme Debt-to-Equity | `debt_to_equity` (#85) | > 5 |
| D9 | Poor Credit Rating | `credit_rating` (#136) | Below investment grade |
| D10 | Insufficient Liquidity | `volume` (#21), `avg_volume_20d` (#38) | Avg volume < 50,000 |

#### Red Flags (R1–R10) — Score Penalties

| Code | Rule | Field(s) Required | Trigger |
|------|------|--------------------|---------|
| R1 | High Debt | `debt_to_equity` (#85) | > 1.5 |
| R2 | Weak Interest Coverage | `interest_coverage` (#86) | 2–3x range |
| R3 | Low ROE | `roe` (#82) | < 10% |
| R4 | Promoter Holding Decline | `promoter_holding` (#110), `promoter_holding_change` (#115) | ↓ > 5% |
| R5 | Promoter Pledging Exists | `promoter_pledging` (#111) | > 0% |
| R6 | Far from 52-Week High | `distance_from_52w_high` (#36) | > 30% |
| R7 | Margin Contraction | `operating_margin` (#43) | Declining trend |
| R8 | Overvalued (P/E) | `pe_ratio` (#95), `sector_avg_pe` (#105) | P/E > 2× sector avg |
| R9 | Low Delivery Volume | `delivery_percentage` (#23) | < 30% consistently |
| R10 | Contingent Liabilities | `contingent_liabilities` (#73) | > 10% of net worth |

#### Quality Boosters (Q1–Q9) — Score Additions

| Code | Rule | Field(s) Required | Trigger |
|------|------|--------------------|---------|
| Q1 | Consistent High ROE | `roe` (#82) | > 20% for 5 years |
| Q2 | Revenue Growth | `revenue_growth_yoy` (#40) | > 15% |
| Q3 | Zero Debt | `debt_to_equity` (#85) | = 0 |
| Q4 | Consistent Dividends | `dividends_paid` (#79), `dividend_payout_ratio` (#92) | 10+ consecutive years |
| Q5 | Increasing Promoter Holding | `promoter_holding_change` (#115) | ↑ |
| Q6 | FII Accumulation | `fii_holding` (#112), `fii_holding_change` (#116) | ↑ > 2% |
| Q7 | High Operating Margin | `operating_margin` (#43) | > 25% |
| Q8 | Near 52-Week High | `52_week_high` (#34), `distance_from_52w_high` (#36) | Close to high |
| Q9 | Strong FCF Yield | `fcf_yield` (#103) | > 5% |

**Extraction System Implication:** All fields referenced in D, R, and Q rules are classified as 🔴 Critical or 🟡 Important priority. The extraction system must guarantee ≥99% availability for these fields on every tracked stock.

---

## Appendix A: Complete 160-Field Reference

| # | Field Name | Category | Type | Source | Method | Update | Priority | Used For |
|---|-----------|----------|------|--------|--------|--------|----------|----------|
| 1 | symbol | Stock Master | String | NSE/BSE | Download | On listing | 🔴 Critical | Primary identifier |
| 2 | company_name | Stock Master | String | NSE/BSE | Download | On change | 🔴 Critical | UI display name |
| 3 | isin | Stock Master | String(12) | NSE/BSE | Download | Never | 🔴 Critical | Cross-exchange ID |
| 4 | nse_code | Stock Master | String | NSE | Download | On change | 🔴 Critical | NSE trading symbol |
| 5 | bse_code | Stock Master | String | BSE | Download | On change | 🟡 Important | BSE scrip code |
| 6 | sector | Stock Master | String | Screener.in | Scrape | On change | 🔴 Critical | Sector comparison |
| 7 | industry | Stock Master | String | Screener.in | Scrape | On change | 🔴 Critical | Industry peer comparison |
| 8 | market_cap_category | Stock Master | Enum | Calculated | Internal | Daily | 🟡 Important | Size classification |
| 9 | listing_date | Stock Master | Date | NSE/BSE | Download | Never | 🟢 Standard | Company age analysis |
| 10 | face_value | Stock Master | Decimal | NSE/BSE | Download | On split | 🟢 Standard | Corp action adjustment |
| 11 | shares_outstanding | Stock Master | Integer | BSE Filings | Scrape | Quarterly | 🟡 Important | Market cap, EPS calc |
| 12 | free_float_shares | Stock Master | Integer | BSE Filings | Scrape | Quarterly | 🟢 Standard | Float analysis |
| 13 | website | Stock Master | URL | Screener.in | Scrape | Never | ⚪ Optional | Company research |
| 14 | registered_office | Stock Master | String | BSE | Scrape | Never | ⚪ Optional | Company info |
| 15 | date | Price & Volume | Date | NSE Bhavcopy | Download | Daily | 🔴 Critical | Time series key |
| 16 | open | Price & Volume | Decimal (₹) | NSE Bhavcopy | Download | Daily | 🔴 Critical | Candlestick, gap analysis |
| 17 | high | Price & Volume | Decimal (₹) | NSE Bhavcopy | Download | Daily | 🔴 Critical | Range, resistance |
| 18 | low | Price & Volume | Decimal (₹) | NSE Bhavcopy | Download | Daily | 🔴 Critical | Range, support |
| 19 | close | Price & Volume | Decimal (₹) | NSE Bhavcopy | Download | Daily | 🔴 Critical | All calculations |
| 20 | adjusted_close | Price & Volume | Decimal (₹) | yfinance | API | Daily | 🔴 Critical | Accurate returns |
| 21 | volume | Price & Volume | Integer | NSE Bhavcopy | Download | Daily | 🔴 Critical | Liquidity, D10 |
| 22 | delivery_volume | Price & Volume | Integer | NSE Bhavcopy | Download | Daily | 🟡 Important | Genuine buying |
| 23 | delivery_percentage | Price & Volume | Decimal (%) | NSE Bhavcopy | Download | Daily | 🟡 Important | Buyer conviction, R9 |
| 24 | turnover | Price & Volume | Decimal (₹ Cr) | NSE Bhavcopy | Download | Daily | 🟡 Important | Value traded |
| 25 | trades_count | Price & Volume | Integer | NSE Bhavcopy | Download | Daily | 🟡 Important | Participation breadth |
| 26 | prev_close | Price & Volume | Decimal (₹) | NSE Bhavcopy | Download | Daily | 🟢 Standard | Daily change calc |
| 27 | vwap | Price & Volume | Decimal (₹) | NSE | Scrape | Daily | 🟢 Standard | Institutional benchmark |
| 28 | daily_return_pct | Derived Metrics | Decimal (%) | Calculated | Internal | Daily | 🔴 Critical | Return analysis, volatility, ML |
| 29 | return_5d_pct | Derived Metrics | Decimal (%) | Calculated | Internal | Daily | 🟢 Standard | ML feature — 5-day momentum |
| 30 | return_20d_pct | Derived Metrics | Decimal (%) | Calculated | Internal | Daily | 🟢 Standard | ML feature — 20-day momentum |
| 31 | return_60d_pct | Derived Metrics | Decimal (%) | Calculated | Internal | Daily | 🟢 Standard | ML feature — 60-day momentum |
| 32 | day_range_pct | Derived Metrics | Decimal (%) | Calculated | Internal | Daily | 🟢 Standard | Intraday volatility, ML |
| 33 | gap_percentage | Derived Metrics | Decimal (%) | Calculated | Internal | Daily | 🟢 Standard | Gap detection, ML feature |
| 34 | 52_week_high | Derived Metrics | Decimal (₹) | Calculated | Internal | Daily | 🔴 Critical | Technical analysis, Q8 |
| 35 | 52_week_low | Derived Metrics | Decimal (₹) | Calculated | Internal | Daily | 🔴 Critical | Support detection |
| 36 | distance_from_52w_high | Derived Metrics | Decimal (%) | Calculated | Internal | Daily | 🟡 Important | R6 penalty (>30%) |
| 37 | volume_ratio | Derived Metrics | Decimal | Calculated | Internal | Daily | 🟡 Important | Volume spike, ML feature |
| 38 | avg_volume_20d | Derived Metrics | Integer | Calculated | Internal | Daily | 🔴 Critical | D10 deal-breaker (<50k) |
| 39 | revenue | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🔴 Critical | D3, growth, P/S |
| 40 | revenue_growth_yoy | Income Statement | Decimal (%) | Calculated | Internal | Quarterly | 🔴 Critical | D3, scoring (>15%=Q2) |
| 41 | revenue_growth_qoq | Income Statement | Decimal (%) | Calculated | Internal | Quarterly | 🟡 Important | Quarterly momentum |
| 42 | operating_profit | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🔴 Critical | Op margin calc |
| 43 | operating_margin | Income Statement | Decimal (%) | Screener.in | Scrape | Quarterly | 🔴 Critical | Q7 (>25%), R7 |
| 44 | gross_profit | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟡 Important | Gross margin |
| 45 | gross_margin | Income Statement | Decimal (%) | Calculated | Internal | Annual | 🟡 Important | Pricing power |
| 46 | net_profit | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🔴 Critical | EPS, P/E |
| 47 | net_profit_margin | Income Statement | Decimal (%) | Calculated | Internal | Quarterly | 🔴 Critical | Profitability |
| 48 | eps | Income Statement | Decimal (₹) | Screener.in | Scrape | Quarterly | 🔴 Critical | P/E, EPS growth |
| 49 | eps_growth_yoy | Income Statement | Decimal (%) | Calculated | Internal | Quarterly | 🔴 Critical | PEG calculation |
| 50 | interest_expense | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🔴 Critical | Interest coverage (D1) |
| 51 | depreciation | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🟡 Important | EBITDA calc |
| 52 | ebitda | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🟡 Important | EV/EBITDA |
| 53 | ebit | Income Statement | Decimal (₹ Cr) | Calculated | Internal | Quarterly | 🟡 Important | Interest coverage |
| 54 | other_income | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🟡 Important | Core vs non-core |
| 55 | tax_expense | Income Statement | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🟢 Standard | Tax rate |
| 56 | effective_tax_rate | Income Statement | Decimal (%) | Calculated | Internal | Annual | 🟢 Standard | Tax efficiency |
| 57 | total_assets | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🔴 Critical | ROA calculation |
| 58 | total_equity | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🔴 Critical | ROE, D/E, BV |
| 59 | total_debt | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🔴 Critical | D/E, D8 deal-breaker |
| 60 | long_term_debt | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟡 Important | Debt structure |
| 61 | short_term_debt | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟡 Important | Short-term liquidity |
| 62 | cash_and_equivalents | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Quarterly | 🔴 Critical | Net debt, Q3 |
| 63 | net_debt | Balance Sheet | Decimal (₹ Cr) | Calculated | Internal | Quarterly | 🟡 Important | EV calculation |
| 64 | current_assets | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟡 Important | Current ratio |
| 65 | current_liabilities | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟡 Important | Current/Quick ratio |
| 66 | inventory | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟡 Important | Quick ratio |
| 67 | receivables | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟢 Standard | Receivables turnover |
| 68 | payables | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟢 Standard | Payables turnover |
| 69 | fixed_assets | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟢 Standard | Asset turnover |
| 70 | intangible_assets | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟢 Standard | Goodwill analysis |
| 71 | reserves_and_surplus | Balance Sheet | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟢 Standard | Retained earnings |
| 72 | book_value_per_share | Balance Sheet | Decimal (₹) | Screener.in | Scrape | Annual | 🟡 Important | P/B ratio |
| 73 | contingent_liabilities | Balance Sheet | Decimal (₹ Cr) | Annual Report | Scrape | Annual | 🟢 Standard | R10 penalty |
| 74 | operating_cash_flow | Cash Flow | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🔴 Critical | OCF > NI check, FCF, D4 |
| 75 | investing_cash_flow | Cash Flow | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🔴 Critical | CapEx analysis |
| 76 | financing_cash_flow | Cash Flow | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟡 Important | Debt/equity financing |
| 77 | capital_expenditure | Cash Flow | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🔴 Critical | FCF = OCF − CapEx |
| 78 | free_cash_flow | Cash Flow | Decimal (₹ Cr) | Calculated | Internal | Annual | 🔴 Critical | D5, FCF yield, Q9 |
| 79 | dividends_paid | Cash Flow | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟡 Important | Dividend payout, Q4 |
| 80 | debt_repayment | Cash Flow | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟢 Standard | Debt servicing |
| 81 | equity_raised | Cash Flow | Decimal (₹ Cr) | Screener.in | Scrape | Annual | 🟢 Standard | Dilution tracking |
| 82 | roe | Financial Ratios | Decimal (%) | Calculated | Internal | Quarterly | 🔴 Critical | Q1 (>20% 5yr), R3 (<10%) |
| 83 | roa | Financial Ratios | Decimal (%) | Calculated | Internal | Annual | 🟡 Important | Asset efficiency |
| 84 | roic | Financial Ratios | Decimal (%) | Calculated | Internal | Annual | 🟡 Important | Capital efficiency |
| 85 | debt_to_equity | Financial Ratios | Decimal | Calculated | Internal | Quarterly | 🔴 Critical | D8 (>5), R1, Q3 (0) |
| 86 | interest_coverage | Financial Ratios | Decimal | Calculated | Internal | Quarterly | 🔴 Critical | D1 (<2x), R2 (2–3x) |
| 87 | current_ratio | Financial Ratios | Decimal | Calculated | Internal | Annual | 🟡 Important | Liquidity (>1.5) |
| 88 | quick_ratio | Financial Ratios | Decimal | Calculated | Internal | Annual | 🟢 Standard | Short-term liquidity |
| 89 | asset_turnover | Financial Ratios | Decimal | Calculated | Internal | Annual | 🟢 Standard | Efficiency analysis |
| 90 | inventory_turnover | Financial Ratios | Decimal | Calculated | Internal | Annual | 🟢 Standard | Working capital |
| 91 | receivables_turnover | Financial Ratios | Decimal | Calculated | Internal | Annual | 🟢 Standard | Collection efficiency |
| 92 | dividend_payout_ratio | Financial Ratios | Decimal (%) | Calculated | Internal | Annual | 🟡 Important | Q4 (10yr consecutive) |
| 93 | market_cap | Valuation | Decimal (₹ Cr) | Calculated | Internal | Daily | 🔴 Critical | Size, EV calc |
| 94 | enterprise_value | Valuation | Decimal (₹ Cr) | Calculated | Internal | Daily | 🔴 Critical | EV/EBITDA |
| 95 | pe_ratio | Valuation | Decimal | Calculated | Internal | Daily | 🔴 Critical | Valuation, R8 |
| 96 | pe_ratio_forward | Valuation | Decimal | Trendlyne | Scrape | Quarterly | 🔴 Critical | Forward valuation |
| 97 | peg_ratio | Valuation | Decimal | Calculated | Internal | Quarterly | 🔴 Critical | Growth-adjusted val |
| 98 | pb_ratio | Valuation | Decimal | Calculated | Internal | Daily | 🟡 Important | Asset-based val |
| 99 | ps_ratio | Valuation | Decimal | Calculated | Internal | Daily | 🟡 Important | Revenue-based val |
| 100 | ev_to_ebitda | Valuation | Decimal | Calculated | Internal | Quarterly | 🔴 Critical | Valuation scoring |
| 101 | ev_to_sales | Valuation | Decimal | Calculated | Internal | Quarterly | 🟢 Standard | Revenue-based EV |
| 102 | dividend_yield | Valuation | Decimal (%) | Calculated | Internal | Daily | 🟡 Important | Income investing |
| 103 | fcf_yield | Valuation | Decimal (%) | Calculated | Internal | Annual | 🟡 Important | Q9 booster (>5%) |
| 104 | earnings_yield | Valuation | Decimal (%) | Calculated | Internal | Daily | 🟡 Important | Bond yield comparison |
| 105 | sector_avg_pe | Valuation | Decimal | Screener.in | Scrape | Weekly | 🟡 Important | R8 (P/E > 2× sector) |
| 106 | sector_avg_roe | Valuation | Decimal (%) | Screener.in | Scrape | Weekly | 🟡 Important | Sector benchmark |
| 107 | industry_avg_pe | Valuation | Decimal | Screener.in | Scrape | Weekly | 🟢 Standard | Industry comparison |
| 108 | historical_pe_median | Valuation | Decimal | Calculated | Internal | Daily | 🟢 Standard | Historical valuation |
| 109 | sector_performance | Valuation | Decimal (%) | NSE Indices | Download | Daily | 🟡 Important | Sector strength check |
| 110 | promoter_holding | Shareholding | Decimal (%) | BSE Filings | Scrape | Quarterly | 🔴 Critical | Ownership, R4 |
| 111 | promoter_pledging | Shareholding | Decimal (%) | BSE/Trendlyne | Scrape | Quarterly | 🔴 Critical | D7 (>80%), R5 |
| 112 | fii_holding | Shareholding | Decimal (%) | BSE Filings | Scrape | Quarterly | 🔴 Critical | Q6 booster |
| 113 | dii_holding | Shareholding | Decimal (%) | BSE Filings | Scrape | Quarterly | 🟡 Important | Domestic institutional |
| 114 | public_holding | Shareholding | Decimal (%) | BSE Filings | Scrape | Quarterly | 🟡 Important | Retail participation |
| 115 | promoter_holding_change | Shareholding | Decimal (%) | Calculated | Internal | Quarterly | 🟡 Important | R4 (↓>5%), Q5 (↑) |
| 116 | fii_holding_change | Shareholding | Decimal (%) | Calculated | Internal | Quarterly | 🟡 Important | Q6 (↑>2%) |
| 117 | num_shareholders | Shareholding | Integer | BSE Filings | Scrape | Quarterly | 🟢 Standard | Retail breadth |
| 118 | mf_holding | Shareholding | Decimal (%) | BSE Filings | Scrape | Quarterly | 🟢 Standard | MF interest |
| 119 | insurance_holding | Shareholding | Decimal (%) | BSE Filings | Scrape | Quarterly | 🟢 Standard | Insurance interest |
| 120 | dividend_per_share | Corp Actions | Decimal (₹) | BSE/NSE | Scrape | On Event | 🟡 Important | Div yield, Q4 |
| 121 | ex_dividend_date | Corp Actions | Date | BSE/NSE | Scrape | On Event | 🟡 Important | Price adjustment |
| 122 | stock_split_ratio | Corp Actions | String | BSE/NSE | Scrape | On Event | 🟡 Important | Price/shares adj |
| 123 | bonus_ratio | Corp Actions | String | BSE/NSE | Scrape | On Event | 🟡 Important | Shares adjustment |
| 124 | rights_issue_ratio | Corp Actions | String | BSE/NSE | Scrape | On Event | 🟢 Standard | Dilution tracking |
| 125 | buyback_details | Corp Actions | String | BSE/NSE | Scrape | On Event | 🟢 Standard | Capital return |
| 126 | next_earnings_date | Corp Actions | Date | BSE Announce | Scrape | On Event | 🟡 Important | Checklist item |
| 127 | pending_events | Corp Actions | List[Object] | BSE Announce | Scrape | On Event | 🟡 Important | Catalyst calendar |
| 128 | stock_status | Corp Actions | Enum | NSE/BSE | Download | On Event | 🔴 Critical | D6 deal-breaker |
| 129 | sebi_investigation | Corp Actions | Boolean | SEBI/News | Scrape/RSS | On Event | 🔴 Critical | D2 deal-breaker |
| 130 | news_headline | News & Sentiment | String | RSS Feeds | RSS Parse | Real-time | 🟡 Important | News display |
| 131 | news_body_text | News & Sentiment | String | RSS → URL | HTTP Fetch | Real-time | 🟡 Important | Full sentiment |
| 132 | news_source | News & Sentiment | String | RSS Feeds | RSS Parse | Real-time | 🟢 Standard | Source credibility |
| 133 | news_timestamp | News & Sentiment | DateTime | RSS Feeds | RSS Parse | Real-time | 🟡 Important | Recency weight |
| 134 | news_sentiment_score | News & Sentiment | Decimal (−1 to 1) | Calculated | NLP/LLM | Real-time | 🟡 Important | Sentiment scoring |
| 135 | stock_tickers_mentioned | News & Sentiment | List[String] | Calculated | NLP | Real-time | 🟢 Standard | Stock tagging |
| 136 | credit_rating | News & Sentiment | String | Rating Agencies | Scrape | On Change | 🟡 Important | D9 deal-breaker |
| 137 | credit_outlook | News & Sentiment | Enum | Rating Agencies | Scrape | On Change | 🟢 Standard | Credit trend |
| 138 | sma_20 | Technical | Decimal (₹) | pandas-ta | Calculated | Daily | 🟡 Important | Short-term trend |
| 139 | sma_50 | Technical | Decimal (₹) | pandas-ta | Calculated | Daily | 🔴 Critical | Medium trend, checklist |
| 140 | sma_200 | Technical | Decimal (₹) | pandas-ta | Calculated | Daily | 🔴 Critical | Long-term trend |
| 141 | ema_12 | Technical | Decimal (₹) | pandas-ta | Calculated | Daily | 🟡 Important | MACD calculation |
| 142 | ema_26 | Technical | Decimal (₹) | pandas-ta | Calculated | Daily | 🟡 Important | MACD calculation |
| 143 | rsi_14 | Technical | Decimal (0–100) | pandas-ta | Calculated | Daily | 🔴 Critical | Overbought/sold (30–70) |
| 144 | macd | Technical | Decimal | pandas-ta | Calculated | Daily | 🔴 Critical | Momentum scoring |
| 145 | macd_signal | Technical | Decimal | pandas-ta | Calculated | Daily | 🔴 Critical | Signal crossovers |
| 146 | bollinger_upper | Technical | Decimal (₹) | pandas-ta | Calculated | Daily | 🟡 Important | Volatility bands |
| 147 | bollinger_lower | Technical | Decimal (₹) | pandas-ta | Calculated | Daily | 🟡 Important | Volatility bands |
| 148 | atr_14 | Technical | Decimal | pandas-ta | Calculated | Daily | 🟡 Important | Stop-loss calc |
| 149 | adx_14 | Technical | Decimal | pandas-ta | Calculated | Daily | 🟢 Standard | Trend strength |
| 150 | obv | Technical | Integer | pandas-ta | Calculated | Daily | 🟢 Standard | Volume confirmation |
| 151 | support_level | Technical | Decimal (₹) | Custom | Calculated | Daily | 🟡 Important | Stop-loss, checklist |
| 152 | resistance_level | Technical | Decimal (₹) | Custom | Calculated | Daily | 🟡 Important | Target, checklist |
| 153 | moat_assessment | Qualitative | Enum/String | Manual/LLM | Manual/LLM | On Event | 💭 Qualitative | Competitive moat |
| 154 | management_assessment | Qualitative | Enum/String | Manual/LLM | Manual/LLM | On Event | 💭 Qualitative | Management track record |
| 155 | industry_growth_assessment | Qualitative | Enum/String | Manual/LLM | Manual/LLM | On Event | 💭 Qualitative | Industry tailwinds |
| 156 | disruption_risk | Qualitative | Enum/String | Manual/LLM | Manual/LLM | On Event | 💭 Qualitative | Existential disruption |
| 157 | fraud_history | Qualitative | Boolean | Manual/News | Manual | On Event | 💭 Qualitative | No accounting fraud |
| 158 | field_availability | Metadata | Dict[str,Bool] | System | Auto | Continuous | 🔵 Metadata | Confidence: Completeness (40%) |
| 159 | field_last_updated | Metadata | Dict[str,DateTime] | System | Auto | Continuous | 🔵 Metadata | Confidence: Freshness (30%) |
| 160 | multi_source_values | Metadata | Dict[str,Dict] | System | Auto | Continuous | 🔵 Metadata | Confidence: Source Agreement (15%) |

---

## Appendix B: Primary Data Sources Summary

| Source | Data Provided | Fields | Cost |
|--------|--------------|--------|------|
| **Screener.in** | All fundamentals, ratios, 10-year history, peer data | 60+ | Free / ₹4k/yr |
| **NSE Bhavcopy** | Official EOD OHLCV, delivery data, bulk deals | 15 | Free |
| **BSE Filings** | Shareholding, corporate announcements, results | 15 | Free |
| **Trendlyne** | FII/DII changes, pledging trends, forward PE | 8 | Free (limited) |
| **yfinance** | Adjusted close, backup prices | 10 | Free |
| **RSS Feeds** | News from Moneycontrol, ET, BS | 4 | Free |
| **Rating Agencies** | Credit ratings (CRISIL, ICRA, CARE) | 3 | Free |
| **pandas-ta** | All technical indicators (calculated) | 15 | Free (library) |

---

## Appendix C: Complete Calculation Formulas Reference

All 57 internally calculated fields with their exact formulas, dependencies, and computation notes.

### C.1 Derived Price Metrics (11 Fields — Category 3)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 28 | daily_return_pct | `((close - prev_close) / prev_close) x 100` | close (#19), prev_close (#26) | Use adjusted_close for multi-year return series |
| 29 | return_5d_pct | `((close_today - close_5d_ago) / close_5d_ago) x 100` | close (#19), 5 trading days lookback | Skip non-trading days |
| 30 | return_20d_pct | `((close_today - close_20d_ago) / close_20d_ago) x 100` | close (#19), 20 trading days lookback | Approximately 1 calendar month |
| 31 | return_60d_pct | `((close_today - close_60d_ago) / close_60d_ago) x 100` | close (#19), 60 trading days lookback | Approximately 3 calendar months |
| 32 | day_range_pct | `((high - low) / low) x 100` | high (#17), low (#18) | Intraday volatility measure |
| 33 | gap_percentage | `((open - prev_close) / prev_close) x 100` | open (#16), prev_close (#26) | Gap-up: positive; Gap-down: negative |
| 34 | 52_week_high | `MAX(high) over 252 trading days` | high (#17), 252-day window | Rolling maximum |
| 35 | 52_week_low | `MIN(low) over 252 trading days` | low (#18), 252-day window | Rolling minimum |
| 36 | distance_from_52w_high | `((52_week_high - close) / 52_week_high) x 100` | 52_week_high (#34), close (#19) | Always >= 0; 0 means at 52-week high |
| 37 | volume_ratio | `volume / avg_volume_20d` | volume (#21), avg_volume_20d (#38) | >2 indicates unusual volume |
| 38 | avg_volume_20d | `SUM(volume over 20 days) / 20` | volume (#21), 20-day window | Exclude zero-volume (halt) days from average |

### C.2 Income Statement Calculated Fields (7 Fields — Category 4)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 40 | revenue_growth_yoy | `((revenue_current_Q - revenue_same_Q_last_year) / revenue_same_Q_last_year) x 100` | revenue (#39), same-quarter prior year | Compare Q-to-Q (not sequential quarters) |
| 41 | revenue_growth_qoq | `((revenue_current_Q - revenue_previous_Q) / revenue_previous_Q) x 100` | revenue (#39), prior quarter | Sequential quarter growth |
| 45 | gross_margin | `(gross_profit / revenue) x 100` | gross_profit (#44), revenue (#39) | null if gross_profit unavailable |
| 47 | net_profit_margin | `(net_profit / revenue) x 100` | net_profit (#46), revenue (#39) | Can be negative for loss-making firms |
| 49 | eps_growth_yoy | `((eps_current - eps_same_Q_last_year) / ABS(eps_same_Q_last_year)) x 100` | eps (#48), same-quarter prior year | Use ABS in denominator for negative base EPS |
| 53 | ebit | `ebitda - depreciation` | ebitda (#52), depreciation (#51) | OR: operating_profit if EBITDA unavailable |
| 56 | effective_tax_rate | `(tax_expense / (net_profit + tax_expense)) x 100` | tax_expense (#55), net_profit (#46) | Pre-tax profit = net_profit + tax_expense |

### C.3 Balance Sheet Calculated Fields (2 Fields — Category 5)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 63 | net_debt | `total_debt - cash_and_equivalents` | total_debt (#59), cash_and_equivalents (#62) | Negative = net cash position (positive signal) |
| 72 | book_value_per_share | `total_equity / shares_outstanding` | total_equity (#58), shares_outstanding (#11) | Also available scraped from Screener.in |

### C.4 Cash Flow Calculated Field (1 Field — Category 6)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 78 | free_cash_flow | `operating_cash_flow - capital_expenditure` | operating_cash_flow (#74), capital_expenditure (#77) | CapEx stored as positive; subtract from OCF |

### C.5 Financial Ratios (11 Fields — Category 7)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 82 | roe | `(net_profit / total_equity) x 100` | net_profit (#46), total_equity (#58) | Use TTM net_profit for quarterly updates; null if equity <= 0 |
| 83 | roa | `(net_profit / total_assets) x 100` | net_profit (#46), total_assets (#57) | Annual calculation |
| 84 | roic | `(NOPAT / invested_capital) x 100` where `NOPAT = operating_profit x (1 - effective_tax_rate/100)` and `invested_capital = total_equity + total_debt - cash_and_equivalents` | operating_profit (#42), effective_tax_rate (#56), total_equity (#58), total_debt (#59), cash_and_equivalents (#62) | Measures return on all invested capital |
| 85 | debt_to_equity | `total_debt / total_equity` | total_debt (#59), total_equity (#58) | null if equity <= 0; negative equity = high risk flag |
| 86 | interest_coverage | `ebit / interest_expense` | ebit (#53), interest_expense (#50) | null if interest_expense = 0; <2 = D1 deal-breaker |
| 87 | current_ratio | `current_assets / current_liabilities` | current_assets (#64), current_liabilities (#65) | null if current_liabilities = 0 |
| 88 | quick_ratio | `(current_assets - inventory) / current_liabilities` | current_assets (#64), inventory (#66), current_liabilities (#65) | More conservative than current ratio |
| 89 | asset_turnover | `revenue / total_assets` | revenue (#39, TTM), total_assets (#57) | Efficiency of asset utilization |
| 90 | inventory_turnover | `cogs / average_inventory` where `cogs = revenue - gross_profit` | revenue (#39), gross_profit (#44), inventory (#66, avg of 2 periods) | N/A for service/banking companies |
| 91 | receivables_turnover | `revenue / average_receivables` | revenue (#39, TTM), receivables (#67, avg of 2 periods) | Higher = faster collection |
| 92 | dividend_payout_ratio | `(dividends_paid / net_profit) x 100` | dividends_paid (#79), net_profit (#46) | null if net_profit <= 0; >100% = paying from reserves |

### C.6 Valuation Metrics Calculated Fields (13 Fields — Category 8)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 93 | market_cap | `close x shares_outstanding` | close (#19), shares_outstanding (#11) | Updated daily; stored in Crores |
| 94 | enterprise_value | `market_cap + net_debt` | market_cap (#93), net_debt (#63) | EV = Market Cap + Total Debt - Cash |
| 95 | pe_ratio | `close / eps_ttm` | close (#19), eps (#48, TTM sum of 4 quarters) | null if EPS <= 0; >500 flagged |
| 97 | peg_ratio | `pe_ratio / eps_growth_yoy` | pe_ratio (#95), eps_growth_yoy (#49) | null if growth = 0; <1 = undervalued |
| 98 | pb_ratio | `close / book_value_per_share` | close (#19), book_value_per_share (#72) | null if BVPS <= 0 |
| 99 | ps_ratio | `market_cap / revenue_ttm` | market_cap (#93), revenue (#39, TTM) | null if revenue <= 0 |
| 100 | ev_to_ebitda | `enterprise_value / ebitda_ttm` | enterprise_value (#94), ebitda (#52, TTM) | null if EBITDA <= 0 |
| 101 | ev_to_sales | `enterprise_value / revenue_ttm` | enterprise_value (#94), revenue (#39, TTM) | null if revenue <= 0 |
| 102 | dividend_yield | `(annual_dividend_per_share / close) x 100` | dividend_per_share (#120), close (#19) | 0 if no dividends (not null) |
| 103 | fcf_yield | `(free_cash_flow / market_cap) x 100` | free_cash_flow (#78), market_cap (#93) | Can be negative; >5% = Q9 booster |
| 104 | earnings_yield | `(eps_ttm / close) x 100` | eps (#48, TTM), close (#19) | Inverse of P/E; compare to bond yields |
| 108 | historical_pe_median | `MEDIAN(pe_ratio) over 5 years (1260 trading days)` | pe_ratio (#95), 5-year history | Exclude null/negative PE periods |
| 8 | market_cap_category | `IF market_cap >= 20000 Cr THEN 'Large Cap' ELIF >= 5000 Cr THEN 'Mid Cap' ELIF >= 500 Cr THEN 'Small Cap' ELSE 'Micro Cap'` | market_cap (#93) | Thresholds per SEBI classification |

### C.7 Shareholding Calculated Fields (2 Fields — Category 9)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 115 | promoter_holding_change | `promoter_holding_current_Q - promoter_holding_previous_Q` | promoter_holding (#110), prior quarter value | Positive = increase; negative = R4 if >5% decline |
| 116 | fii_holding_change | `fii_holding_current_Q - fii_holding_previous_Q` | fii_holding (#112), prior quarter value | Positive >2% = Q6 booster |

### C.8 Technical Indicators (15 Fields — Category 12)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 138 | sma_20 | `SUM(close over 20 days) / 20` | close (#19), 20-day window | Short-term trend; Bollinger middle band |
| 139 | sma_50 | `SUM(close over 50 days) / 50` | close (#19), 50-day window | Medium-term trend reference |
| 140 | sma_200 | `SUM(close over 200 days) / 200` | close (#19), 200-day window | Long-term trend; golden/death cross signal |
| 141 | ema_12 | `EMA(close, span=12)` where `multiplier = 2/(12+1)` and `EMA_today = (close - EMA_yesterday) x multiplier + EMA_yesterday` | close (#19), prior EMA values | Fast EMA for MACD |
| 142 | ema_26 | `EMA(close, span=26)` | close (#19), prior EMA values | Slow EMA for MACD |
| 143 | rsi_14 | `100 - (100 / (1 + RS))` where `RS = avg_gain_14 / avg_loss_14` | close (#19), 14-period gains and losses | Range 0-100; <30 oversold, >70 overbought |
| 144 | macd | `ema_12 - ema_26` | ema_12 (#141), ema_26 (#142) | Positive = bullish momentum |
| 145 | macd_signal | `EMA(macd, span=9)` | macd (#144), 9-period EMA | MACD crossing above signal = buy signal |
| 146 | bollinger_upper | `sma_20 + (2 x StdDev(close, 20))` | sma_20 (#138), close (#19) standard deviation | Upper volatility band |
| 147 | bollinger_lower | `sma_20 - (2 x StdDev(close, 20))` | sma_20 (#138), close (#19) standard deviation | Lower volatility band |
| 148 | atr_14 | `EMA(true_range, span=14)` where `true_range = MAX(high-low, ABS(high-prev_close), ABS(low-prev_close))` | high (#17), low (#18), prev_close (#26) | Volatility measure for stop-loss sizing |
| 149 | adx_14 | `EMA(ABS(+DI - -DI) / (+DI + -DI) x 100, 14)` | high, low, close, 14-period directional movement | >25 = strong trend; <20 = weak/no trend |
| 150 | obv | `OBV_prev + (volume if close > prev_close, -volume if close < prev_close, 0 if equal)` | volume (#21), close (#19), prev_close (#26) | Cumulative; confirms price trends |
| 151 | support_level | Custom pivot low: `lowest of recent significant lows within 20-period lookback` | low (#18), pivot calculation | Implementation-specific; use local minima |
| 152 | resistance_level | Custom pivot high: `highest of recent significant highs within 20-period lookback` | high (#17), pivot calculation | Implementation-specific; use local maxima |

### C.9 Metadata Fields (3 Fields — Category 13)

| # | Field | Formula | Dependencies | Notes |
|---|-------|---------|-------------|-------|
| 158 | field_availability | `FOR EACH field IN 160_fields: {field_name: is_populated(stock, field)}` | All 160 fields per stock | Auto-updated after every extraction cycle |
| 159 | field_last_updated | `FOR EACH field IN 160_fields: {field_name: last_write_timestamp(stock, field)}` | Write timestamps for all fields | Auto-updated on every database write |
| 160 | multi_source_values | `FOR EACH multi_source_field: {field_name: {source1: value1, source2: value2, ...}}` | All multi-source field extractions | Used for cross-verification and confidence scoring |

### C.10 Confidence Score Formula

```
Data Confidence Score (0-100) =
    (Data Completeness x 0.40)   -- % of 160 fields populated
  + (Data Freshness x 0.30)      -- % of fields within staleness threshold
  + (Source Agreement x 0.15)    -- % of multi-source fields in agreement (within 2%)
  + (Priority Coverage x 0.15)   -- Weighted completeness favoring Critical/Important fields

Where Priority Coverage =
    (Critical fields filled / 58) x 0.50
  + (Important fields filled / 52) x 0.30
  + (Standard fields filled / 35) x 0.15
  + (Optional+Qual fields filled / 12) x 0.05
```

---

## Appendix D: Validation Rules Quick Reference

Complete validation rules organized by severity level for rapid implementation reference.

### D.1 Hard Rejection Rules (Data Rejected if Failed)

| Rule ID | Category | Validation | Action on Failure |
|---------|----------|-----------|-------------------|
| V-HR-01 | Price | `low <= open <= high AND low <= close <= high` | Reject entire day's price record |
| V-HR-02 | Price | All prices (`open`, `high`, `low`, `close`) > 0 | Reject record |
| V-HR-03 | Master | `symbol` non-empty, matches `[A-Z0-9&-]+` | Reject stock entry |
| V-HR-04 | Master | `isin` matches `INE[0-9A-Z]{9}` (12 chars) | Reject; use backup source |
| V-HR-05 | Volume | `volume` >= 0 | Reject record |
| V-HR-06 | Shareholding | All holding percentages 0-100% | Reject filing data |
| V-HR-07 | Technical | `rsi_14` in range 0-100 | Recalculate; reject if still invalid |
| V-HR-08 | Technical | `bollinger_upper` > `sma_20` > `bollinger_lower` | Recalculate from source data |
| V-HR-09 | News | `news_sentiment_score` in range [-1, +1] | Reject sentiment; re-run NLP |
| V-HR-10 | News | `news_timestamp` not in the future | Reject article |
| V-HR-11 | Cash Flow | `free_cash_flow` = `operating_cash_flow` - `capital_expenditure` (exact) | Recalculate; flag inconsistency |

### D.2 Warning Rules (Data Accepted but Flagged)

| Rule ID | Category | Validation | Flag Type |
|---------|----------|-----------|-----------|
| V-WN-01 | Price | `daily_return_pct` within +/-20% | EXTREME_MOVE (circuit limit check) |
| V-WN-02 | Price | `daily_return_pct` within +/-50% | SUSPICIOUS (possible data error) |
| V-WN-03 | Price | `gap_percentage` > 20% | LARGE_GAP |
| V-WN-04 | Price | `volume_ratio` > 10 | VOLUME_ANOMALY |
| V-WN-05 | Income | `revenue` < 0 | NEGATIVE_REVENUE (extremely rare) |
| V-WN-06 | Income | `effective_tax_rate` outside 0-50% | TAX_ANOMALY |
| V-WN-07 | Income | `operating_margin` outside -100% to +100% | MARGIN_EXTREME |
| V-WN-08 | Balance | `current_ratio` < 0.1 or > 50 | SUSPICIOUS_RATIO |
| V-WN-09 | Ratios | `roe` > 100% or < -100% | ROE_ANOMALOUS |
| V-WN-10 | Ratios | `debt_to_equity` > 10 | HIGHLY_LEVERAGED |
| V-WN-11 | Ratios | `interest_coverage` < 0 | NEGATIVE_COVERAGE |
| V-WN-12 | Valuation | `pe_ratio` > 500 | EXTREME_PE |
| V-WN-13 | Valuation | `pe_ratio` < 0 | NEGATIVE_PE (store as null) |
| V-WN-14 | Balance | `total_assets` != approx `total_equity + total_liabilities` (>5% divergence) | BALANCE_MISMATCH |
| V-WN-15 | Technical | `rsi_14` < 10 or > 90 | RSI_EXTREME |

### D.3 Consistency Rules (Cross-Field Validation)

| Rule ID | Validation | Fields Involved | Tolerance |
|---------|-----------|----------------|-----------|
| V-CR-01 | `52_week_high >= 52_week_low` | #34, #35 | Exact |
| V-CR-02 | `vwap` between `low` and `high` | #27, #17, #18 | Exact |
| V-CR-03 | `delivery_percentage` 0-100% | #23 | Exact |
| V-CR-04 | `market_cap` = `close x shares_outstanding` | #93, #19, #11 | Within 1% rounding |
| V-CR-05 | Sum of holdings approx 100% | #110+#112+#113+#114 | Within +/-2% |
| V-CR-06 | `promoter_pledging` <= `promoter_holding` | #111, #110 | Exact |
| V-CR-07 | `dividend_yield` >= 0 | #102 | Exact (0 if no dividends) |
| V-CR-08 | `sma_200` > 0 | #140 | Exact |
| V-CR-09 | `total_debt` >= 0 | #59 | Exact |
| V-CR-10 | Temporal ordering: new quarter > previous quarter | Period dates | Exact |

### D.4 Multi-Source Agreement Rules

| Rule ID | Field(s) | Sources | Tolerance | Action on Disagreement |
|---------|----------|---------|-----------|----------------------|
| V-MS-01 | close price | NSE Bhavcopy, yfinance, BSE | 0.5% | Use NSE Bhavcopy as canonical |
| V-MS-02 | market_cap | Calculated, Screener.in | 2% | Use calculated as canonical |
| V-MS-03 | pe_ratio | Calculated, Screener.in, Trendlyne | 5% | Use calculated as canonical |
| V-MS-04 | promoter_holding | BSE Filings, Trendlyne, Screener.in | 0.5% | Use BSE Filings as canonical |
| V-MS-05 | eps | Screener.in, Calculated, Trendlyne | 2% | Use Screener.in as canonical |
| V-MS-06 | net_profit | Screener.in, BSE Results, Trendlyne | 2% | Use Screener.in as canonical |
| V-MS-07 | dividend_yield | Calculated, Screener.in, Trendlyne | 5% | Use calculated as canonical |
| V-MS-08 | sector/industry | Screener.in, Trendlyne, BSE | Exact match | Use Screener.in as canonical |

**Source Preference Hierarchy (descending priority):**
1. Calculated (from verified inputs)
2. Official Source (NSE/BSE filings)
3. Screener.in
4. Trendlyne
5. yfinance

### D.5 Staleness Thresholds

| Data Frequency | Stale Warning | Critical Alert | Auto-Flag |
|---------------|--------------|----------------|-----------|
| Daily (OHLCV, technicals, daily valuations) | > 2 trading days | > 5 trading days | STALE_DAILY |
| Weekly (peer averages, sector data) | > 10 calendar days | > 21 calendar days | STALE_WEEKLY |
| Quarterly (financials, shareholding, ratios) | > 60 days from quarter end | > 90 days from quarter end | STALE_QUARTERLY |
| Annual (balance sheet, cash flow) | > 6 months from FY end | > 12 months from FY end | STALE_ANNUAL |
| Real-time (news, sentiment) | > 1 hour | > 6 hours | STALE_REALTIME |
| On Event (corp actions, master data) | N/A | N/A | Checked on access |

### D.6 Deal-Breaker Threshold Summary (D1-D10)

These thresholds trigger automatic STRONG AVOID verdict in the scoring engine. The extraction system must guarantee these fields are available, fresh, and accurate.

| Code | Field(s) | Threshold | Scoring Impact |
|------|----------|-----------|---------------|
| D1 | interest_coverage (#86) | < 2x | Cap scores at 35; verdict = STRONG AVOID |
| D2 | sebi_investigation (#129) | = true | Cap scores at 35; verdict = STRONG AVOID |
| D3 | revenue (#39), revenue_growth_yoy (#40) | Negative YoY for 3+ quarters | Cap scores at 35; verdict = STRONG AVOID |
| D4 | operating_cash_flow (#74) | < 0 for 2+ years | Cap scores at 35; verdict = STRONG AVOID |
| D5 | free_cash_flow (#78) | < 0 for 3+ years | Cap scores at 35; verdict = STRONG AVOID |
| D6 | stock_status (#128) | Not ACTIVE | Cap scores at 35; verdict = STRONG AVOID |
| D7 | promoter_pledging (#111) | > 80% | Cap scores at 35; verdict = STRONG AVOID |
| D8 | debt_to_equity (#85) | > 5 | Cap scores at 35; verdict = STRONG AVOID |
| D9 | credit_rating (#136) | Below investment grade | Cap scores at 35; verdict = STRONG AVOID |
| D10 | volume (#21), avg_volume_20d (#38) | Avg volume < 50,000 | Cap scores at 35; verdict = STRONG AVOID |

### D.7 Red Flag Penalty Summary (R1-R10)

| Code | Field(s) | Trigger | Long-Term Penalty | Short-Term Penalty |
|------|----------|---------|-------------------|-------------------|
| R1 | debt_to_equity (#85) | > 1.5 | -15 | -10 |
| R2 | interest_coverage (#86) | 2-3x range | -10 | -5 |
| R3 | roe (#82) | < 10% | -12 | -5 |
| R4 | promoter_holding (#110), promoter_holding_change (#115) | Decline > 5% | -10 | -15 |
| R5 | promoter_pledging (#111) | > 0% | -10 | -15 |
| R6 | distance_from_52w_high (#36) | > 30% | -5 | -10 |
| R7 | operating_margin (#43) | Declining trend | -8 | -5 |
| R8 | pe_ratio (#95), sector_avg_pe (#105) | P/E > 2x sector avg | -10 | -5 |
| R9 | delivery_percentage (#23) | < 30% consistently | -5 | -8 |
| R10 | contingent_liabilities (#73) | > 10% of net worth | -8 | -5 |

### D.8 Quality Booster Summary (Q1-Q9)

| Code | Field(s) | Trigger | Long-Term Boost | Short-Term Boost | Cap |
|------|----------|---------|----------------|-----------------|-----|
| Q1 | roe (#82) | > 20% for 5 years | +15 | +5 | Combined max +30 |
| Q2 | revenue_growth_yoy (#40) | > 15% | +12 | +5 | Combined max +30 |
| Q3 | debt_to_equity (#85) | = 0 (zero debt) | +10 | +5 | Combined max +30 |
| Q4 | dividends_paid (#79), dividend_payout_ratio (#92) | 10+ consecutive years | +8 | +3 | Combined max +30 |
| Q5 | promoter_holding_change (#115) | Increasing | +5 | +8 | Combined max +30 |
| Q6 | fii_holding (#112), fii_holding_change (#116) | Increase > 2% | +5 | +8 | Combined max +30 |
| Q7 | operating_margin (#43) | > 25% | +10 | +5 | Combined max +30 |
| Q8 | 52_week_high (#34), distance_from_52w_high (#36) | Close to 52-week high | +5 | +10 | Combined max +30 |
| Q9 | fcf_yield (#103) | > 5% | +8 | +5 | Combined max +30 |

**Total Quality Booster cap: +30 points maximum** (sum of all triggered boosters, capped).

---

*End of Document — StockPulse Data Extraction System Blueprint v2.0*

