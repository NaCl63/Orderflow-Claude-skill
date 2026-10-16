# What footprint reading is good for

The other files say what not to claim. This one says what to do instead. The short version:
**a footprint is a diagnostic and a filter, not a forecaster.** The strong evidence (Cont, Kukanov &
Stoikov; Gould & Bonart; Kolm et al.) is about explaining price *now* and predicting the next few
ticks. That is enough to make flow useful for understanding, risk, execution and filtering. It is
not enough to support standalone multi-bar forecasts.

## Horizon map: match the use to the evidence

| Horizon | What the evidence supports | Useful footprint role | Tier |
|---|---|---|---|
| Ticks to seconds | Queue imbalance predicts the next mid move; OFI explains price change | **Execution**: rest a limit or cross the spread; when to wait | T1 (needs book data, not just a footprint) |
| The bar that just closed | Price change ≈ OFI / depth, contemporaneously | **Diagnosis**: what kind of move it was, how liquid the market was | T1 mechanism; reading it from trades only is partial |
| Next 1-3 bars at a predefined level | Nothing published; author's tests of absorption and sweep rules found no edge | **Filter and invalidation** on a setup that stands on its own | T3, untested as a filter |
| 5-60 min and beyond | No evidence | **None as a forecast.** Context only (positioning, forced flow) | T4 if claimed |

When someone asks "what happens next", answer at the horizon the evidence covers, and say which
horizon that is.

## 1. Diagnose what just happened (strongest, always available)
The OFI relation turns a footprint into an explanation of the move that already printed:

| Observation | What it means (contemporaneously) | What it does not mean |
|---|---|---|
| Big delta, big move | Aggression met thin opposition | That the move continues |
| Big delta, small move | Deep or refilling passive side (or a linked market absorbing) | Absorption proven; it needs book data |
| Small delta, big move | Book was thin or liquidity withdrew; limit side drove price | "Fake move"; thin-book moves are real prices |
| Delta against the candle | Limit-side events dominated (refills or pulled quotes) | A reversal signal |
| One-sided stack through several rows | Aggressors swept several levels inside that bar | An institutional zone |
| Volume concentrated at the extreme, price back inside | Trading happened at that price and was not accepted *in that bar* | That it won't be accepted on the next |

Practical value: post-trade review ("why did my stop get hit so fast?" → thin book, small delta
moved it), separating forced flow from voluntary flow (BTC liquidation cascades: `btc.md`), and
learning which market conditions a strategy trades in.

## 2. Read liquidity conditions, then adjust risk (T1 mechanism)
Impact per unit of flow is roughly 1/depth. If a modest delta moves price several rows, the book
is thin: around opens, news, funding timestamps, weekends and overnight for BTC. Practical
response, which needs no forecast:
- smaller size or wider stops in thin conditions, or stand aside;
- expect more slippage on market orders;
- treat any level as weaker when it is being tested in a thin book.
Measure it from data where possible (price change ÷ |delta| over recent bars, by time of day).

## 3. Define invalidation precisely (practical, untested for expectancy)
A thesis built on a level needs a point where it is wrong. Flow gives that point in measured
terms instead of an arbitrary tick distance:
- **Fade at a level** is invalid when price *accepts* beyond it: closes outside with delta in the
  breakout direction and new volume building there (initiative, `setups.md` card 7).
- **Breakout** is invalid when price returns inside on aggression against the breakout.
This does not make the trade profitable. It makes the loss defined and the reasoning checkable,
which is the precondition for testing anything.

## 4. Filter a setup that already stands on its own (testable)
The only defensible way to add a footprint condition to a strategy is as a **filter on a base
setup that has its own evidence**, measured as an increment:
1. Pick a base with published or pre-registered evidence (opening-range breakout with a relative
   volume filter is T2 in US equities; `evidence.md`).
2. Add one flow condition fixed in advance (breakout bar delta in the breakout direction above its
   80th percentile; no opposing stack at the breakout bar).
3. Compare base vs base + filter on the same trades, after costs, out of sample. Report every
   variant tried.
4. Keep the filter only if it improves expectancy or drawdown, not just hit rate (filters often
   raise hit rate by skipping the big winners).
Answer "should I use X as confirmation?" with this procedure, not with yes or no.

## 5. Execution at the few-tick horizon (T1, needs book data)
Queue imbalance at the best quotes predicts the next mid move, much more strongly for large-tick
instruments (ES, most stocks) than small-tick ones (BTC perps at fine tick sizes). Use: if you have
decided to trade, choose between resting a limit (queue on your side is thick) and crossing (your
side is thinning and price is about to move away). The edge is smaller than the spread for a taker
trading on it directly; its value is reducing slippage on trades you take for other reasons.
A footprint alone can't show this; a DOM or L1 feed can.

## 6. Generate hypotheses worth testing
Every observation that seems to repeat ("stacks at the overnight high keep failing") becomes a
rule card: location, condition, entry, invalidation, exit, base rate to beat, data needed
(`setups.md` format). That converts screen time into something that can be checked.

## How to answer with this
For a screenshot or setup question, after the facts and competing explanations, give the useful
part explicitly:
- **What it tells you now:** the diagnosis (section 1) and the liquidity read (section 2).
- **How you could use it:** invalidation level, filter role, or execution note, whichever applies.
- **What it can't tell you:** the multi-bar direction, unless a cited test covers it.
A reader should leave knowing what to do with the chart, not just what not to believe.
