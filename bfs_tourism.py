"""
Download monthly Swiss (FSO/BFS) hotel-sector tourism data, one CSV per month.

Table:  px-x-1003020000_101 - Hotel sector: arrivals and overnight stays of open
        establishments by year, month, commune and visitors' country of residence
Source: https://www.pxweb.bfs.admin.ch/pxweb/en/px-x-1003020000_101/

Usage:
    pip install requests
    python bfs_tourism.py                      # 2013-01 .. latest month -> bfs_tourism_monthly/
    python bfs_tourism.py 2020-01 2021-12      # custom range (YYYY-MM YYYY-MM)

Files are named YYYY-MM.csv (UTF-8, ',' separated, one row per commune x country
of residence, with Arrivals and Overnight stays columns). Existing files are
skipped, so the script can be re-run to resume or to pick up new months.
The table starts in 2013; months with no published values are skipped.
"""

import csv
import io
import sys
import time
from datetime import date
from pathlib import Path

import requests

URL = ("https://www.pxweb.bfs.admin.ch/api/v1/en/"
       "px-x-1003020000_101/px-x-1003020000_101.px")
OUT_DIR = Path(__file__).parent / "bfs_tourism_monthly"
FIRST = (2013, 1)
PAUSE = 2.0  # seconds between requests, the API rate-limits aggressively
MISSING = {"", ".", "..", "...", "-", "x", "X"}


def months(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def parse_ym(s):
    y, m = s.split("-")
    return int(y), int(m)


def fetch_month(session, year, month):
    body = {
        "query": [
            {"code": "Jahr", "selection": {"filter": "item", "values": [str(year)]}},
            {"code": "Monat", "selection": {"filter": "item", "values": [str(month)]}},
            # without this the country dimension collapses to the total only
            {"code": "Herkunftsland", "selection": {"filter": "all", "values": ["*"]}},
        ],
        "response": {"format": "csv"},
    }
    for _ in range(10):
        r = session.post(URL, json=body, timeout=180)
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 15)) + 2
            print(f"  rate limited, waiting {wait}s")
            time.sleep(wait)
            continue
        r.raise_for_status()
        return list(csv.reader(io.StringIO(r.content.decode("cp1252"))))
    raise RuntimeError("still rate limited after 10 attempts")


def main():
    today = date.today()
    start = parse_ym(sys.argv[1]) if len(sys.argv) > 1 else FIRST
    end = parse_ym(sys.argv[2]) if len(sys.argv) > 2 else (today.year, today.month)

    OUT_DIR.mkdir(exist_ok=True)
    session = requests.Session()
    saved = skipped = empty = 0
    for y, m in months(start, end):
        period = f"{y}-{m:02d}"
        out = OUT_DIR / f"{period}.csv"
        if out.exists():
            skipped += 1
            continue
        rows = fetch_month(session, y, m)
        header, body = rows[0], rows[1:]
        # value columns are the last two (Arrivals, Overnight stays)
        if not any(v not in MISSING for row in body for v in row[-2:]):
            print(f"{period}: no published values, skipping")
            empty += 1
            continue
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(header)
            w.writerows(body)
        saved += 1
        print(f"{period}: {len(body):,} rows -> {out.name}")
        time.sleep(PAUSE)
    print(f"\nDone: {saved} saved, {skipped} already present, {empty} empty, folder: {OUT_DIR}")


if __name__ == "__main__":
    main()
