# Strategy setups as falsifiable rule cards

None of these has a published, peer-reviewed or independently replicated backtest. Each is a
**hypothesis**. Its status says whether the skill's author has tested it (Binance BTCUSDT; scope and
caveats in `backtests.md`). The rules are written generically and apply to any instrument with
exchange-flagged aggressor data. Distances go in ATR fractions or
rows, not ticks (a 2-tick ES rule has no fixed BTC equivalent). Names like `buy_stack` or `pd_vah`
are shorthand for the plain-language condition. An illustrative chart is never evidence.

## Which data each feature needs

| Needs only OHLCV (any chart) | Needs trades with aggressor side (footprints, taker volume) | Needs order-book updates | Needs derivatives or other venues |
|---|---|---|---|
| Prior-day/week high, low, close; opening range; ATR; candle shape; approximate VWAP (typical price); range/volume bars | Bar and row delta, CVD, imbalances, stacks, bar POC, exact VWAP and volume profile, aggression at extremes, "heavy volume that failed to move price" (a *proxy* for absorption) | Displayed depth, refills, cancels, hidden size: the strict absorption definition, liquidity withdrawal, DOM/heatmap patterns, queue position | OI, funding, liquidations, spot vs perp basis, other venues' trades |

A screenshot estimate is never a substitute for these data. A visual pattern becomes testable
only once it is rewritten as a rule on one of these columns.

## How to read the status
`untested` = practitioner idea only; no test known. `tested-no-edge` = the author ran it on Binance
BTCUSDT 2020-2024 (some also 2025+) against the same location without the footprint condition,
after fees: no edge (`backtests.md`). `exploratory-lead` = a consistent difference that is not
tradable after fees. Nothing here is
validated, so no card supports a directional call on its own.

---

## 1. Absorption → failed continuation (short at resistance; mirror for long) · status: **tested-no-edge**
- **Mechanism:** aggressive buyers meet passive supply larger than displayed; when buying stops, price reverts.
- **Context:** not a trend day; at PDH, VAH, PWH or an overnight high; no scheduled news ±10 min.
- **Conditions:** heavy aggressive buying in the top 1-3 rows (≥ H × their 50-bar median); buy ≥ sell there; bar closes below the level, close location ≤ 0.5; volume ≥ its 20-bar average. Visual version: big ask prints at the high with no new high after them.
- **Entry:** close of the bar that closes back below the absorption price (market), or a limit at that close.
- **Invalidation/stop:** a trade above the absorption high; stop 0.1 ATR beyond it.
- **Exits:** 2R; VWAP; opposite value edge; 12-bar time stop.
- **Failure modes:** trend days; news; the passive seller is exhausted and the buyer lifts through; liquidity *withdrawal* looks identical in a footprint.
- **Counterexample:** the same prints followed by a breakout bar with stacked buy imbalances (the "absorber" was finished).
- **Tier:** T3 (iceberg *detection* is T1 on CME order-level data; its trading value is untested).
- **Data:** trades (proxy only); strict version needs order book.
- **Author's test:** zone version, then level + extreme rows + multi-bar + limit entry: no edge on 5m/15m/1h (`backtests.md`).

## 2. Stacked imbalance continuation · status: untested
- **Mechanism:** ≥3 stacked buy imbalances = buyers swept several offer levels; the first retest is defended.
- **Context:** leaving the prior-day value area or the opening range, in the stack's direction.
- **Conditions:** `buy_stack ≥ 3` (ratio 3, min volume) in one bar; close in the top third (`clv ≥ 0.67`); close above `pd_vah` or `dh_prev`.
- **Entry:** first later bar whose low touches `buy_stack_lo` (carry the level forward), with bar delta > −X (X = 20th percentile of bar delta).
- **Invalidation/stop:** a close below the stack; stop 0.1 ATR under `buy_stack_lo`.
- **Exits:** prior swing high; 2R; trail under the newest stack.
- **Failure modes:** stacks formed *into* a higher-timeframe level; quiet sessions where 3:1 means 6 vs 2 coins.
- **Counterexample:** the retest slices through the stack on rising sell delta (the stack was short covering, not initiative).
- **Tier:** T3. A ~48% win-rate forum claim is unsourced (T4).
- **Data:** trades.

