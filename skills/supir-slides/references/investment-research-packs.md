# Investment Research Packs

Use this reference with `data-acquisition.md` for finance, investment research,
company, industry, macro, market, fund product, and institutional roadshow
decks. A research pack is the minimum evidence plan before page planning. It
does not force every deck to use every source; unavailable items must be
recorded in `needs_source_registry.jsonl` and `data_audit.md`.

Always maintain the workpaper ledger described in
`research-workpaper-archive.md`.

## Tool Routing Rules

Use these hard routes before choosing a page outline:

| Need | Route |
| --- | --- |
| A-share company financials, A-share quotes, A-share index, China macro standard time series | `search_cn_marketdata` |
| HK/US/Japan/Korea/Taiwan and other overseas stocks; global indices; ETFs/funds; FX; crypto; commodities; Treasury rates; overseas quote/price/history/financials/valuation/analyst data | `search_global_data` |
| Single or multi-company financial snapshot with valuation, three statements, and estimates | `quick_fetch_stock_financials` |
| Screening, ranking, joins, computed ratios, peer set construction, cross-market calculations | delegate to `data_analyst` |
| Exact report/announcement/minutes retrieval by institution, ticker, date, keyword, or full coverage | delegate to `doc_searcher` |
| Semantic research scan, analyst views, commentary, thematic framing | `search_paipai` |
| Public policy, regulatory, official website, or news outside PaiWork professional databases | `search_web` then `fetch_web` |

Fallback rules:

- If direct `search_cn_marketdata` or `search_global_data` attempts fail twice
  or return incomplete data for a computed/screening need, delegate to
  `data_analyst`.
- If `search_paipai` is not enough to support a phrase such as "all recent",
  "market consensus", "latest reports", or "since date X", delegate to
  `doc_searcher`.
- Record every material tool call in `tool_run_registry.jsonl`, including empty
  results and fallback decisions.

## `search_global_data` Details

Use `search_global_data` for standardized overseas/global structured data.
Before calling it directly in PaiWork, read the `search-global-data` skill if
the runtime requires tool-specific skill loading.

Coverage includes:

- overseas stocks including US, HK, Japan, Korea, Taiwan, and ADRs
- global indices, ETFs, mutual funds, FX, crypto, commodities, Treasury rates
- real-time or latest quote, pre-market/after-hours where requested, historical
  daily/minute prices, financial statements, ratios, key metrics, valuation,
  analyst ratings and target prices, earnings calendar, dividends, splits, ETF
  holdings, SEC filing metadata, 13F summaries, insider and congressional
  trading summaries

Query rules:

- Use one clear English natural-language query per tool call.
- State object, metric/event, period/timeframe, market/asset class, and
  statement/ratio/holding scope where relevant.
- Split quote, financials, analyst ratings, target price, ETF holdings, and news
  into separate calls when the request spans multiple data domains.
- For annual financials, say `annual` or `fiscal year`; for quarterly, say
  `quarterly` or `fiscal quarter`.
- For crypto, use fiat pairs by default, e.g. `BTCUSD` or `ETHUSD`.

Do not use it as the primary route for A-share data, China macro mainline,
SEC filing original text or high-granularity XBRL, HKEX announcement originals,
HK local specialty disclosures, or long-form research interpretation.

## Company Deep-Dive Pack

Use for single-company investment overview, earnings review, valuation review,
company roadshow support, or investment committee discussion.

Minimum evidence plan:

- Target company identity: ticker, market, listing venue, fiscal year, sector.
- Financial snapshot: revenue, profit, margins, cash flow, balance sheet,
  valuation, and estimates via `quick_fetch_stock_financials` or structured data.
- Historical series: at least 3 years or 8 quarters when available.
- Price and valuation series: A-share/domestic via `search_cn_marketdata`,
  overseas/global via `search_global_data`.
- Announcements/filings: use `doc_searcher` for comprehensive coverage when the
  deck depends on recent disclosures.
- Management commentary: roadshow, earnings call, or meeting minutes via
  `search_paipai` or `doc_searcher`.
- Analyst debate: recent reports/views via `search_paipai`; use `doc_searcher`
  for "all recent reports" or institution/date filters.
