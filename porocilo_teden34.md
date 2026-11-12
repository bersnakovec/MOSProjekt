 	

Ukvarjal sem se s pridobivanjem in pripravo podatkov za primerjavo turističnega obiska v višje ležečih občinah (smučarska središča). Slovenske podatke SURS smo zaradi premalo podatkov opustili in se osredotočili na Italijo in Švico.

Pridobivanje podatkov: Napisal sem skripte, ki samodejno prenesejo mesečne podatke o prihodih in prenočitvah po občinah:
Južna Tirolska (ASTAT, 2005–2026, 261 mesečnih datotek),
Švica (BFS, 2013–2026, 164 mesečnih datotek, po državah izvora gostov),
vsa Italija (ISTAT, mesečno 2022–2025 in letno 2014–2025).
Nadmorske višine: Iz Wikidata sem pripravil tabelo višin za italijanske občine in švicarske občine. Za Italijo so pokrite skoraj vse občine, pri Švici pa so višine za 52 občin dvoumne in jih je treba še popraviti.
Združen nabor podatkov: V Jupyter zvezku (01_build_dataset.ipynb) sem tri vire očistil in združil v eno tabelo z 209.568 vrsticami. Pri tem sem izločil seštevke okrajev, manjkajoče vrednosti obravnaval kot manjkajoče in ne kot nič ter švicarske občine povezal z uradnimi šiframi.
Preverjanje: Podatki ASTAT in ISTAT za Južno Tirolsko se ujemajo (razmerje 1,00), zato je treba pri združevanju Italije paziti na dvojno štetje.

Naslednji koraki so popravek višin za Švico, določitev višinskega praga in prva analiza ter vizualizacija sezonskih vzorcev.