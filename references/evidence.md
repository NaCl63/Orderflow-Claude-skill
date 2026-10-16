# Evidence: tiers, base rates, misconceptions, sources

## Tiers
T1 primary empirical (peer-reviewed or exchange spec) · T2 technical professional (books, working
papers by practitioners) · T3 practical education (Dalton, practitioner channels) · T4 unverified
(forum claims, vendor win rates). A claim missing sample size, period, costs, slippage, OOS split
or the number of variants drops to T4.

## What the evidence supports (T1)
- Net order flow at the best quotes explains most short-interval price change, linearly, slope ∝
  1/depth (Cont, Kukanov & Stoikov 2014). Contemporaneous, not a forecast.
- OFI (with limit adds/cancels) beats trade-only imbalance in liquid equities; in the thin BitMEX
  XBTUSD book trade imbalance did better (Silantyev 2019).
- Book/queue imbalance predicts the next mid move, strongly for large-tick and moderately for
  small-tick instruments (Gould & Bonart 2016). Forecast horizon of flow models ≈ two average price
  changes (Kolm, Turiel & Westray 2023).
- Trade-sign classification matters: VPIN's "toxicity" signal reversed with accurate
  classification on the E-mini (Andersen & Bondarenko).
- The one positive profitability result from book signals (Cartea, Donnelly, Jaimungal 2018) is
  for a passive, low-latency market-making strategy, not a retail taker.

## What it does not support
- That stacked imbalances, absorption or delta divergence are profitable on their own. No
  peer-reviewed test of these exact patterns exists.
- That a footprint reveals who traded or why.
- That one crypto exchange's footprint represents "the BTC market".

## Strategies with published backtests (price/volume effects that flow might filter)

| Strategy | Source | Result | Caveats |
|---|---|---|---|
| Market intraday momentum | Gao, Han, Li, Zhou, JFE 2018; SPY 1993-2013 | First half-hour return predicts last half-hour; stronger on volatile, high-volume, news days | Peer-reviewed; one trade/day; small R² |
| 5-min ORB, all stocks | Zarattini, Barbon, Aziz 2024; 2016-2023 | 29% total, Sharpe 0.48, hit 41.4% | Weak without a filter |
| 5-min ORB "Stocks in Play" (rel. volume ≥100%, top 20) | same | 1,637% total, Sharpe 2.81, MDD 12% | No slippage despite stop entries; no explicit OOS; 15/30/60-min versions much weaker; co-author runs a trading-education firm |
| SPY "noise area" momentum | Barbon, Aziz, Zarattini 2024 | 19.6%/yr, Sharpe 1.33 net | Working paper; independent replications lower |
| Hedging-demand intraday momentum | Baltussen et al., JFE 2021 | Momentum partly from dealer gamma hedging | Not visible on any footprint |

The ORB result depends on a relative-volume filter, an order-flow-adjacent variable. Whether
delta, stacks or OFI improve ORB expectancy is **unpublished**.

## Base rates any claim must beat
Among Brazilian mini-index day traders who persisted 300+ days, **97% lost money**, with no evidence
of learning, and only ~0.4-0.5% earned more than a bank teller's wage (Chague, De-Losso, Giovannetti;
specific to that market and sample).

## Misconceptions → better statements

| Claim | Why misleading | Better statement |
|---|---|---|
| "The footprint shows institutions buying." | Aggressor side is measured; identity/intent aren't. ⅓ of ES volume around the 2010 crash came from small-inventory HFTs | Someone paid the spread to buy; who and why is unknown |
| "Positive delta → price should go up." | Price depends on all book events | Delta is one part of OFI; divergence means the limit side dominated |
| "Order flow predicts price." | Evidence is contemporaneous or one-tick-ahead | Explains price now, forecasts a few ticks; minute-scale footprint forecasts are untested |
| "Big volume at a level = support." | Could be intermediary inventory turnover | A level matters if repeated tests reject beyond a base rate |
| "Stacked imbalances are institutional zones." | Thresholds are arbitrary; the 48% win rate is unsourced (T4) | A stack records one-sided sweeping in that bar; test its forward value |
| "Unfinished auctions always get revisited." | No primary test; nearby revisits are frequent by chance | Compare the revisit rate of unfinished highs with all highs at the same distance/time |
| "Spoofing is visible on the heatmap." | Spoofing = intent, proven with account data | Flickering size is unreliable; don't label it spoofing |
| "One exchange's BTC footprint shows the market." | Flow is common across venues; wash trading on unregulated venues | Aggregate top-tier venues |
| "VPIN/toxicity warns of crashes." | Reversed with accurate classification | Disputed |
| "With order flow retail can day-trade for a living." | 97% of persistent day traders lost | Strongly negative base rate; any edge needs documented testing |
| "A clean backtest proves the edge." | Best-of-many selection inflates results | Report all variants and an overfitting estimate (PBO) |