## 3. Trapped aggressors / failed breakout (stack reversal) · status: untested
- **Mechanism:** a stack at a range extreme that is immediately rejected traps the late aggressors, whose exits fuel the reversal.
- **Context:** range day (price inside the prior-day range for the first N hours); stack forms beyond PDH/PDL or the session extreme.
- **Conditions:** `buy_stack ≥ 3` with `buy_stack_lo` above PDH; within K bars price closes back below PDH and below `buy_stack_lo`.
- **Entry:** that close (market).
- **Invalidation/stop:** a new high above the stack bar; stop 0.1 ATR beyond it.
- **Exits:** prior-day POC; VWAP; 2R.
- **Failure modes:** trend days (the trap becomes a pullback); news.
- **Counterexample:** the reclaim fails and the next bar prints a new stack above (continuation).
- **Tier:** T3/T4.
- **Data:** trades.

## 4. Delta and CVD divergence at a level · status: untested
- **Mechanism:** a new high made on weaker aggressive buying shows the push is running out.
- **Context:** only at a predefined level (PDH, PWH, VAH); ignore mid-range divergences.
- **Conditions:** higher high at the level; bar delta at the new high < 50% of the delta at the prior swing high; CVD (anchored at the UTC day open, declared) makes a lower high.
- **Entry:** break of the divergence bar's low.
- **Invalidation/stop:** a new high above the divergence bar.
- **Exits:** VWAP; prior-day POC; 2R; time stop.
- **Failure modes:** in trends divergence persists for many bars; per the OFI mechanism (`concepts.md`) offers being pulled means less buying was needed, which is *bullish*.
- **Counterexample:** divergence after divergence while price trends higher.
- **Tier:** T3 at a level; generic divergence T4.
- **Data:** trades. A screenshot's CVD is only usable if its anchor is known.

## 5. Exhaustion at session extremes · status: one version **tested-no-edge**
- **Mechanism:** aggressive volume per row declines into the extreme and reaches (near) zero at the high: the auction finished.
- **Context:** session or prior-day extremes, late session, range.
- **Conditions:** `top1_buy ≤ f × buy_vol / n_rows` (fade f) and `top1_buy < top2_buy < top3_buy`; the top rows must be visible (not cut off or merged).
- **Entry:** close back inside the level within K bars.
- **Invalidation/stop:** a new high; stop 0.1 ATR above it.
- **Exits:** midpoint of the range; VWAP; 2R.
- **Failure modes:** thin markets where zero rows are common by chance; OpenMarket's auto-scale merging the top rows.
- **Counterexample:** a "finished" high taken out on the next bar with fresh stacked buying.
- **Tier:** T3 ("unfinished auction revisits" are untested, T4).
- **Data:** trades.
- **Author's test:** the fade rule at PDH/PDL, inside the sweep study: no edge; the one 15m short lead failed on 2025+ data.

