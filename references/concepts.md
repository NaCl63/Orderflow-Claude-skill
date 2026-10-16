# Footprint and order-flow concepts

## How a footprint is built
A footprint is a two-way histogram: for each bar and each price row, the volume where the **buyer
was the aggressor** ("ask volume", taker buy) and where the **seller was the aggressor** ("bid
volume", taker sell). Everything else (imbalances, absorption, exhaustion) is a rule applied to
those two counts.

1. **Match:** an incoming marketable order (the aggressor) trades against resting limit orders
   (passive). CME ES/NQ match price-then-time (FIFO).
2. **Feed:** the aggressor side is reported by the exchange (CME MDP 3.0 tag 5797: 0 = none,
   1 = buy, 2 = sell; Binance `is_buyer_maker`). It is measured, not guessed.
3. **Aggregate:** each trade's quantity is added to its row's ask or bid column within the bar.

**Where classification breaks**
- CME trades with no aggressor: the open, after a pre-open/pause, and implied-order trades. The
  opening print is ambiguous.
- One CME Trade Summary (and one Binance aggTrade) consolidates all fills of one aggressor at one
  price. A "500-lot print" is usually one taker sweeping many resting orders.
- Feeds without an aggressor flag need inference (tick rule, Lee-Ready, BVC). On ES the tick rule
  misclassified 11.6% of trades, but 38.7% when applied to 60-s bars; BVC on 1-min bars got 23.2%
  wrong (Andersen & Bondarenko, T1). Errors correlate with volatility, which biases exactly the
  bars that matter.
- TradingView-style "footprints" built from OHLCV estimate delta from bar shape. **They are not
  footprints.**

## Core quantities

| Quantity | Definition | Status |
|---|---|---|
| Ask volume at P | Bought by aggressive buyers at P | Measured |
| Bid volume at P | Sold by aggressive sellers at P | Measured |
| Bar delta | Σ ask − Σ bid | Measured |
| CVD | Running delta from an anchor (session, day, swing, or the first loaded bar) | Measured; the anchor is a choice |
| POC | Price with the most volume (bar or session) | Measured (depends on row size) |
| Value area | Prices around the POC holding ~70% of volume (Steidlmayer) | Measured given the convention |
| Delta divergence | New price extreme without a new delta/CVD extreme | Pattern rule |
| Diagonal imbalance | Ask at P vs bid at P − 1 row ≥ ratio (often 3:1) with min volume | Pattern rule; the threshold is arbitrary |
| Stacked imbalance | 3+ consecutive diagonal imbalances one way | Pattern rule |
| Absorption / exhaustion / trapped traders | Interpretations of the above | **Inferred** |

**Why diagonal:** at 5000.00 bid / 5000.25 offer, buyers lift 5000.25 while sellers hit 5000.00.
Competing aggressors trade at adjacent prices at the same moment, so compare ask(P) with bid(P−1).

**Worked diagonal example**, ratio 3:1, min 50:

| Price | Bid | Ask | Test | Flag |
|---|---|---|---|---|
| 5005.00 | 20 | 260 | 260 vs 70 = 3.7× | buy imb |
| 5004.75 | 70 | 310 | 310 vs 85 = 3.6× | buy imb |
| 5004.50 | 85 | 290 | 290 vs 60 = 4.8× | buy imb |
| 5004.25 | 60 | 140 | 140 vs 110 = 1.3× | none |
| 5004.00 | 110 | 90 | — | — |

The result is a 3-row stack at 5004.50-5005.00. At 4:1 only one row qualifies, and at 2-tick rows
the stack can vanish, so **always state the ratio and row size behind a stack**.

## Why delta and price disagree (the key mechanism)
Cont, Kukanov & Stoikov (2014, T1): over short windows, price change ≈ OFI / depth, where OFI
counts **all** events at the best quotes:

ΔP ≈ (1 / (λ·depth)) × [ (buy MO − sell MO) + (bid adds − bid cancels) − (ask adds − ask cancels) ]

Delta is only the market-order term. When delta and price disagree, the limit-order part
dominated, **and the footprint can't see that part.** A DOM or heatmap recording can. The
relationship is linear with slope ∝ 1/depth: the same delta moves price more when the book is thin
(open, news, overnight, weekends for BTC). R² averaged 65% on 10-s bins in equities, and it is
**contemporaneous, not a forecast**. In thin crypto books (BitMEX) trade imbalance explained price
*better* than OFI (Silantyev 2019, T1, single venue).

### Example A: negative delta in a green bar
ES 1-min, O 5000.00 C 5001.25. Sellers initiated 800 more contracts, yet price rose 5 ticks.
Possible causes (the footprint can't tell which):
1. Passive buyers kept refilling the bid (absorption by limit buyers).
2. Offers were cancelled or lifted away (liquidity withdrawal). This is thinner and more fragile.
3. A mix, plus buying in a linked market (SPY/NQ/MES, or other BTC venues) arbitraged in passively.

Check next: did price hold above the bar's mid on the next bars? Book data would separate case 1
(bid size replenishing) from case 2 (ask size vanishing).

### Example B: absorption vs inactivity
Price stalls at an offer in both cases. **Absorption**: 3,400 traded vs ~300 displayed (~11×)
against a typical 400 per tick, so far more supply was available than was displayed. **Inactivity**:
120 traded, so nobody pushed and nothing is learned about supply.
Measurable rule of thumb: call it absorption only if traded volume at the level is several times
**both** its displayed depth and the typical per-tick volume, and price failed to trade through.
Otherwise it is a stall.

The strict v1.0 definition (event window t₀→t₁, quantities V, D₀, D₁, A_new, A_ref, C, hidden
residual H = V − (D₀ + A_new + A_ref − C − D₁); features RR = V/D₀, Z = V/V_med, PR = C/(supply);
labels Absorption: RR≥3, Z≥3, PR<0.5, no breakthrough; Withdrawal-driven advance; Stall without
information) **needs event-level book data**. A footprint or screenshot doesn't contain it, so only footprint
proxies are available: the Z part (traded vs normal) and "failed to trade through". Say so whenever
"absorption" comes up.

### Example C: exhaustion / finished auction
Top four rows at a new high: ask 380 → 95 → 12 → 0. Measured: buyers initiated less at each higher
tick and nothing at the high. Practitioners call this a "finished auction" (zero on one side at the
extreme). With both sides trading at the high (e.g. 35×60) they call it an "unfinished auction"
and "expect a revisit". **That revisit claim is untested (T4)**. Compare it against the revisit
rate of all highs at the same distance and time.

## Settings that change the picture
- **Row size** merges or splits imbalances and POCs. Fixed $ rows mean different things at $7k and
  $120k BTC, so compare rows as a share of the bar's range, not in dollars.
- **Bar type:** time bars mix quiet and busy periods; volume or dollar bars equalize information
  per bar (López de Prado AFML ch 2). Most retail footprints are time bars.
- **Feed:** aggregated trade streams merge fills of one taker, which changes trade counts but not
  volume.
- **CVD anchor:** session / day / continuous. This changes every divergence.
- **Instrument:** linked markets (MES/ES, perp/spot, other venues) are invisible on one footprint.

## Footprint vs other views

| View | Shows | Misses |
|---|---|---|
| Candles | OHLC, volume | Who initiated; distribution inside the bar |
| Time & sales | Every print, size, side, time | Spatial summary |
| DOM / ladder | Current resting size | History; what traded; spoofed or flickering size |
| Book heatmap | Resting size over time | Hidden size; can't separate cancels from fills without a trade overlay |
| Footprint | Executed volume by side per price per bar | Limit adds/cancels, hidden size, other venues |

## Advanced concepts. The stronger the evidence, the shorter the horizon

| Concept | Mechanism | Evidence | Measure | Use | Limits |
|---|---|---|---|---|---|
| OFI vs delta | OFI adds limit adds/cancels at L1 | OFI > trade imbalance in equities; reverse in thin BitMEX book (T1) | Needs L1 quote updates | Explains delta-price divergence | Contemporaneous |
| Multi-level OFI | Deeper flow also moves price | OOS fit improves with each level; collinear (Xu, Gould, Howison, T1) | L2/L3 | Weight deeper flow | Spoofable depth |
| Queue imbalance | Thinner queue depletes first | Predicts next mid move; AUC 0.75-0.81 large-tick vs 0.58-0.64 small-tick (Gould & Bonart, T1) | (bid−ask)/(bid+ask) at L1 | Execution timing | One-tick horizon; edge < spread for takers |
| Depth & impact | Impact per unit OFI ∝ 1/depth | Cont et al. (T1) | L1 depth by time of day | Expect bigger moves per delta at thin times | Depth flickers |
| Square-root impact | Metaorders split; latent liquidity V-shaped | Impact ∝ √Q across markets (Tóth et al., T1) | Needs parent orders | Why big volume rarely moves price proportionally | Parent orders, not single prints |
| Flow persistence | Order splitting → long-memory trade signs | Power-law sign autocorrelation (Lillo, Mike, Farmer, T1) | Sign autocorrelation | Flow predicts flow | **Not** return predictability: liquidity adjusts |
| Resiliency | Passive orders refill after sweeps | Bouchaud et al. Part V-VI | L1 recovery time | Absorbed vs exhausted | Needs book data |
| Trade-signing error | Inferred side is wrong for some trades | VPIN reversed with accurate signing (T1) | Inferred vs flagged | Use exchange flags only | Errors cluster in volatile bars |
| Event sampling | Information arrives unevenly | AFML ch 2 (T2) | Volume/dollar/imbalance bars | Compare like with like | Bar size is a parameter |
| Adverse selection | Makers lose to informed takers | Kyle, Glosten-Milgrom; Cartea et al. (T1) | Markouts after fills (1 s, 10 s, 60 s) | Check if resting orders | Retail latency |
| Hidden liquidity | Icebergs execute without showing | 44% of order volume hidden on Euronext Paris (Bessembinder et al.); CME native icebergs detectable from order IDs (Zotikov & Antonov, T1) | Traded ÷ max displayed | Absorption detection | Footprint can't see displayed size |
| News regimes | Liquidity withdraws before releases | ES impact rises, submissions slow (Takahashi, T1 WP) | Depth/events per minute | Different thresholds, or flat | Shocks fade in ~1 s |
| Incremental value | Flow features vs raw book | Flow inputs beat raw book; useful horizon ≈ 2 price changes (Kolm et al., T1) | Nested models | Test flow on top of a price/level setup | **No evidence at 5-60 min** |

**Signal or story?** (1) Pre-register the rule. (2) Base rate: compare with all bars at
the same location and time of day, not with zero. (3) Parameter surface: real effects are plateaus,
not spikes. (4) Count every variant and deflate (PBO).

## Who is behind the prints

| Participant | Documented behaviour | Footprint shows |
|---|---|---|
| Electronic MMs / HFT | One large HFT traded 4 of 5 times passively, earned the spread, lost on held positions (Menkveld 2013) | Passive side of prints; quotes flicker in the DOM |
| HFT in ES | 16 accounts ≈ ⅓ of E-mini volume around 6 May 2010, small inventories (Kirilenko et al.) | Much "aggressive" volume is inventory rebalancing, not conviction |
| Asset managers / pensions | Split parent orders over hours/days; impact ~√Q | Children look like small prints; one-sided persistence is the only trace |
| Hedge funds / CTAs | Mix passive and aggressive | Can't be separated without account data |
| Prop firms | Strategies not public | "Prop firm setups" = T3/T4 |
| Retail | Mostly small aggressive orders; poor outcomes | Small prints, but sliced institutional orders look the same |

Mechanics: FIFO means queue position, not size, decides who fills first. Every print has a passive
counterparty, so "buyers in control" only means buyers paid the spread. Makers pull or skew quotes
when flow looks informed, which is why depth vanishes before news and after sweeps. VWAP/TWAP algos
slice into small children. Spoofing is defined by **intent** (CFTC v JPMorgan, $920.2M, 2008-2016,
proven with account data and communications), so flickering size must not be labelled spoofing.
Large volume plus large replenishing passive supply = small move: impact depends on volume
relative to liquidity.

**Never inferable from a footprint:** identity, intent, opening vs closing, hedge vs directional,
parent-order size. Label "smart money buying" or "institutions defending" as inference.
