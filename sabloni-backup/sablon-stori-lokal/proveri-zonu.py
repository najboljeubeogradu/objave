# Provera jedinstvene sigurne zone (stori + Reels + isečak 4:5 u feedu).
# Upotreba (iz foldera šablona): python3 proveri-zonu.py <putanja-do-repoa-sajta> [kadrovi.png]
# Meri stvarne piksele sadržaja (razlika prema samoj pozadini) svakih 0,2 s, bez poslednjih 0,6 s (pretapanje)
# i bez uletanja stikera sleva (1,35–2,25 s, samo leva ivica).
# Zona (px na 1080x1920): gore >= 300, dole <= 1500, levo >= 60, desno <= 1020; ispod y 1100 desno <= 940 (dugmad u Reelsu).
import sys, os, io, shutil, asyncio, threading, http.server, functools
import numpy as np
from PIL import Image, ImageDraw
repo = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__)); site = os.path.join(here, '_site')
os.makedirs(os.path.join(site, 'styles'), exist_ok=True)
for f in ('post-shared.css', 'post-mobile.css', 'post-desktop.css', 'site-header-mobile.css', 'aurora.css'):
    shutil.copy(os.path.join(repo, 'src/styles', f), os.path.join(site, 'styles', f))
shutil.copytree(os.path.join(repo, 'src/assets/fonts/inter'), os.path.join(site, 'assets/fonts/inter'), dirs_exist_ok=True)
shutil.copytree(os.path.join(repo, 'public/fonts/neometric-alt'), os.path.join(site, 'fonts/neometric-alt'), dirs_exist_ok=True)
shutil.copy(os.path.join(repo, 'public/fonts/neometric-alt.css'), os.path.join(site, 'fonts/'))
shutil.copy(os.path.join(here, 'stori-lokal.html'), os.path.join(site, 'index.html'))
for f in os.listdir(here):
    if f.lower().endswith('.png'): shutil.copy(os.path.join(here, f), site)
class Tih(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8767), functools.partial(Tih, directory=site))
threading.Thread(target=srv.serve_forever, daemon=True).start()
TOP, BOT, LEFT, RIGHT, COLY, COLX = 300, 1500, 60, 1020, 1100, 940

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--font-render-hinting=none']); f = 1080/430
        a = await b.new_page(viewport={'width': 430, 'height': 765}, device_scale_factor=f)
        c = await b.new_page(viewport={'width': 430, 'height': 765}, device_scale_factor=f)
        for pg in (a, c):
            await pg.goto('http://127.0.0.1:8767/index.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(800)
        await c.add_style_tag(content='#stage > *:not(.glow):not(.bg){visibility:hidden!important}')
        tot = await a.evaluate('TOTAL'); env = np.zeros((1920, 1080), bool); bad = []; t = 0.0
        async def shot(pg, t):
            await pg.evaluate(f'seek({t})')
            return np.asarray(Image.open(io.BytesIO(await pg.screenshot())).convert('L'), dtype=int)[:1920, :1080]
        while t < tot - 0.6:
            m = np.abs((await shot(a, t)) - (await shot(c, t))) > 40
            ys, xs = np.where(m)
            if len(ys):
                entering = 1.35 <= t < 2.25
                errs = []
                if ys.min() < TOP: errs.append(f'gore {ys.min()}')
                if ys.max() > BOT: errs.append(f'dole {ys.max()}')
                if not entering and xs.min() < LEFT: errs.append(f'levo {xs.min()}')
                if xs.max() > RIGHT: errs.append(f'desno {xs.max()}')
                if m[COLY:, COLX+1:].any(): errs.append('kolona dugmadi Reelsa')
                if errs: bad.append(f'{t:.1f} s: ' + ', '.join(errs))
                if not entering: env |= m
            t = round(t + 0.2, 2)
        ys, xs = np.where(env)
        print(f'sadržaj: gore {ys.min()}, dole {ys.max()} ({1919-ys.max()} od dna), levo {xs.min()}, desno {xs.max()} ({1079-xs.max()} od desne)')
        if len(sys.argv) > 2:
            fr = []
            for t in (3.0, 7.2, 11.0):
                await a.evaluate(f'seek({t})'); im = Image.open(io.BytesIO(await a.screenshot())).convert('RGBA').crop((0, 0, 1080, 1920))
                ov = Image.new('RGBA', im.size); d = ImageDraw.Draw(ov)
                d.rectangle((0, 0, 1080, TOP), fill=(255, 60, 60, 70)); d.rectangle((0, BOT, 1080, 1920), fill=(255, 60, 60, 70))
                d.rectangle((COLX, COLY, 1080, BOT), fill=(255, 60, 60, 70)); d.rectangle((3, 285, 1077, 1635), outline=(255, 210, 0, 255), width=6)
                im.alpha_composite(ov); fr.append(im)
            pv = Image.new('RGB', (3280, 1920), 'white')
            for i, im in enumerate(fr): pv.paste(im, (i*1100, 0))
            pv.resize((1640, 960)).save(sys.argv[2])
        await b.close()
        print('\n'.join(bad) if bad else 'OK: sav sadržaj je u zajedničkoj sigurnoj zoni (stori, Reels, 4:5)')
asyncio.run(main())