- Peer comparison: use `quick_fetch_stock_financials` for quick peer snapshots;
  delegate to `data_analyst` for constructed peer sets, ranking, ratios, or
  cross-market comparisons.

Expected ledger outputs:

- `D001_target_financials`
- `D002_price_valuation_timeseries`
- `D003_peer_valuation`
- `C001...` core thesis, evidence, and risks
- `F001...` chart specs and key numbers
- `page_evidence_registry.jsonl` for every main-deck page

## Industry / Theme Pack

Use for sector research, thematic investment decks, industry chain maps, supply
and demand studies, or policy-driven sector reviews.

Minimum evidence plan:

- Define the investable universe and industry chain segments.
- Collect industry research and thematic views via `search_paipai`.
- Use `doc_searcher` for precise retrieval of reports, policies, meeting
  minutes, or company announcements when the outline depends on a document set.
- Pull structured indicators with `search_cn_marketdata` for China/domestic
  indicators and `search_global_data` for overseas market prices, global
  indices, commodities, FX, ETFs, and overseas companies.
- Delegate to `data_analyst` for company screens, exposure tables, ranking,
  factor grouping, joins, and computed metrics.
- Use public web tools only for official policy, regulator, overseas public
  news, or data outside PaiWork professional databases.

Expected ledger outputs:

- industry driver sources and limitations
- segment/company exposure dataset when available
- supply/demand/price/policy datasets or `Needs-Source` records
- at least one counter-evidence or disconfirming-signal claim for main thesis

## Macro / Market Strategy Pack

Use for macro strategy, cross-asset, market dashboard, allocation, risk review,
or monitoring decks.

Minimum evidence plan:

- Domestic macro and A-share market indicators: `search_cn_marketdata`.
- Overseas market variables: `search_global_data` for global indices, ETFs, FX,
  commodities, crypto, Treasury rates, and overseas market history.
- Complex cross-asset calculations, rankings, rolling correlations, or screens:
  delegate to `data_analyst`.
- Policy/regulatory/news events outside professional databases: public web
  tools, with source metadata.
- Qualitative market debate and strategist views: `search_paipai`; use
  `doc_searcher` for precise date/institution coverage.

Expected ledger outputs:

- indicator datasets with unit, frequency, latest period, and freshness
- chart specs for every dashboard or strategy figure
- scenario/monitoring claims with assumptions and disconfirming indicators

## Overseas Company / Cross-Market Pack

Use when the deck involves US/HK/global companies, ADRs, global peers, overseas
indices, ETFs, FX, commodities, crypto, SEC metadata, or 13F summaries.

Minimum evidence plan:

- Use `search_global_data` for standardized quote, historical price,
  financials, valuation, analyst ratings, target prices, ETF holdings, and
  global asset data.
- Use dedicated filing or announcement routes for official SEC filing text,
  detailed XBRL, HKEX announcement originals, or high-audit disclosure extracts;
  do not rely on `search_global_data` for those original-text needs.
- Use `data_analyst` for cross-market peer construction, currency normalization,
  ranking, and calculated ratios.
- Use `search_paipai`, `doc_searcher`, or public web tools for qualitative
  research, management comments, and policy/news context as appropriate.

Expected ledger outputs:

- raw `search_global_data` outputs under `data/raw/Rxxx_search_global_data/`
- normalized datasets with currency/unit policies
- visible slide source labels using provider names only
- limitations when data are quick standardized snapshots rather than official
  filing originals

## Fund Product / Institutional Roadshow Pack

Use for mutual fund product launch, channel education, institutional roadshow,
strategy sales support, or client-facing market materials.

Minimum evidence plan:

- Market environment: relevant indices, rates, macro, sector performance, and
  risk factors via structured tools.
- Product or strategy exposure: target sectors, holdings, factor style, or
  representative companies when provided by the user or source material.
- Comparable market or peer evidence: use structured data and `data_analyst`
  where comparison is material.
- Qualitative positioning and investor concerns: `search_paipai` /
  `doc_searcher` for current debates and risk factors.
- Compliance posture: convert promotional or action language into scenario,
  allocation context, monitoring, valuation, or risk language.

Expected ledger outputs:

- source and dataset records for all market environment charts
- assumptions and risk claims for product positioning pages
- `Needs-Source` records for unsupported product-specific holdings or claims

