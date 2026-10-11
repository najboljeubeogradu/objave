# Šablon: stori i Reels za lokale (poziv na ocenjivanje) — KONAČNI, standard od 9.10.2026

JEDNA VERZIJA ZA SVE (standard od 9.10.2026): isti MP4 ide u stori, u Reels i u feed (isečak 4:5), bez posebnih verzija. Sav sadržaj je u zajedničkoj sigurnoj zoni (vidi dole). Iz istog fajla se renderuju dve varijante (CONFIG.varijanta): 'stori' sa poljem "ovde nalepi link" (za link sticker) i 'reels' sa trakom sa adresom sajta na istom mestu (za Reels i feed, gde link ne može).

Referentni video: stori-babalu-oceni-v4 (Babalu, sendvič Rapsodija). Za svaki sledeći lokal menjaju se SAMO tekst i stiker (+ ocena i procenat iz Supabase); raspored, animacija, muzika, efekti i balans zvuka se ne diraju.

Video 9:16 (1080×1920, 13 s, 30 fps, sa muzikom) koji lokal objavljuje na svom profilu (stori ili Reels), a može i na naš feed. Prvi put napravljen za Babalu (sendvič Rapsodija), 5.10.2026.
Menjaju se SAMO tekst pitanja, brojke i stiker. Raspored, animacija, muzika i efekti ostaju isti.

