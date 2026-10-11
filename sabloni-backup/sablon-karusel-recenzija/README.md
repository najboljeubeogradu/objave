# Šablon: karusel o recenziji (5 slajdova, 4:5) — KONAČNI, zaključan 5.10.2026

Referenca: karusel za sendvič Rapsodija (Babalu), fajlovi sajt-final-1…5. Za svaki sledeći specijalitet menja se SAMO blok `window.CONFIG` u `karusel.html`; raspored, tipografija i grafika ostaju. Ton: informišemo, ne reklamiramo (bez hvaljenja, prikazuju se i "za koga nije").

## Slajdovi
1. Hero-mobile slika preko celog slajda (cela, 4:5). Gore levo naslov "za koga je / <vrsta jela>" (stil `.t10-head__title`), gore desno nalepnica sa imenom lokala (plavo) i pin + opština. Dole velika reč (naziv jela + "?") koja prelazi na slajd 2.
2. Pločice sa posta `.m-vtile`: "Za koga je" / "Za koga nije", centrirane između velikih reči.
3. i 4. JEDNA hero-desktop slika preko oba slajda (cela, bez sečenja), jelo tačno na prelazu; spoljne ivice tamne ka pozadini.
   - 3 (levo od jela): lista Nivo cene / Radno vreme / Adresa — ikonica u plavom krugu, oznaka (Inter 11px, velika slova), vrednost (Neometric 700), dopuna (Inter).
   - 4 (desno od jela): prosečna ocena X.X/5 i prsten sa procentom ("NARUČILO BI PONOVO"), isti stil natpisa, centrirano.
5. Veliki "?", oznaka "KVIZ · 3 PITANJA", "kviz, ocene i svi utisci su na sajtu", plavo dugme "link u bio", adresa najboljeubeogradu.rs kao običan tekst.

Vezni element: velike reči u obrisu (kao rang brojevi na Top 10) preko ivica slajdova: `<jelo>?` (1|2, dole), `cena` (2|3, gore), `kviz` (4|5, gore). Granica između slova pada tačno na ivicu slajda (računa se samo). Bez logotipa sajta. Pozadina: Aurora + blago zrno.

## Pravila
- Nijedan ispis ne sme preko jela (ni čačkalice). Posle rendera obavezno `python3 proveri-hranu.py`; ako javi preklapanje, podesi `raspored` u CONFIG (veličina naslova, položaj nalepnice, pomak desktop slike) ili skrati tekst.
- Slike se ne seku. Razmak slova u naslovima +0.01em (slova se ne dodiruju).
- Brojke samo iz Supabase `get_post_feedback(slug)`; tekstovi "za koga je/nije", cena, plaćanje, radno vreme, adresa iz `src/content/posts/<slug>.json`.

## Kad jelo zauzima drugačiji deo slike (primer: šiš ćevap, 6.10.2026)
Dizajn ostaje isti; menja se samo raspored, i to samo toliko koliko je potrebno da ispisi ostanu na pozadini:
- velika reč može da ide gore ili dole (`data-y`) i da se podeli na drugom slovu (`data-split`, `recPodela`); reč koja ne može da pređe preko jela staje tačno na ivici slajda;
- na slajdovima 3–4 lista i ocene prate praznu pozadinu (npr. kod dijagonalnog jela: lista gore levo, ocena i prsten jedno pored drugog dole desno);
- naslov na slajdu 1 sme da bude kraći, ako se čita zajedno sa velikom rečju ("za koga je šiš" + "ćevap?");
- duže ime lokala na nalepnici ide u dva reda (`<br>`), manjim slovima.
`proveri-hranu.py` meri stvarne linije teksta i grafičke elemente (ne prazne kutije).

## Postupak
1. Popuni CONFIG u `karusel.html`.
2. `python3 render-karusel.py <repo-sajta> <slug> <izlaz>` → `<izlaz>-1.png` … `-5.png`
3. `python3 proveri-hranu.py` i `python3 proveri-slova.py` → oba moraju "OK" (nijedan ispis preko jela; velike reči se ne preklapaju sa tekstom i nijedno slovo nije presečeno ivicom slajda).
4. Pogledaj svih 5 slajdova; dopuni "gotove-objave.md".
