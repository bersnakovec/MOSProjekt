Ta teden sem nadaljeval z vizualizacijami in primerjavo z obstoječimi analizami, tokrat s poudarkom na razporeditvi prenočitev čez leto, ter zasnoval hipoteze in statistične teste (04_teden6_hipoteze.ipynb). Primerjam obdobje pred covidom (2013–2019) in po njem (2023–2025).

Obstoječe analize: Zbral sem šest virov o sezonskosti: poročila Eurac Research za Južno Tirolsko, ISTAT za vso Italijo, BFS za Švico, članek Serquet in Rebetez (2011) o vplivu poletne vročine na obisk Alp, Fernández-Morales (2003) o merjenju sezonskosti z Ginijevim koeficientom in južnotirolsko omejitev postelj (Bettenstopp). Naši podatki se z objavami ujemajo: v Južni Tirolski maj–oktober prinese 62 % prenočitev (Eurac okoli 60 %), avgust v Italiji 17,8 % (ISTAT 17,4 %), v Švici sta poletje 2025 in zima 2024/25 rekordni tako kot pri BFS (razmerje poletje/zima 1,32, BFS 1,35).

Vizualizacije:
Ginijev koeficient po letih: sezonska koncentracija v visokih občinah pada v obeh državah (Južna Tirolska z 0,35 na 0,32, Švica z 0,26 na 0,23).
Mesečni deleži pred in po covidu: pridobivajo junij, maj, oktober in december, izgubljata avgust (Južna Tirolska) in marec (obe državi).
Zimska in poletna sezona skozi čas: obe sezoni sta po covidu nad ravnjo 2014–2019. V Švici poletje raste hitreje od zime že od leta 2016.
Sprememba sezonskosti po občinah: sezonskost se je zmanjšala v 91 % visokih južnotirolskih in 80 % visokih švicarskih občin.

Hipoteze in testi: Zaradi majhnih vzorcev, asimetričnih porazdelitev in deležev sem izbral neparametrične teste (Spearman, Mann–Whitney, Kruskal–Wallis, Wilcoxon) z α = 0,05, Holm–Bonferronijevim popravkom za 9 testov in velikostjo učinka. Teste sem napisal z numpy in rezultate preveril s scipy.
H1 (višje občine imajo večji zimski delež): potrjena v obeh državah.
H2 (zimski delež visokih občin se med državama razlikuje): ni potrjena po popravku.
H3 (nižje občine so pozimi bolj nestanovitne, Falk 2010): potrjena za Južno Tirolsko, ne za Švico.
H4 (sezonskost je po covidu nižja): potrjena v obeh državah, najmočnejši rezultat.
H5 (poletje raste hitreje od zime): ni potrjena, ker v smučarskih občinah raste tudi zima.

Naslednji koraki so povezava z vremenskimi podatki (temperatura za junijski učinek, sneg za H3), popravek švicarskih višin in upoštevanje spreminjajoče se sezonskosti v napovednem modelu.