## Vetting a video, course or vendor
Pause at each entry and write down: the level, the footprint evidence, the invalidation, and what
happened on the **ten nearest similar setups**. If the presenter can't answer the last one, the
video teaches vocabulary, not edge. Also ask: were the examples pre-selected? Was the level defined
before the trade? For win rates: sample, period, costs, slippage, OOS, variants tried.
Channels: Axia Futures (live footprint/DOM reads; course considered overpriced by some), Jigsaw
(DOM/tape; software vendor, so separate execution skill from signal), Michael Valtos (pattern
vocabulary; sells an add-on), Trader Dale (volume-profile levels; were HVN/LVN tested against
random levels?). All T3.
Verifiable talks: Bouchaud on market impact (slides); Westray on multi-level/cross-asset OFI (NYU
2022); Cont on SPDE LOB models; López de Prado "7/10 reasons ML funds fail" (watch before building
any backtest).

## Ranked reading list
1. Bouchaud, Bonart, Donier, Gould, *Trades, Quotes and Prices* (CUP 2018). Part II, ch 10, Part V, ch 15.
2. Cont, Kukanov, Stoikov, "The price impact of order book events", JFE 2014, arXiv 1011.6402.
3. Harris, *Trading and Exchanges* (OUP 2002). Parts III-IV, ch 10 informed traders.
4-5. CME MDP 3.0 Trade Summary (tag 5797) and Supported Matching Algorithms.
6. Dalton, *Mind Over Markets* / *Markets in Profile* (T3, conceptual).
7. Hasbrouck, *Empirical Market Microstructure* (OUP 2007).
8. Gould & Bonart, queue imbalance, arXiv 1512.03492.
9. Kolm, Turiel, Westray, "Deep order flow imbalance", Math. Finance 2023, SSRN 3900141.
10. Xu, Gould, Howison, multi-level OFI, arXiv 1907.06230.
11. Easley, López de Prado, O'Hara (JFE 2016), read with Andersen & Bondarenko (RoF 2015).
12. Zotikov & Antonov, CME iceberg detection, arXiv 1909.09495.
13. Tóth et al., anomalous price impact, PRX 2011, arXiv 1105.1694.
14. Lillo, Mike, Farmer, long memory in supply/demand, arXiv cond-mat/0412708.
15. Kirilenko, Kyle, Samadi, Tuzun, Flash Crash, JF 2017, SSRN 1686004.
16. Takahashi, OFI and macro news, arXiv 2508.06788.
17. Silantyev, crypto order flow, Digital Finance 2019, DOI 10.1007/s42521-019-00007-w.
18. Makarov & Schoar, crypto arbitrage, JFE 2020, eprints.lse.ac.uk/100409.
19. López de Prado, *Advances in Financial Machine Learning* (Wiley 2018). Ch 2, 7, 11-14, 19.
20. Bailey, Borwein, López de Prado, Zhu, PBO, SSRN 2326253 (R package `pbo`).
21. Chague et al., "Day trading for a living?", SSRN 3423101.
22. Gao, Han, Li, Zhou, intraday momentum, JFE 2018.
23. Zarattini, Barbon, Aziz, ORB, SSRN 4729284.
24. Bessembinder, Panayides, Venkataraman, hidden liquidity, JFE 2009, SSRN 956476.
Crypto extras: Cong et al. wash trading (Mgmt Sci 2023, NBER w30783); He, Manela, Ross, von Wachter
perpetuals (arXiv 2212.06888); Albers et al. BTC fragmentation/cross-impact (arXiv 2108.09750;
linear models explain 10-37% of 500-ms returns, and the fee regime decides leader/lagger).

## Evidence ledger caveat
Of the 30 load-bearing claims in the research behind this skill, only 7 were checked against the full paper. Most numbers come from abstracts
or secondary sources. Upgrade before relying on them: trade imbalance vs OFI numbers (Cont §4.1),
the "two price changes" horizon (Kolm), Cartea OOS profit, Makarov & Schoar's 80%, the 97% figure;
then hidden-order share, square-root impact, sign memory, Menkveld, multi-level OFI, Takahashi,
Silantyev. **No primary support exists** for: the 48% stack win rate, unfinished-auction revisit
rates, value-area rotation percentages.
