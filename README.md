# orderflow — an evidence-graded order-flow & footprint skill for Claude

Reads footprint and order-flow charts like a skeptical quant: splits measured data from
inference, insists on location, and tells you which patterns have actually been tested
(almost none have).

## What it does
- **Reads chart screenshots** (footprint, volume profile, DOM, heatmap, CVD, OI) with a fixed
  10-step protocol: sides established from the legend or printed delta, never from colour; row
  size measured from the image; time zone never assumed; unreadable numbers flagged, not guessed.
- **Explains concepts**: delta, CVD, diagonal and stacked imbalances, absorption vs stalls,
  finished/unfinished auctions, POC/value area/VWAP, OFI and why delta and price disagree.
- **Judges setups** as falsifiable rule cards (13 of them): mechanism, conditions, entry, stop,
  failure modes, counterexample, evidence tier, test status.
- **BTC specifics**: venue fragmentation, wash trading, funding, OI × delta labels as
  probabilities, liquidation cascades, spot vs perp.
- **Says what footprints are good for**: a horizon map from ticks to hours, and the practical
  uses the evidence supports: diagnosing the move that just printed, reading liquidity to adjust
  risk, defining invalidation, filtering a setup that stands on its own (with a test procedure),
  and execution timing.
- **Vets claims** from videos, courses and vendors against base rates and a checklist.

## What it won't do
Give trade calls. Its directional lean defaults to "none" and it answers with conditional
scenarios, plus what the chart is useful for at the horizon the evidence covers. It will not call a pattern "high probability" without a cited test.

## Evidence it rests on
Peer-reviewed market-microstructure research (Cont, Kukanov & Stoikov; Gould & Bonart; Bouchaud
et al.; Makarov & Schoar, and others; full list in `references/evidence.md`), plus the author's
own event studies on Binance BTCUSDT 2020-2024 after fees, which found no edge in absorption,
sweep/failed-auction or spot-confirmation setups (`references/backtests.md`). Those tests are
unpublished and not independently replicated; the skill says so whenever it cites them.

## Install

**Claude app (web/desktop):** download `orderflow.zip` from the
[latest release](https://github.com/NaCl63/Orderflow-Claude-skill/releases/latest),
then upload it in the Skills section of settings.

**Claude Code:**
```bash
git clone https://github.com/NaCl63/Orderflow-Claude-skill ~/.claude/skills/orderflow
```

Then ask about order flow, or drop in a footprint screenshot and say which time zone the chart uses.

## Optional script
`scripts/check_screenshot.py` (Python 3, standard library only) checks a screenshot
transcription for internal consistency and, given raw trades such as a Binance aggTrades CSV
from data.binance.vision, rebuilds the bar and compares it cell by cell. Run with `--help`.

## Contents
```
orderflow/
├── SKILL.md                  ground rules, workflow router, answer format
├── references/
│   ├── visual-analysis.md    screenshot protocol + A–H output format
│   ├── chart-types.md        every format, verified platform conventions
│   ├── concepts.md           mechanics, quantities, OFI, participants
│   ├── uses.md               what footprints are good for, by horizon
│   ├── setups.md             13 rule cards with test status
│   ├── backtests.md          the author's tests: scope and results
│   ├── btc.md                crypto market structure
│   └── evidence.md           tiers, base rates, misconceptions, reading list
└── scripts/check_screenshot.py
```

## Disclaimer
Educational analysis only, not financial advice. Trading is risky; most active day traders lose
money (see the base rates in `references/evidence.md`).

Author: Sergiu.
