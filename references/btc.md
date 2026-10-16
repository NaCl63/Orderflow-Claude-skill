# Bitcoin specifics

The footprint mechanics carry over from CME, but the assumptions don't. ES is one central book
with an exchange-reported aggressor. BTC is dozens of books, some with inflated volume, linked by
arbitrage and perpetual funding.

| Topic | CME ES/NQ | BTC perps and spot |
|---|---|---|
| Venue structure | One Globex book, FIFO | Fragmented CEXs/DEXs, no best-execution linkage |
| Aggressor | Exchange tag 5797; none at open/pause/implied | Exchange taker side, per venue |
| Volume quality | Regulated | >70% of reported volume on unregulated venues estimated as wash trading (Cong et al. 2023, T1). Use top-tier venues |
| One footprint = | Most ES price discovery | One venue's flow. Most BTC return variation comes from order flow common across exchanges (Makarov & Schoar 2020, T1; ~80%, abstract-level) |
| Price discovery | ES leads cash | Contested: Binance/BitMEX perps and CME each lead in different studies and periods |
| Depth | Deep, queue position matters | Thinner; trade imbalance can beat OFI (Silantyev, T1) |
| Sessions | RTH 09:30-16:00 ET vs overnight | 24/7; liquidity varies by region and weekend |
| Extra state | PD/PW levels, VWAP, macro releases | Funding, OI, liquidations, spot-perp basis |
| Forced flow | Stops; margin calls rarely visible | Liquidation engines send market orders that show up as aggressive flow |

## Funding
Longs pay shorts a rate tied to the perp-spot gap, typically every 8 h (Binance: 00, 08, 16 UTC).
Deviations from no-arbitrage are larger than in traditional FX (He, Manela, Ross, von Wachter).
High positive funding means longs pay to hold. It is a **positioning gauge, not a timing signal**.
Costs: include funding when a holding period crosses a funding timestamp.

## Open interest × delta: probabilistic labels only
Every contract has one long and one short. Rising OI = a new long *and* a new short were created.
OI doesn't say which side was the aggressor or who is informed.

| ΔOI | Delta / price | Common label | Other explanations consistent with the same data |
|---|---|---|---|
| Up | Positive, rising | New longs initiating | Aggressive buyers closing shorts while passive participants open both sides; basis traders shorting perps vs spot longs |
| Up | Negative, falling | New shorts initiating | Hedgers shorting perps vs spot; aggressive sellers closing longs while others open |
| Down | Negative, falling | Long liquidation/closing | Voluntary profit-taking; forced vs voluntary unknown without a liquidation feed |
| Down | Positive, rising | Short covering/squeeze | Longs exiting passively into aggressive covering |

## Liquidations
10-11 Oct 2025: ≈$19B liquidated after a tariff announcement; BTC ≈$122.6k → ≈$104.8k; market
makers pulled quotes, and some venues had load problems (CoinShares; secondary sources, T3). On a
footprint a cascade looks like extreme negative delta with stacked sell imbalances: **forced flow,
not informed selling**. OI that stops falling is a condition to monitor, not a reversal trigger.
OI can stabilise while price keeps falling.

## Spot vs perp delta
Perp-led moves with flat spot delta = leverage-driven. Spot-led (e.g. Coinbase taker buying) =
unlevered demand. Practitioners use this widely; there is no peer-reviewed test (T3).
**Practical rule:** aggregate taker flow across the major perp venues plus 1-2 spot venues before
reading delta. Treat a single-exchange divergence as venue-specific until confirmed.

## What the author's Binance tests found (2020-2024, after fees; scope in `backtests.md`)
- **Spot agreement (Binance spot vs perp):** perp delta bursts confirmed by spot did no better than
  unconfirmed ones (precise null). The two are arbitraged within the minute, so Binance spot is not
  an independent confirmation; other venues (Coinbase, Bybit, OKX) were not tested.
- **Delta × OI:** large selling bursts with *falling* OI did *worse* afterwards than those with
  rising OI. That contradicts the "long liquidation → bounce" label in the table above, but the
  effect flipped sign in 2022-23 and is not tradable after fees: a lead, not a rule.
