#!/usr/bin/env python3
"""Check numbers transcribed from a footprint screenshot.

Pure standard library, no private data. Two levels:

1. Internal checks (no data needed): row prices on one grid, no duplicate rows, row sums vs the
   bar's printed volume and delta.
2. Data check (optional): rebuild the bar from the venue's raw trades and compare cell by cell.
   Works with Binance aggTrades CSVs (futures or spot) from https://data.binance.vision, or any
   CSV with columns price, quantity, time (ms or us since epoch, UTC) and is_buyer_maker.

Transcription format (CSV, one row per price row, top to bottom or any order):
    price,sell,buy          # price = the row's LOWER edge as the chart labels it
    78600,12.4,30.1
    78585,40.2,8.0
"sell" = aggressive sellers (bid column), "buy" = aggressive buyers (ask column). Map the image's
columns to these only after the side has been established (legend, printed delta, or a documented
platform default), never from colour.

CLI:
    python check_screenshot.py --read read.csv [--row 15] [--volume 812.4] [--delta -35.2]
    python check_screenshot.py --read read.csv --trades BTCUSDT-aggTrades-2026-09-15.csv \
        --bar "2026-09-15 14:00" --tf 15m --row 15 [--grid-offset 0]

--bar is the bar OPEN time in UTC. Never guess the chart's time zone: ask the user.
--grid-offset shifts row edges (e.g. 3 when a platform snaps $50 rows to a $3 grid).
"""

import argparse
import csv
import datetime as dt
import math
from collections import defaultdict

TF_SECONDS = {"1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
              "1h": 3600, "2h": 7200, "4h": 14400, "1d": 86400}


# ---------------------------------------------------------------- level 1: internal checks
def internal_checks(rows, bar_volume=None, bar_delta=None, row=None, grid_offset=0.0):
    """rows = [(price, sell, buy), ...] as read from the image. Returns a dict of findings."""
    prices = [p for p, _, _ in rows]
    out = {"rows": len(rows),
           "duplicate_prices": sorted({p for p in prices if prices.count(p) > 1})}
    if row:
        out["off_grid_prices"] = [p for p in prices
                                  if not math.isclose(((p - grid_offset) / row) % 1, 0, abs_tol=1e-6)
                                  and not math.isclose(((p - grid_offset) / row) % 1, 1, abs_tol=1e-6)]
        srt = sorted(prices)
        out["gaps_in_ladder"] = [(a, b) for a, b in zip(srt, srt[1:]) if b - a > row + 1e-9]
    sell = sum(r[1] for r in rows if r[1] is not None)
    buy = sum(r[2] for r in rows if r[2] is not None)
    out["sum_volume"], out["sum_delta"] = round(sell + buy, 4), round(buy - sell, 4)
    out["unreadable_cells"] = sum(r[1] is None for r in rows) + sum(r[2] is None for r in rows)
    if bar_volume:
        out["volume_gap_pct"] = round(100 * ((sell + buy) / bar_volume - 1), 2)
    if bar_delta is not None:
        out["delta_gap"] = round((buy - sell) - bar_delta, 4)
        if bar_volume and math.isclose(sell - buy, bar_delta, abs_tol=max(0.5, 0.01 * bar_volume)) \
                and not math.isclose(buy - sell, bar_delta, abs_tol=max(0.5, 0.01 * bar_volume)):
            out["warning"] = "row sums reproduce the printed delta only with columns swapped: check the side mapping"
    return out


# ---------------------------------------------------------------- level 2: rebuild from trades
def _parse_time(v):
    t = float(v)
    if t > 1e17:      # nanoseconds
        t /= 1e9
    elif t > 1e14:    # microseconds (newer Binance spot files)
        t /= 1e6
    elif t > 1e11:    # milliseconds
        t /= 1e3
    return t


def _truthy(v):
    return str(v).strip().lower() in ("true", "1", "t", "yes")


def load_trades(path, start_s, end_s):
    """Yield (price, qty, is_buyer_maker) for trades with start_s <= time < end_s.
    Handles Binance aggTrades files with or without a header row."""
    with open(path, newline="") as f:
        first = f.readline()
        f.seek(0)
        has_header = any(c.isalpha() for c in first.replace("true", "").replace("false", "")
                         .replace("True", "").replace("False", ""))
        reader = csv.reader(f)
        if has_header:
            head = [h.strip().lower() for h in next(reader)]
            ip = head.index("price")
            iq = head.index("quantity") if "quantity" in head else head.index("qty")
            it = next(head.index(c) for c in ("transact_time", "time", "timestamp") if c in head)
            im = head.index("is_buyer_maker")
        else:   # Binance aggTrades column order
            ip, iq, it, im = 1, 2, 5, 6
        for r in reader:
            if not r:
                continue
            t = _parse_time(r[it])
            if start_s <= t < end_s:
                yield float(r[ip]), float(r[iq]), _truthy(r[im])


