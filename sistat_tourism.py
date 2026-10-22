"""
Download Slovenian tourism tables from SURS SiStat (PX-Web API) into tidy CSVs.

Usage:
    pip install requests pandas
    python sistat_tourism.py list                 # list tourism-related tables
    python sistat_tourism.py list overnight       # filter by your own keyword
    python sistat_tourism.py meta 2164408S        # show a table's dimensions
    python sistat_tourism.py get 2164408S         # download the full table -> 2164408S.csv

Table IDs in the examples are placeholders: run `list` first and pick real IDs.
The output is long format: one row per combination of dimensions + value,
which is what you want for pandas / LightGBM / statsmodels.
"""

import sys
import math
import time
import requests
import pandas as pd

BASE = "https://pxweb.stat.si/SiStatData/api/v1/{lang}/Data"
LANG = "sl"            # "sl" for Slovenian labels
MAX_CELLS = 100_000    # stay under the API's per-request cell limit
PAUSE = 1.0            # seconds between requests, be polite to the API

DEFAULT_KEYWORDS = ["tourist", "overnight", "accommodation", "tourism", "arrivals"]


def base_url():
    return BASE.format(lang=LANG)


def list_tables(keywords):
    r = requests.get(base_url() + "/", timeout=60)
    r.raise_for_status()
    rows = []
    for item in r.json():
        text = item.get("text", "")
        if any(k.lower() in text.lower() for k in keywords):
            rows.append((item.get("id", ""), item.get("updated", ""), text))
    for tid, updated, text in sorted(rows):
        print(f"{tid:<16} {updated[:10]:<11} {text}")
    print(f"\n{len(rows)} tables")


def table_url(table_id):
    if not table_id.endswith(".px"):
        table_id += ".px"
    return f"{base_url()}/{table_id}"


def get_meta(table_id):
    r = requests.get(table_url(table_id), timeout=60)
    r.raise_for_status()
    return r.json()


def show_meta(table_id):
    meta = get_meta(table_id)
    print(meta.get("title", ""))
    total = 1
    for v in meta["variables"]:
        n = len(v["values"])
        total *= n
        sample = ", ".join(v["valueTexts"][:5])
        print(f"  {v['code']:<30} {n:>6} values   e.g. {sample}")
    print(f"\nTotal cells: {total:,}")


def find_time_var(variables):
    for v in variables:
        if v.get("time"):
            return v
    # fallback: SiStat often names it MESEC / LETO / month / year
    for v in variables:
        if v["code"].upper() in ("MESEC", "LETO", "MONTH", "YEAR", "ČETRTLETJE"):
            return v
    # last resort: the dimension with the most values
    return max(variables, key=lambda v: len(v["values"]))


def fetch_chunk(table_id, variables, time_var, time_values):
    query = []
    for v in variables:
        values = time_values if v["code"] == time_var["code"] else v["values"]
        query.append({
            "code": v["code"],
            "selection": {"filter": "item", "values": values},
        })
    body = {"query": query, "response": {"format": "json"}}
    r = requests.post(table_url(table_id), json=body, timeout=300)
    r.raise_for_status()
    return r.json()


def to_frame(payload, variables):
    # map value codes to readable labels
    labels = {v["code"]: dict(zip(v["values"], v["valueTexts"])) for v in variables}
    dim_cols = [c for c in payload["columns"] if c["type"] in ("d", "t")]
    val_cols = [c for c in payload["columns"] if c["type"] == "c"]

    records = []
    for row in payload["data"]:
        rec = {}
        for col, key in zip(dim_cols, row["key"]):
            rec[col["code"]] = labels.get(col["code"], {}).get(key, key)
            rec[col["code"] + "_code"] = key
        for col, val in zip(val_cols, row["values"]):
            rec[col["text"] or col["code"]] = val
        records.append(rec)
    df = pd.DataFrame.from_records(records)

    # SiStat uses symbols like "-", "...", "z" for missing / confidential
    for col in val_cols:
        name = col["text"] or col["code"]
        df[name] = pd.to_numeric(df[name], errors="coerce")
    return df


def download(table_id):
    meta = get_meta(table_id)
    variables = meta["variables"]
    time_var = find_time_var(variables)

    other_cells = 1
    for v in variables:
        if v["code"] != time_var["code"]:
            other_cells *= len(v["values"])

    if other_cells > MAX_CELLS:
        sys.exit(
            f"A single time period has {other_cells:,} cells, above the "
            f"{MAX_CELLS:,} limit. Narrow another dimension in the code first."
        )

    per_chunk = max(1, MAX_CELLS // other_cells)
    tvals = time_var["values"]
    n_chunks = math.ceil(len(tvals) / per_chunk)
    print(f"{meta.get('title', table_id)}")
    print(f"Time variable: {time_var['code']} ({len(tvals)} periods), "
          f"{n_chunks} request(s)")

    frames = []
    for i in range(n_chunks):
        chunk = tvals[i * per_chunk:(i + 1) * per_chunk]
        payload = fetch_chunk(table_id, variables, time_var, chunk)
        frames.append(to_frame(payload, variables))
        print(f"  chunk {i + 1}/{n_chunks}: {chunk[0]} .. {chunk[-1]}")
        time.sleep(PAUSE)

    df = pd.concat(frames, ignore_index=True)
    out = f"{table_id.replace('.px', '')}.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df):,} rows -> {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "list":
        list_tables(sys.argv[2:] or DEFAULT_KEYWORDS)
    elif cmd == "meta":
        show_meta(sys.argv[2])
    elif cmd == "get":
        download(sys.argv[2])
    else:
        print(__doc__)