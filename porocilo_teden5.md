Ta teden sem pripravil vizualizacije za analizo turističnega obiska v višje ležečih občinah in rezultate primerjal z obstoječimi analizami. Primerjam hotelske prenočitve v Južni Tirolski (ASTAT) in Švici (BFS) v letih 2013–2025. Za smučarske občine sem začasno vzel občine nad 1000 m in upošteval le občine z vsaj 95 % mesečnih podatkov (106 italijanskih, 171 švicarskih).

Osnovni vizualizaciji (02_osnovne_vizualizacije.ipynb):
Mesečne prenočitve skozi čas: obe državi imata zimski in poletni vrh. V Južni Tirolski je poletni vrh višji, v Švici zimski. Med covidom je bila zima 2020/21 v Italiji v celoti izgubljena, v Švici pa so smučišča ostala odprta.
Povprečni sezonski profil: v občinah nad 1000 m december–marec prinese okoli 46 % letnih prenočitev, v nižjih le 21 % (Italija) oz. 26 % (Švica).

Kompleksnejše vizualizacije (03_teden5_vizualizacije.ipynb):
Ena spremenljivka: histogram zimskega deleža po občinah. Južna Tirolska ima dve skupini občin (poletne okoli Merana in zimske v Dolomitih), Švica pa je zgoščena okoli 20–30 % zaradi mest.
Dve spremenljivki: nadmorska višina in zimski delež sta močno povezana (Spearman 0,71 v Italiji, 0,49 v Švici; okoli 2–3 odstotne točke več na 100 m).
Tri spremenljivke: razsevni diagram z velikostjo občine in toplotna karta leto × mesec × odstopanje od let 2013–2019. Na njej se poleg covida vidi, da april niha za ±30–45 % glede na datum velike noči, po letu 2022 pa so predsezona in posezona (maj, junij, oktober, november) 30–55 % nad ravnjo pred covidom.

Primerjava z obstoječimi analizami:
Uradne objave: naše spremembe se z BFS ujemajo na 0,3–2,5 odstotne točke (2020: −42,5 % proti −40,0 %; zima 2020/21: −28,9 % proti −26,4 %; 2024: +2,9 % proti +2,6 %). Naših 186 švicarskih občin pokriva okoli 80 % vseh švicarskih hotelskih prenočitev. Vsote za Južno Tirolsko (34,4 in 36,1 mio. v letih 2022 in 2023) so enake kot pri Eurac Research. Nova ugotovitev: švicarske občine nad 1000 m so pozimi 2020/21 izgubile le 8 % prenočitev, ker so domači gostje (po BFS +16,5 %) nadomestili tuje.
Znanstvena literatura (Falk 2010, Gonseth 2013, Steiger in sod. 2019) pravi, da so nižje ležeči kraji bolj odvisni od snega. V Južni Tirolski to potrdimo: zimske prenočitve nihajo iz leta v leto za 28 % pod 600 m, 12 % med 600 in 1000 m ter 8 % nad 1000 m, poletne pa povsod le 5–7 %. V Švici razlike ni, verjetno zaradi mest med nizkimi občinami in nezanesljivih višin iz Wikidata.

Naslednji koraki so popravek švicarskih višin, dokončna izbira višinskega praga in povezava z vremenskimi podatki (sneg), s katero bi učinek snega preverili neposredno.