def build_bar(trades_path, bar_open_utc, tf, row, grid_offset=0.0):
    """Rebuild one bar: returns ({row_lower_edge: [sell, buy]}, totals dict)."""
    start = dt.datetime.fromisoformat(bar_open_utc).replace(tzinfo=dt.timezone.utc).timestamp()
    end = start + TF_SECONDS[tf]
    ladder = defaultdict(lambda: [0.0, 0.0])
    hi, lo, n = -math.inf, math.inf, 0
    for price, qty, buyer_is_maker in load_trades(trades_path, start, end):
        edge = math.floor((price - grid_offset) / row) * row + grid_offset
        ladder[round(edge, 8)][0 if buyer_is_maker else 1] += qty   # maker buyer => taker SELL
        hi, lo, n = max(hi, price), min(lo, price), n + 1
    if not n:
        raise ValueError(f"no trades between {bar_open_utc} UTC and +{tf}: wrong file, date or time zone?")
    sell = sum(v[0] for v in ladder.values())
    buy = sum(v[1] for v in ladder.values())
    return dict(ladder), {"trades": n, "high": hi, "low": lo, "volume": round(sell + buy, 4),
                          "delta": round(buy - sell, 4)}


def compare(rows, ladder, tol=0.02, abs_tol=0.01):
    """Cell-by-cell comparison. Status per row: ok / MISMATCH / SWAPPED / not transcribed / not in data."""
    read = {round(p, 8): (s, b) for p, s, b in rows}
    out = []
    close = lambda a, b: a is not None and abs(a - b) <= max(abs_tol, tol * abs(b))
    for p in sorted(set(read) | set(ladder), reverse=True):
        s, b = read.get(p, (None, None))
        ds, db = ladder.get(p, (None, None))
        if p not in read:
            status = "not transcribed"
        elif p not in ladder:
            status = "not in data"
        elif close(s, ds) and close(b, db):
            status = "ok"
        elif close(s, db) and close(b, ds):
            status = "SWAPPED (sell/buy columns reversed?)"
        else:
            status = "MISMATCH"
        out.append((p, s, b, None if ds is None else round(ds, 4), None if db is None else round(db, 4), status))
    return out


# ---------------------------------------------------------------- CLI
def _read_rows(path):
    def num(v):
        v = (v or "").strip()
        return None if v in ("", "?", "null", "None") else float(v)
    with open(path, newline="") as f:
        return [(float(r["price"]), num(r["sell"]), num(r["buy"])) for r in csv.DictReader(f)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--read", required=True, help="CSV of the transcription: price,sell,buy")
    ap.add_argument("--row", type=float, help="row size read from the image")
    ap.add_argument("--grid-offset", type=float, default=0.0)
    ap.add_argument("--volume", type=float, help="bar volume as printed")
    ap.add_argument("--delta", type=float, help="bar delta as printed")
    ap.add_argument("--trades", help="raw trades CSV (Binance aggTrades format)")
    ap.add_argument("--bar", help="bar open time in UTC, e.g. '2026-09-15 14:00'")
    ap.add_argument("--tf", choices=sorted(TF_SECONDS, key=TF_SECONDS.get))
    a = ap.parse_args()

    rows = _read_rows(a.read)
    print("Internal checks:")
    for k, v in internal_checks(rows, a.volume, a.delta, a.row, a.grid_offset).items():
        print(f"  {k}: {v}")

    if a.trades:
        if not (a.bar and a.tf and a.row):
            ap.error("--trades needs --bar, --tf and --row")
        ladder, tot = build_bar(a.trades, a.bar, a.tf, a.row, a.grid_offset)
        print(f"\nRebuilt bar {a.bar} UTC {a.tf}, row {a.row}: {tot}")
        res = compare(rows, ladder)
        print(f"\n{'price':>12} {'sell_read':>10} {'buy_read':>10} {'sell_data':>10} {'buy_data':>10}  status")
        for p, s, b, ds, db, st in res:
            f = lambda x: "-" if x is None else f"{x:g}"
            print(f"{p:>12g} {f(s):>10} {f(b):>10} {f(ds):>10} {f(db):>10}  {st}")
        bad = sum(r[5].startswith(("MISMATCH", "SWAPPED")) for r in res)
        print(f"\nrows checked: {sum(r[1] is not None for r in res)}, mismatches: {bad}")


if __name__ == "__main__":
    main()
