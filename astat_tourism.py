"""
Download monthly South Tyrol (ASTAT) tourism data, one CSV per month.

Dataset: ITH1,DF_TOUR_ACC_CAP_COMMUNITY_MONTHLY_1,1.0
         (accommodation capacity / arrivals / overnights per municipality, monthly)
Source:  https://statastat.prov.bz.it/databrowser/ -> SDMX web service behind it

Usage:
    pip install requests
    python astat_tourism.py                      # 2005-01 .. latest month -> astat_tourism_monthly/
    python astat_tourism.py 2020-01 2021-12      # custom range (YYYY-MM YYYY-MM)

Files are named YYYY-MM.csv (SDMX-CSV, ';' separated). Existing files are skipped,
so the script can be re-run to resume or to pick up new months.
"""

import csv
import io
import sys
import time
from datetime import date
from pathlib import Path

import requests

URL = ("https://astatsdmxservices.prov.bz.it/dsm/NSI_WS/rest/data/"
       "ITH1,DF_TOUR_ACC_CAP_COMMUNITY_MONTHLY_1,1.0/M...../ALL/")
HEADERS = {"Accept": "application/vnd.sdmx.data+csv;version=1.0.0"}
OUT_DIR = Path(__file__).parent / "astat_tourism_monthly"
PAUSE = 0.5  # seconds between requests, be polite to the server


def months(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def parse_ym(s):
    y, m = s.split("-")
    return int(y), int(m)


def fetch_month(session, period):
    r = session.get(URL, params={"startPeriod": period, "endPeriod": period},
                    headers=HEADERS, timeout=180)
    if r.status_code == 404:  # no data published for this month
        return None
    r.raise_for_status()
    r.encoding = "utf-8"
    rows = list(csv.reader(io.StringIO(r.text), delimiter=";"))
    header, body = rows[0], rows[1:]
    # the server's endPeriod also returns the following month, keep only the requested one
    t = header.index("TIME_PERIOD")
    body = [row for row in body if row[t] == period]
    return header, body


def main():
    today = date.today()
    start = parse_ym(sys.argv[1]) if len(sys.argv) > 1 else (2005, 1)
    end = parse_ym(sys.argv[2]) if len(sys.argv) > 2 else (today.year, today.month)

    OUT_DIR.mkdir(exist_ok=True)
    session = requests.Session()
    saved = skipped = 0
    for y, m in months(start, end):
        period = f"{y}-{m:02d}"
        out = OUT_DIR / f"{period}.csv"
        if out.exists():
            skipped += 1
            continue
        result = fetch_month(session, period)
        if result is None:
            print(f"{period}: no data, skipping")
            continue
        header, body = result
        if not body:
            print(f"{period}: empty, skipping")
            continue
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";", lineterminator="\n")
            w.writerow(header)
            w.writerows(body)
        saved += 1
        print(f"{period}: {len(body):,} rows -> {out.name}")
        time.sleep(PAUSE)
    print(f"\nDone: {saved} saved, {skipped} already present, folder: {OUT_DIR}")


if __name__ == "__main__":
    main()
