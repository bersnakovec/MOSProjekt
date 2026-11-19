# Dodajanje novih podatkov (npr. nove države)

## Kako tečejo podatki

```
1. Prenos (skripte v korenu projekta)
   astat_tourism.py  -> astat_tourism_monthly/*.csv
   istat_tourism.py  -> istat_tourism/*.csv
   bfs_tourism.py    -> bfs_tourism_monthly/*.csv
   elevation.py      -> data/reference/elevation.csv

2. Združevanje
   notebooks/01_build_dataset.ipynb -> data/processed/tourism_monthly.csv

3. Analiza
   notebooks/02, 03, 04 ... berejo SAMO data/processed/tourism_monthly.csv
```

## Pravila

1. **Surovih podatkov ne spreminjamo.** Kar prenese skripta, ostane tako, kot je prišlo z vira.
2. **V `data/processed/` ne pišemo ročno.** Zvezek 01 ob vsakem zagonu prepiše `tourism_monthly.csv`, zato bi ročno dodane vrstice izginile. Vse, kar je v `processed`, mora nastati s kodo.
3. **Vsak vir ima svojo skripto za prenos in svojo mapo** (`<vir>_tourism.py` -> `<vir>_tourism_monthly/`).
4. **Občine povezujemo z uradnimi šiframi, ne z imeni.** Imena se ob združitvah občin spreminjajo.
5. **Manjkajoča vrednost je `NaN`, ne 0.** Zaupni podatki (`..`, `...`, `c`) niso nič.
6. Koda, komentarji in izpisi so v angleščini, besedilo v zvezkih in README v slovenščini.

## Koraki za nov vir

### 1. Skripta za prenos

Nova skripta v korenu, npr. `statat_tourism.py` za Statistik Austria. Kot vzor vzemite `bfs_tourism.py` ali `astat_tourism.py`:
- prenese mesečne podatke po občinah (prihodi, prenočitve; če obstaja, posebej hoteli);
- shrani eno datoteko na mesec v svojo mapo, npr. `statat_tourism_monthly/2024-01.csv`;
- preskoči datoteke, ki že obstajajo (ponovni zagon samo doda nove mesece);
- se zažene s `python statat_tourism.py`.

### 2. Nadmorske višine

V `elevation.py` dodajte poizvedbo za novo državo (koda države, npr. `AT`, in uradna šifra občine iz Wikidata). Nato znova zaženite `python elevation.py`. Preverite, koliko občin ima več različnih višin (stolpec `n_values`); pri Švici je to veliko.

### 3. Razdelek v `01_build_dataset.ipynb`

Dodajte razdelek (markdown naslov + celica), ki surove datoteke pretvori v tabelo z **natanko temi stolpci**:

| Stolpec | Pomen | Primer |
|---|---|---|
| `country` | dvočrkovna koda države | `AT` |
| `source` | ime vira | `STATAT` |
| `scope` | `hotel` (samo hoteli) ali `all` (vse nastanitve) | `hotel` |
| `muni_id` | uradna šifra občine, **kot niz** (vodilne ničle!) | `70101` |
| `muni_name` | ime občine | `Innsbruck` |
| `region` | dežela/regija, če je na voljo, sicer prazno | `Tirol` |
| `date` | prvi dan meseca | `2024-01-01` |
| `arrivals` | prihodi | `12345` |
| `overnights` | prenočitve | `45678` |
| `beds` | postelje, če so na voljo, sicer prazno | |

Če vir ima oboje, naredite dve skupini vrstic: eno s `scope="hotel"` in eno s `scope="all"`.

Nato tabelo dodajte v obstoječo vrstico:

```python
df = pd.concat([astat, istat, bfs, statat], ignore_index=True)
```

Višine, `year` in `month` se dodajo samodejno. Zaženite celoten zvezek 01 od začetka (*Restart & Run All*).

### 4. Preverjanje

V razdelku *Preverjanje* na koncu zvezka 01 preverite za nov vir:
- število občin in obdobje (prvi in zadnji mesec);
- delež manjkajočih prenočitev in občin brez višine;
- ali se letne vsote ujemajo z uradno objavo vira (npr. letno poročilo statističnega urada). Razlika do nekaj odstotkov je normalna (zaupne občine), večja pomeni napako.

### 5. Analitični zvezki (02, 03, 04)

Države so v vsakem zvezku določene na enem mestu, v prvi celici s kodo:

```python
COUNTRIES = {"IT": "Italija (Južna Tirolska)", "CH": "Švica"}
```

Za novo državo dodajte njeno kodo (enako kot v stolpcu `country`) in ime, npr. `"AT": "Avstrija"`. Barva se dodeli samodejno iz `PALETTE`, grafi dobijo dodatno ploščo, testi pa se izvedejo tudi za novo državo (H2 za vsak par držav). Zvezek zaženite od začetka in preverite, da so grafi še berljivi.

Izjema so primerjave z uradnimi objavami (BFS, ISTAT, Eurac) v zvezkih 03 in 04: te so vezane na konkreten vir, zato za novo državo dodajte svojo primerjavo z objavo njenega statističnega urada.

Analize uporabljajo hotelske podatke (`scope="hotel"`), zato država brez hotelskega dela v grafih ne bo prikazana.

## Na kaj paziti

- **Hoteli proti vsem nastanitvam.** Švica (BFS) ima samo hotele. Če nov vir primerjamo s Švico, mora imeti tudi `scope="hotel"`.
- **Dvojno štetje.** Če nov vir pokriva isto območje kot obstoječi (kot ISTAT in ASTAT za Južno Tirolsko), ga pred seštevanjem izločite.
- **Zadnji mesec je pogosto nepopoln.** Ne uporabljajte zadnjega leta za primerjave.
- **Kodiranje znakov.** Datoteke shranite v UTF-8 (npr. BFS pošilja Windows-1252, skripta to pretvori).
- **Omejitve API-jev.** Nekateri viri omejujejo število zahtev (BFS vrne HTTP 429). Skripta naj počaka in poskusi znova.
- Ko je vir dodan, ga vpišite v tabelo *Data* v `CLAUDE.md` in v `PLAN.md`.