## Šta se menja za novi lokal
1. U `stori-lokal.html`, blok `window.CONFIG` na vrhu skripte:
   - `pitanje`: 4 reda, `<br>` između redova, `&nbsp;` da kratka reč ne ostane sama. Malim slovima. Ime lokala u `<span class="hl">…</span>` da bude plavo (boja sa sajta #00AEEF), npr. `u&nbsp;<span class="hl">babalu</span>?`.
   - `ocena`: `ratings.score` iz Supabase `get_post_feedback('<slug>')` (prikaz sa 1 decimalom, kao na sajtu).
   - `procenat`: `returnVote.percent` iz iste funkcije (zaokružuje se, kao na sajtu).
   - `pozadina`: 'tamna' (osnovna, #0C0E12) ili 'pink' (opcija 2, #B8005F, preliv #C8076B → #B0005C → #98004F). Menja se samo pozadina, svi elementi ostaju isti.
   - `varijanta`: 'stori' ili 'reels' (renderuju se obe, npr. stori-<lokal>-oceni.mp4 i reels-<lokal>-oceni.mp4).
   - `stiker`: ime PNG fajla u folderu šablona. Veličina stikera se sama prilagodi odnosu stranica slike (okviri BOX1 i BOX3 u skripti), ručno se ne podešava.
2. Stiker: `python3 napravi-stiker.py <slika-posta> sticker.png` (izrez jela + bela ivica). Za izvor uzeti sliku na kojoj je jelo celo i oštro (card ili galerija). Proveriti izrez pre rendera.
3. Provera zone: `python3 proveri-zonu.py <putanja-do-repoa-sajta> zona.png` mora da vrati "OK" (meri stvarne piksele svakih 0,2 s; zona.png su kadrovi 3,0 / 7,2 / 11,0 s sa ucrtanim zonama).
4. Naslovna (obavezna za varijantu 'reels', standard od 10.10.2026): `naslovna-reels-<lokal>-oceni.jpg`, 1080×1920, po pravilima iz `claude/dizajn-sistem.md`, odeljak "Naslovna za Reels". Hero slika posta preko celog kadra, dole naziv specijaliteta, plava crta, naziv lokala, logo. Sav tekst u zoni gore ≥ 300, dole ≤ 1620, sa strana ≥ 60. Varijanta 'stori' nema naslovnu.
5. Statične kadrove (t = 3.0 / 7.2 / 11.0 s) i naslovnu poslati na odobrenje, pa tek onda render: `python3 render.py <putanja-do-repoa-sajta> stori-<lokal>-oceni.mp4`
6. Objava Reelsa preko Metricool-a: naslovna se zadaje kao `videoThumbnailUrl` (javni URL), za IG Reel i FB Reel. Posle objave proveriti pločicu u mreži oba profila.

Posle rendera dopuniti "gotove-objave.md" (uz video i ime naslovne).

## Raspored (ne menja se)
- Kadar 1 (0–3,3 s): pitanje centrirano, Neometric Alt 900 (`.m-h1`), 45 px na 430 px širine, razmak slova +0.01em, nagnuto −5° kao stiker, počinje na ~300 px; ispod veliki stiker (uleće sleva, njiše se), u okviru 300×214 css px.
- Kadar 2 (3,9–8 s): gore levo "trenutne / ocene / na sajtu" ("ocene" plavo), ispod logo (`.shm-logo`) na nalepnici (kartica sa sajta + bela ivica) koja iskoči i diše (period 2 s), centrirano u bloku, nagnuto −5°; gore desno manji stiker (isti stiker doplovi iz kadra 1); dole `.dm-vres` (prosečna ocena, X.X/5) i `.dm-ring` (procenat u krugu, zoom .56, natpis "NARUČILO BI PONOVO" 21 px; ceo red odmaknut 34 css px od desne ivice da krug ne ulazi u kolonu dugmadi Reelsa) sa desktop verzije sajta, broje kao na sajtu (1,1 s i 2 s); natpisi ispod brojeva uvećani i podebljani radi čitljivosti.
- Kadar 3 (8,45–13 s): "oceni i ti!" ("ti" plavo) centrirano, nagnuto +4°; stiker ponovo naraste (okvir 300×226 css px); plava munja (52×80 css px) pokazuje na polje za link i udara nadole na svaki takt.
- Polje za link sticker: 600×110 px, na sredini, 1383–1494 px od vrha, sve vreme; diskretan ispis "• OVDE NALEPI LINK" sa isprekidanim okvirom (procena veličine Instagram link stickera). U storiju lokal preko njega nalepi link sticker. U varijanti 'reels' na istom mestu je traka sa adresom: pill kao kartica sa sajta, logo `.shm-logo` + plavo dugme sa strelicom (gradijent kao `.m-quiz__share`).
- Prelazi bez smene cele slike: slova odlaze unazad u zamućenje, stiker vodi kroz ceo video. Pozadina: Aurora sa sajta (`aurora.css`), blago živa. Poslednjih 0,6 s meko pretapanje u pozadinu.
- Zajednička sigurna zona (px na 1080×1920), proverava je `proveri-zonu.py`:
  - gore ≥ 300 (isečak 4:5 u feedu počinje na 285, stori traži 250);
  - dole ≤ 1500, tj. 420 od dna (opis i ime naloga u Reelsu; stori traži 340, isečak 4:5 završava na 1635);
  - sa strana ≥ 60;
  - ispod 1100 px od vrha desno najviše do 940 (kolona dugmadi u Reelsu: srce, komentar, deli).
  Izuzeci koje provera ne broji: uletanje stikera sleva (1,35–2,25 s) i poslednjih 0,6 s (pretapanje).

## Zvuk (`zvuk.py`, generisan, bez tuđih semplova)
Muzika 120 BPM (Am–F–C–G, kik, klap, hat, of-bit bas, pad, sidechain), utišava se na kraju. Efekti (odobreno 5.10.2026): kratak čist klik kad stiker sleti i na oba reza (1,62 / 3,95 / 8,45 s); odbrojavanje dok se ocene učitavaju (tik na svakih 4% prstena, usporava kao brojač na sajtu, "ding" kad se napuni; procenat se sam čita iz CONFIG); munja = električno pražnjenje (zujanje + varnice na svaki takt, 9,15–12,6 s).
Miks: muzika bez <30 Hz, efekti bez <140 Hz; svaki efekat se automatski poravna prema muzici na svom mestu (kratki po vrhu −6 dB, dugi po glasnoći, vrh najviše −6 dB); muzika se blago povuče najviše 2 dB ispod efekta; meki limiter; ukupno −14 LUFS, vrh ispod −1 dBTP.

## Link za lokal
Stori: `https://www.najboljeubeogradu.rs/<slug>/?utm_source=instagram&utm_medium=story&utm_campaign=lokal-<lokal>` (link sticker preko polja "ovde nalepi link").
Reels: link ne može u video; ide u opis kao tekst ili lokal upućuje na najboljeubeogradu.rs.
