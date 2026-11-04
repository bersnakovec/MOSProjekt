"""
Download Italian municipal tourism data from ISTAT and write tidy long CSVs.

Source: ISTAT "Occupancy in collective accommodation establishments at municipality level"
        (bulk file DCSC_Occupancy_in_collective_accommodation.zip on esploradati.istat.it)

Usage:
    pip install requests openpyxl
    python istat_tourism.py

Writes to istat_tourism/:
    monthly_municipal.csv  year, region, province, municipality, istat_code, flag,
                           indicator (arrivals|nights), month, value
                           (all accommodation types, 2022-2025)
    annual_municipal.csv   one row per municipality and year, columns
                           {arrivals|nights}_{total|hotel|other}_{residents|non_residents|total}
                           (2014-2025)

Municipalities whose data is confidential are absent from the source, and suppressed
cells "(*)" become empty values. From 2025 the totals include privately rented
accommodation, so non-hotel and total figures are not comparable with earlier years.
"""

import csv
import io
import zipfile
from pathlib import Path

import openpyxl
import requests

URL = ("https://esploradati.istat.it/databrowser/DWL/Servizi/"
       "DCSC_Occupancy_in_collective_accommodation.zip")
MEMBER = "2_dati_comunali.xlsx"
OUT_DIR = Path(__file__).parent / "istat_tourism"

ID_COLS = ["year", "region", "province", "municipality", "istat_code", "flag"]
ACCOMMODATION = ["total", "hotel", "other"]
RESIDENCE = ["residents", "non_residents", "total"]


def clean(v):
    """Numeric cell -> int; suppressed / missing markers -> None."""
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).strip().replace(".", "") if v is not None else ""
    return int(s) if s.lstrip("-").isdigit() and s != "-" else None


def is_data_row(row):
    return isinstance(row[0], int) and row[6] is not None


def ids(row):
    return [row[0], row[2], row[4], row[5], row[6], row[7] or ""]


def write_monthly(ws, path):
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(ID_COLS + ["indicator", "month", "value"])
        for row in ws.iter_rows(values_only=True):
            if not is_data_row(row):
                continue
            for k, indicator in enumerate(["arrivals", "nights"]):
                for month in range(12):
                    value = clean(row[8 + 12 * k + month])
                    w.writerow(ids(row) + [indicator, month + 1, value])
                    n += 1
    return n


def write_annual(ws, path):
    """Wide format: one row per municipality and year, 18 value columns."""
    columns = [f"{ind}_{acc}_{res}"
               for ind in ("arrivals", "nights")
               for acc in ACCOMMODATION
               for res in RESIDENCE]
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(ID_COLS + columns)
        for row in ws.iter_rows(values_only=True):
            if not is_data_row(row):
                continue
            w.writerow(ids(row) + [clean(row[8 + i]) for i in range(len(columns))])
            n += 1
    return n


def main():
    print("Downloading ISTAT bulk file (~17 MB)...")
    r = requests.get(URL, timeout=300)
    r.raise_for_status()
    wb = openpyxl.load_workbook(
        io.BytesIO(zipfile.ZipFile(io.BytesIO(r.content)).read(MEMBER)), read_only=True)
    annual = next(ws for ws in wb.worksheets if "annual" in ws.title.lower())
    monthly = next(ws for ws in wb.worksheets if "mensili" in ws.title.lower())

    OUT_DIR.mkdir(exist_ok=True)
    print(f"monthly: {write_monthly(monthly, OUT_DIR / 'monthly_municipal.csv'):,} rows")
    print(f"annual:  {write_annual(annual, OUT_DIR / 'annual_municipal.csv'):,} rows")
    print(f"Saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
