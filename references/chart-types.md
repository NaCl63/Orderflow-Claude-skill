# Chart types and platform conventions

For each format: what data it shows, how it is drawn, the settings that change it, how to read it,
and the usual mistakes. **Colour never tells you the side on its own.** Establish the legend or
the platform's documented default first (see the platform table at the end).

## Traded volume (what already executed)

| Format | Data | Drawn as | Settings that change it | Read it as | Common errors |
|---|---|---|---|---|---|
| **Bid × Ask footprint** (Split, Cluster, Ladder) | Aggressive sells and aggressive buys per price row per bar | Two numbers per row ("12 x 45"), or two bars | Row size (ticks per row), auto-merge on zoom, units (coin/USD), decimals on/off, colour scheme, value threshold | Left/right = the platform's sides; delta per row = buy − sell | Reading columns backwards; assuming green = buy; comparing rounded whole-coin numbers as exact; rows merged by auto-scale |
| **Delta footprint** | One number per row = buy − sell | Single signed column, coloured by sign | Same as above | Net aggressor per row only | Treating it as volume; can't recover buy and sell separately |
| **Total (volume) footprint** | sell + buy per row | One column | Same | Where activity happened, not who initiated it | Inferring direction from it |
| **Imbalance highlights** | Diagonal ratio: buy(P) vs sell(P − 1 row), sell(P) vs buy(P + 1 row) | Coloured cells, side lines or text colour | Ratio (often 3 = 300%), minimum/threshold, **zero-cell handling**, stack length | One side traded ≥ ratio × the other diagonally | Recomputing horizontally (buy(P) vs sell(P)) when the platform is diagonal; zero-cell rule differs by platform |
| **Stacked imbalances** | ≥ N consecutive same-side imbalances (N often 3) | Shaded band or zone, sometimes extended | Stack length, extension | One-sided sweeping through several rows in that bar | Calling a zone "support" without a test (`setups.md` card 2) |
| **Bar statistics** | Bar volume, delta, delta %, **CVD** | Rows under or over candles | Which badges are on; CVD anchor | Delta = this bar only. CVD = running sum of delta from an anchor | Confusing bar delta with CVD; not knowing the CVD anchor |
| **Bar POC** | Row with the most volume in one bar | Outlined row or line | Tie rule, row size | Where that bar did most business | Confusing it with session or composite POC |
| **Volume profile** (session, composite, visible range, fixed range) | Volume by price over a period | Horizontal histogram; POC, VAH, VAL lines; HVN/LVN by shape | Period/anchor, row size, value-area % (often 70), split vs total | POC = most volume; VA = band around POC holding X%; HVN/LVN = local peaks/troughs | Mixing profiles of different periods; reading VA% as fixed; LVN/HVN as tested levels (they're descriptive) |
| **Candles + delta + CVD panels** | OHLC; per-bar delta (histogram); CVD (line) | Three panes | CVD anchor (session, day, visible range, continuous), venue aggregation | A histogram = per-bar delta; a line = cumulative. CVD changes by exactly each bar's delta | Reading the CVD level as meaningful without its anchor; divergence claims that depend on the anchor |
| **VWAP / anchored VWAP** | Volume-weighted average price from an anchor | Line, often with bands | Anchor (session, event, swing), band method (SD or %) | Average traded price since the anchor; execution benchmark | Unknown anchor; bands as support/resistance without a test |
| **Range / renko / volume bars** | Bars closed by price range or volume, not time | Equal-size boxes | Range or brick size | Time is irregular: bar count ≠ time | Applying time-bar thresholds; treating gaps in time as gaps in data |

## Resting liquidity (orders waiting, not traded)

| Format | Data | Drawn as | Settings | Read it as | Common errors |
|---|---|---|---|---|---|
| **DOM / order book ladder** | Current displayed size per price (bids below, asks above) | Ladder of sizes, sometimes with traded volume and changes | Depth levels, aggregation, venue(s) | Snapshot of what is displayed now | Treating displayed size as committed (it can be pulled or spoofed); confusing DOM size with traded volume |
| **Order book delta** | Change in resting size (adds − cancels) | Signed bars per level | Window | Where liquidity was added or removed | Calling removals "absorption" or "spoofing" (intent isn't visible) |
| **Liquidity heatmap** | Resting size per price over time | Colour intensity behind candles | Colour scale/clipping, aggregation, venue(s), snapshot interval | Where large resting orders sat and for how long | Hidden and iceberg size is invisible; snapshots miss refills; colour scale changes "large" |

## Derivatives panels

| Format | Data | Read it as | Common errors |
|---|---|---|---|
| **Open interest** | Open contracts (coin or USD), per venue or aggregated | Positions opened (up) or closed (down), net. Each contract has a long and a short | "Rising OI = longs" (it's both sides; see the table in `btc.md`); USD OI moves with price |
| **Funding** | Periodic payment between longs and shorts | Positioning cost, not timing | Treating extremes as a reversal signal (untested here) |
| **Liquidations** | Forced closes (side, size) | Forced aggressive flow | Venue coverage is partial; markers ≠ all liquidations |
| **Basis** | Perp or futures minus spot | Leverage demand vs spot | Mixing venues or quote currencies |
| **Liquidation / TP-SL heatmaps** | **Modelled** levels where positions would be liquidated or exit | An estimate, not observed orders | Reading a model output as real resting liquidity |

## Multi-chart layouts
Identify each pane separately (chart type, venue, timeframe, anchor). Panes often differ in
venue (aggregated vs one exchange), timeframe and time zone. Never carry a setting from one pane to another.

## Platform conventions (verified only where a source is given)

| Platform | Footprint sides | Defaults that matter for reading | Source (checked 2026-10-12) |
|---|---|---|---|
| **OpenMarket** | Left = bid side (sellers hit the bid); right = ask side (buyers lifted the ask). Delta = ask − bid | Unit **Coin**. **Show Decimals off**: BTC values rounded to whole coins. **Auto Scale Bars on** (merges rows when zoomed out). Ticks per bar 1 (1m), 15 (1h), 50 (1d); BTCUSDT perp rows: the row size is **not** always Ticks per bar × $5. Rows of $9, $15, $30 and $50 have been seen with the same settings on different dates, and $50 rows whose edges are snapped to a $3 price grid (so a row edge can sit a few dollars off a round number). Read the row size from the image (row spacing against the price axis), not from the setting. Imbalance **off** by default; when on: ratio 3, diagonal, **Skip Zero Values on** (a print against an empty cell is NOT an imbalance), stacks of 3. POC outlined; VA 70%. Modes: Split, Delta, Total, Cluster, Imbalance Only, Ladder. Stats rows (Volume, Buy, Sell, Delta, Delta %, Cum Delta) off by default | openmarket.xyz/learn/order-flow/footprint.md; …/footprint/settings-reference.md. **The live UI differed from the docs (observed 2026-10-12):** the Advanced tab has **Volume decimals (Auto / fixed)** instead of Show Decimals, **Hide Zeros** (off = zeros print as 0), Scale & Grading, Dynamic Candle Width, Auto Scale Bars; extra tabs Filters, Visibility, Price marker. Skip Zero Values has been seen **off** on a live chart (the docs say the default is on), so don't assume either. Ask for these settings. Real screenshots also showed: imbalance boxes can hide a cell's first digit (`179.331` looks like `79.331`); price labels can sit on top of the stats box; CVD starts at the first loaded bar |
| **TradingView** (Volume footprint chart type) | "Seller volume to the left, buyer volume to the right" (Buy and Sell type) | Types: Buy and Sell, Delta, Total, Ladder. Row size **Auto = 0.2 × normalized ATR** by default, or Manual ticks per row. Imbalance 300%, diagonal; buy imbalance line drawn to the **right** of the level, sell to the **left**. Built from lower-interval data (1 tick on professional plans, otherwise 1 s / 1 m), so totals can differ from tick data. Repaints in real time | tradingview.com/support/solutions/43000726164 |
| **ExoCharts** | **Not verified**: no documentation found | Ask for the legend or settings | — |
| **ATAS** | Not verified from its own docs | A search summary says the default Bid×Ask imbalance is 150% (not opened) | atas.net (search result only) |

The bundled `scripts/check_screenshot.py` uses the Binance convention: `buy` = taker buy (ask),
`sell` = taker sell (bid). Platforms differ on whether a print against an empty diagonal cell is an
imbalance (OpenMarket's documented default skips those), so imbalance counts can differ between
platforms for the same bar.
