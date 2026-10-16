# Reading a chart screenshot

A picture is the weakest input: small numbers get misread, layouts differ by platform, and the
settings that change every number are often not visible. Follow the protocol in order. Formats
and platform defaults: `chart-types.md`. In the author's blind check (2026-10-14) readers following
this protocol transcribed 5,712/5,712 cells correctly on 24 OpenMarket BTC screenshots and 0.999 on
deliberately hard synthetic charts. The protocol, not the reader, is what made that possible.

## Hard rules
- **Never invent a value.** Unreadable means `null`, listed as unreadable, and a request for a zoom
  if it matters.
- **Never map a side from colour alone.** Establish the columns in this order: (1) a legend or
  column header in the image; (2) a printed delta: bar or row Δ = buy − sell, so check which
  column ordering reproduces it; (3) the platform's *documented* default, only if the platform is
  identifiable (`chart-types.md`); otherwise **unknown + ask**. State which basis you used.
- **Keep apart:** traded volume (footprint, profile) vs resting liquidity (DOM, heatmap); bar delta
  vs CVD (and the CVD anchor); bar POC vs session or composite POC; observed vs modelled
  (liquidation heatmaps).
- **No absorption call without price response.** High volume alone is not absorption. Absorption
  also needs price failing to move through the level, and even then it is an *interpretation*:
  passive refill and liquidity withdrawal look the same in a footprint (`concepts.md` example A).
- **Never infer hidden or iceberg orders, spoofing, institutions, intent or queue position** from a
  static footprint. Those need order-level or account data.
- **Facts, interpretations and hypotheses are separate lists.** Certainty words ("will", "high
  probability") are not allowed without a cited test.

## Protocol (mandatory order)
1. **Identify**: instrument, venue (single or aggregated), timeframe, chart type(s), platform,
   visible time range and **time zone label**. Each item is either seen or "not visible".
2. **Settings**: legend and columns (with the basis above), units (coin/USD), decimals shown or
   rounded, row size (measure it from the price axis if not stated; on OpenMarket it is **not**
   always Ticks per bar × $5: $9, $15, $30 and $50 rows have all been seen), imbalance rule and
   colours, stats rows, anchors (CVD, VWAP, profile period), auto-merged rows.
3. **Extract**: row prices, cell numbers, bar totals, delta, imbalances and stacks (by the stated
   rule), POC, wicks, closes, marked levels. Copy numbers **as printed**. For two-sided cells keep
   left/right positions; map to buy/sell only through step 2.
4. **Check the reading**: row delta = buy − sell; rows sum to printed totals when every row is
   visible; prices on one grid; candle high/low vs the visible rows. If the header's high or low
   lies beyond the visible rows, the extremes are **cut off**: say so and don't judge the extreme
   rows. Mark every value as *exact*, *estimate* (read from an axis or bar length) or *unreadable*.
   Axis label text can sit a few pixels off its price: place the row grid using printed high/low
   markers where they exist. When a box or label hides part of a number, use the printed totals
   and delta to decide between the candidate readings, and say you did.
5. **Sequence**: rebuild what happened in the bar or bars: where aggression concentrated, where
   price went after it, where the close sits.
6. **Context**: trend or range, session, prior-day and prior-week levels, value area, VWAP, as
   visible or supplied. If missing, the read stays descriptive.
7. **Competing explanations**: at least two when the evidence allows more than one (for example
   passive buyers absorbing vs offers pulled; initiative vs short covering).
8. **For each**: what supports it, what contradicts it, and what would invalidate it.
9. **Conditional scenarios**: "if X then Y, invalid if Z", with the levels. Give both directions
   only when both are plausible.
10. **Ask** for a zoomed crop, the missing settings or the bar time when anything essential can't
    be read. Don't produce a trade idea from an insufficient picture.

**Optional data check** (when code execution is available): `scripts/check_screenshot.py` runs
the step 4 checks on a transcription, and, if the user supplies the venue's raw trades for that bar
(e.g. a Binance aggTrades CSV from data.binance.vision), rebuilds the bar at the chart's row size and
grid and compares it cell by cell. Once matched, the data replaces the transcription. Expect small
differences: platforms can move a few hundredths of a coin across bar boundaries, and OpenMarket
rounds BTC to whole coins unless decimals are on (±0.5).

## Output format (detailed analysis)
**A. Chart identification**: instrument, venue, timeframe, platform, chart type, visible settings,
what is missing.
**B. Objective observations**: readable numbers (exact/estimate), bid × ask relationships, delta,
imbalance and stack locations, POC, price response, candle structure, marked levels.
**C. Market context**: regime, session, prior-day/week levels, value area, VWAP, as visible or
supplied, and what is unknown.
**D. Order-flow interpretation**: aggressor behaviour, price response, possible passive opposition,
continuation or failure, and the limits of a static footprint. **Whenever delta, CVD or a delta
divergence is part of the evidence, say that it is one venue's flow** (BTC trades on many venues;
a single-venue divergence is venue-specific until other venues confirm it).
**E. Competing hypotheses**: at least one alternative when the chart is ambiguous.
**F. Conditional scenarios and practical use**: confirmation, invalidation and levels. Bullish and
bearish only when both are plausible. Then say what the chart is useful for right now (`uses.md`):
the diagnosis of the move that printed, the liquidity read (delta vs price response), and the
invalidation level a trader at this location would use.
**Directional lean** (when the user asks what happens next): **default "none"**. Give up/down only when a
rule with a passing test supports it (a card in `setups.md` above `exploratory-lead`) at that location and horizon, and cite it. Nothing has
passed validation: absorption-type setups at prior-day and value-area levels were tested with no edge,
and stacked imbalances and delta divergence are untested. So offer the conditional scenarios instead
of a direction, and say at which horizon the evidence does help (`uses.md` horizon map).
**G. Confidence and limitations**: *reading* confidence (how sure the numbers are right) separately
from *interpretation* confidence (how sure the story is right); unreadable or ambiguous elements.
**H. Research implications**: descriptive only / a testable hypothesis (point to the rule card in
`setups.md`, and say which data it needs: OHLCV, trades or order book) / covered by the author's tests
(cite the card's status in `setups.md` and the scope in `backtests.md`: the patterns tested had no edge) / validated
(nothing is yet).

## Typical mistakes
- Columns read backwards because colours were trusted.
- Stacks or imbalances called without knowing the row size, the ratio or the zero-cell rule.
- "Zero at the high" when the top rows are cut off or merged by auto-scale.
- Bar delta read as CVD, or a CVD level read without its anchor.
- Bar POC treated as the session POC.
- DOM or heatmap size treated as traded volume, or as committed liquidity.
- Time converted with an assumed offset. Footprint charts usually don't print their time zone, and
  the same platform has been seen set to both UTC and local time. Don't assume one: give the labels as
  printed, leave UTC unknown, and ask, unless the image, the user or a data match settles it
  (daylight saving also shifts local offsets in late October).
- Coin numbers compared with USD numbers, or rounded whole-coin cells treated as exact.
- One venue's footprint read as "the BTC market".
