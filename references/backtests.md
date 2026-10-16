# Author's backtests: what was tested and what it means

The skill's author ran event studies on a few footprint setups before publishing it. They are the
only tests of these exact rules that this skill knows of. Cite them as **author-run, unpublished,
not independently replicated** (tier T3 as evidence; code and data are not bundled). They are
included because a skill that shows only untested ideas would hide the one piece of evidence
pointing the other way.

## Scope (state it whenever you cite a result)
- **Instrument / venue:** Binance BTCUSDT USDT-margined perpetual; Binance BTCUSDT spot for test A.
- **Data:** Binance aggTrades rebuilt into footprints ($5 base rows); 1-min klines (spot vs perp);
  Binance 5-min open interest.
- **Period:** 2020-2024 in-sample; some follow-ups re-run on 2025 onwards as out-of-sample.
- **Timeframes:** 5m, 15m, 1h bars.
- **Benchmark:** the same location (prior-day high/low, value-area edge) **without** the footprint
  condition. A pattern has to beat its own level, not zero.
- **Costs:** taker fees included.

## Results

| Card (`setups.md`) | Test | Result |
|---|---|---|
| 1. Absorption → failed continuation | Zone version; then level + extreme rows + multi-bar + limit entry | No edge on 5m/15m/1h after fees |
| 5. Exhaustion (extreme-row fade) | Fade rule at PDH/PDL inside the sweep study | No edge; one 15m short lead failed on 2025+ data |
| 6. Liquidity sweep + failed auction | Sweep of PDH/PDL + fade + close back inside | No edge; follow-ups lost about 15-16 bp per trade on 2025+ data; the long side lost consistently on 15m |
| 12. Delta × open interest | Large 5-min selling bursts split by OI falling vs rising | Falling-OI selling did *worse* than rising-OI selling in most cells (against the "long liquidation → bounce" label), not significant on 2024, sign flipped in 2022-23, not tradable after fees: **exploratory lead only** |
| 13. Spot confirms perp | Perp 60-s delta bursts with vs without same-sign Binance spot delta | Agreement added nothing (≈ −0.3 bp, CI about −0.8 to +0.3). Binance spot and perp are arbitraged within the minute, so Binance spot is not an independent check. Coinbase, Bybit, OKX untested |

## How to use these results
- A null on Binance BTC perps, at these timeframes, with these exact rules, is **not** proof the
  pattern fails everywhere (ES, NQ, other venues, other thresholds). It is proof that the popular
  claim "this works" has at least one documented failure and no documented success.
- Never upgrade a card to "works" because of this file. Nothing here passed validation.
- When a user has their own test, compare its scope with this one before comparing results.