## 6. Liquidity sweep + failed auction · status: **tested-no-edge** (also failed on 2025+ data)
- **Mechanism:** stops cluster beyond obvious highs and lows; a sweep fills them, aggression dries up, price returns inside.
- **Context:** PDH/PDL, PWH/PWL, overnight extremes, first sweep of the day.
- **Conditions:** high ≥ PDH + s × ATR, the first such bar today; extreme-row fade (card 5); close back below PDH within K bars, same day.
- **Entry:** that close.
- **Invalidation/stop:** acceptance beyond the level (N bars closing outside); stop 0.1 ATR above the sweep high.
- **Exits:** range midpoint; POC; VWAP; 2R.
- **Failure modes:** breakout days; news.
- **Counterexample (author's test):** on 15m, the long side of the same rule lost consistently; reclaims of PDL kept falling.
- **Tier:** T3; stop clustering in FX (Osler) is a T2 pointer.
- **Data:** trades.
- **Author's test:** no edge 2020-2024; follow-ups lost about 15-16 bp per trade on 2025+ data.

## 7. Initiative vs responsive activity (Dalton) · status: untested
- **Mechanism:** aggression away from value (outside the prior value area) is *initiative* and tends to build new value; aggression back toward value is *responsive* and tends to rotate.
- **Context:** open relative to the prior-day value area.
- **Conditions:** initiative = close outside `pd_vah`/`pd_val` with bar delta in the breakout direction above its 80th percentile and a stack ≥ 2; responsive = the same outside the VA but delta *toward* value.
- **Entry:** initiative: continuation on the next close beyond; responsive: rotation entry on a close back inside the VA.
- **Invalidation/stop:** back inside value (initiative); a new extreme outside value (responsive).
- **Exits:** the opposite VA edge; POC; 2R.
- **Failure modes:** news; low-volume weekends.
- **Counterexample:** strong initiative delta outside value that fully reverses (short covering, not new positions; check OI).
- **Tier:** T3.
- **Data:** trades.

## 8. Trend pullback continuation · status: untested
- **Mechanism:** in a trend, pullbacks with little counter-aggression are absorbed and the trend resumes.
- **Context:** trend defined on OHLCV (e.g. price above a rising 20-bar EMA and above VWAP).
- **Conditions:** pullback to VWAP or to a prior stack's origin; counter-delta over the pullback < 30% of the impulse delta.
- **Entry:** first bar closing back in the trend direction with delta in that direction.
- **Invalidation/stop:** a close beyond the pullback extreme.
- **Exits:** prior high; 2R; trailing stop.
- **Failure modes:** trend ends (a lower high forms); the pullback becomes a range.
- **Counterexample:** a small-delta pullback that keeps grinding through VWAP (low aggression ≠ support).
- **Tier:** T3.
- **Data:** trades + OHLCV.

## 9. VWAP interactions · status: untested
- **Mechanism:** VWAP is an execution benchmark, so flow clusters around it; rejection or acceptance there may carry information.
- **Context:** session (UTC day) VWAP; anchored VWAP only with a declared anchor.
- **Conditions:** touch of VWAP ± 0.1 ATR; rejection = close back on the original side with delta in that direction; acceptance = two closes beyond.
- **Entry:** the rejection close (fade) or the acceptance close (continuation).
- **Invalidation/stop:** a close on the other side; stop 0.1 ATR beyond the touch extreme.
- **Exits:** prior swing; band; 2R.
- **Failure modes:** chop around VWAP on range days.
- **Counterexample:** repeated "rejections" that each fail by a few bars.
- **Tier:** T3.
- **Data:** trades (exact VWAP) or OHLCV (approximate).

## 10. Opening-range breakout with an order-flow filter · status: untested
- **Mechanism:** ORB has published edges in US equities (Zarattini et al., T2 with caveats); flow may filter false breaks.
- **Context:** BTC has no official open. Pre-register one: 00:00 UTC (daily candle) **or** 13:30 UTC (US cash open).
- **Conditions:** 15/30-min opening range; breakout bar delta in the breakout direction ≥ its 80th percentile, or a stack in that direction.
- **Entry:** stop entry at OR high/low + 1 row (model slippage) or the breakout close.
- **Invalidation/stop:** a close back inside the OR.
- **Exits:** end of session; 2R; OR-height multiples.
- **Failure modes:** low relative volume days; news inside the range.
- **Counterexample:** high-delta breakouts that reverse into the range (short-term exhaustion).
- **Tier:** ORB T2 (equities); the flow filter is untested.
- **Data:** OHLCV (ORB) + trades (filter).

## 11. Value-area acceptance / rejection (Dalton) · status: untested
- **Mechanism:** price that opens outside the prior value area, re-enters and holds tends to rotate to the other side; price that holds outside builds new value.
- **Context:** first hours of the UTC day relative to `pd_vah`/`pd_val`.
- **Conditions:** open outside the VA; re-entry = two consecutive 15m closes inside; footprint role: responsive aggression at the edge (card 1/5) vs initiative away (card 7).
- **Entry:** the second close inside (rotation).
- **Invalidation/stop:** a close back outside.
- **Exits:** the opposite VA edge; POC.
- **Failure modes:** trend days.
- **Counterexample:** re-entry that fails at the POC and returns outside.
- **Tier:** T3. The popular "80% rule" percentages were not found in any primary test.
- **Data:** trades (VA) + OHLCV.

## 12. Footprint + open interest, funding and liquidations · status: **exploratory-lead** (delta × OI only)
- **Mechanism:** the same aggressive flow means different things when positions are opening vs closing, or when it is forced (liquidations).
- **Context:** large delta events.
- **Conditions:** 5-min delta ≤ p-th percentile of the trailing 30 days; OI change over the same 5 min: falling ≤ −b%, rising ≥ +b% (volume-weighted OI change, thresholds fixed before testing). Extensions: funding extremes; liquidation volume share.
- **Entry:** at the event close (15-min horizon) for the event study; trades only after a passing gate.
- **Invalidation/stop:** defined per extension before testing.
- **Exits:** fixed horizons {1, 5, 15, 60 min}.
- **Failure modes:** OI labels are probabilistic (`btc.md` table): rising OI is a new long *and* a new short.
- **Counterexample (author's test):** 2022 and 2023 had the opposite sign to 2020-21 and 2024.
- **Tier:** T3 (OI-label folklore); author's test: lead only.
- **Data:** trades + OI; funding and liquidation feeds for the extensions.
- **Author's test:** falling-OI selling did worse than rising-OI selling in most cells, not significant on 2024 data; sign flipped in 2022-23; not tradable after fees.

## 13. Cross-venue spot and perpetual confirmation · status: **tested-no-edge** (Binance spot vs perp only)
- **Mechanism:** flow common across venues drives most BTC returns (Makarov & Schoar, T1); agreement may separate real demand from venue-specific noise; spot-led moves may be unlevered demand.
- **Context:** large perp delta bursts.
- **Conditions:** perp 60-s delta z ≥ Z (24-h SD); agreement = other venues' z with the same sign ≥ A (fixed before testing).
- **Entry:** event close; horizons 1/5/15/60 min.
- **Exits:** fixed horizons.
- **Failure modes:** venues arbitraged within the minute (as Binance spot vs perp turned out to be).
- **Counterexample (author's test):** agreeing events did no better (≈ −0.3 bp, CI about −0.8 to +0.3).
- **Tier:** T1 for the common-flow fact; the trading rule is T3.
- **Data:** trades from several venues. Only Binance spot + perp (1-min) was tested; Coinbase spot, Bybit/OKX perps and 1-s bins are open.

---

## Worked example (illustrative, not a backtest): sweep + absorption short in ES
PDH 5040.00, VAH 5032.00, ON high 5037.50, no releases until 10:00. At 09:41 the rally reaches
5041.50 with ask volume fading 620/410/260/140/60/0 into the high. At 09:43, 1,900 lots trade at the
ask at 5040.75 while ≤150 were ever displayed (≈13×), and nothing prints at 5041.75. At 09:45 a bar
closes at 5039.50 with delta −310 → short 5039.25, stop 5042.00 (11 ticks), target VAH 5032.00
(29 ticks ≈ 2.6R). If the 10:00 release lifts price through the stop, the loss is −11 ticks.
Lessons: be flat before scheduled releases (BTC equivalents: funding times, CPI/FOMC). And the
"≤150 displayed" part needs DOM data, which a footprint screenshot cannot show.
