"""
Build a municipality elevation reference table from Wikidata.

Usage:
    pip install requests
    python elevation.py

Writes data/reference/elevation.csv with columns:
    country (IT|CH), muni_id, name, elev_min_m, elev_max_m, n_values

IT: muni_id is the ISTAT code (Wikidata P635), which also matches ASTAT's TOUR_GEO.
CH: muni_id is the BFS commune number (Wikidata P771), which matches the codes in the
    BFS PxWeb table (the downloaded CSVs only contain names).

Wikidata sometimes holds several elevations per municipality (centre vs. lowest/highest
point), so min and max are both kept; check rows with n_values > 1 before relying on them.
"""

import csv
from collections import defaultdict
from pathlib import Path

import requests

SPARQL = "https://query.wikidata.org/sparql"
HEADERS = {"Accept": "text/csv",
           "User-Agent": "MOS-student-project/1.0 (university coursework)"}
OUT = Path(__file__).parent / "data" / "reference" / "elevation.csv"

QUERIES = {
    "IT": ('SELECT ?id ?elev ?label WHERE { ?c wdt:P31/wdt:P279* wd:Q747074; '
           'wdt:P635 ?id; wdt:P2044 ?elev. ?c rdfs:label ?label FILTER(LANG(?label)="it") }'),
    "CH": ('SELECT ?id ?elev ?label WHERE { ?c wdt:P771 ?id; wdt:P2044 ?elev. '
           '?c rdfs:label ?label FILTER(LANG(?label)="de") }'),
}


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for country, query in QUERIES.items():
        # POST on purpose: GET responses from the query service come back silently truncated
        r = requests.post(SPARQL, data={"query": query}, headers=HEADERS, timeout=180)
        r.raise_for_status()
        elev, names = defaultdict(set), {}
        for rec in csv.DictReader(r.content.decode("utf-8").splitlines()):
            elev[rec["id"]].add(float(rec["elev"]))
            names[rec["id"]] = rec["label"]
        for muni_id, values in sorted(elev.items()):
            rows.append([country, muni_id, names[muni_id],
                         min(values), max(values), len(values)])
        print(f"{country}: {len(elev):,} municipalities")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["country", "muni_id", "name", "elev_min_m", "elev_max_m", "n_values"])
        w.writerows(rows)
    print(f"Saved {len(rows):,} rows -> {OUT}")


if __name__ == "__main__":
    main()
