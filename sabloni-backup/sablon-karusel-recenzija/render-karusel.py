# Render šablona karusela u 5 PNG slajdova 1080x1350.
# Upotreba (iz foldera šablona): python3 render-karusel.py <repo-sajta> <slug> <izlazni-prefiks>
# Pre rendera popuni CONFIG u karusel.html. Slike se same uzimaju iz posta (heroMobile, heroDesktop).
import sys, os, json, shutil, asyncio, threading, http.server, functools
from PIL import Image
repo, slug, out = sys.argv[1], sys.argv[2], sys.argv[3]
here=os.path.dirname(os.path.abspath(__file__)); site=os.path.join(here,'_site')
os.makedirs(os.path.join(site,'styles'),exist_ok=True); os.makedirs(os.path.join(site,'img'),exist_ok=True)
for f in ('post-shared.css','post-mobile.css','post-desktop.css','home-card.css','aurora.css'):
    shutil.copy(os.path.join(repo,'src/styles',f),os.path.join(site,'styles',f))
shutil.copytree(os.path.join(repo,'src/assets/fonts/inter'),os.path.join(site,'assets/fonts/inter'),dirs_exist_ok=True)
shutil.copytree(os.path.join(repo,'public/fonts/neometric-alt'),os.path.join(site,'fonts/neometric-alt'),dirs_exist_ok=True)
shutil.copy(os.path.join(repo,'public/fonts/neometric-alt.css'),os.path.join(site,'fonts/'))
post=json.load(open(os.path.join(repo,'src/content/posts',slug+'.json'),encoding='utf-8'))
def img(rel,name):
    p=os.path.normpath(os.path.join(repo,'src/content/posts',rel)); Image.open(p).convert('RGB').save(os.path.join(site,'img',name),quality=95)
img(post['heroMobile'],'hero-mobile.jpg'); img(post['heroDesktop'],'hero-desktop.jpg')
shutil.copy(os.path.join(here,'karusel.html'),os.path.join(site,'index.html'))
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8767),functools.partial(http.server.SimpleHTTPRequestHandler,directory=site))
threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--font-render-hinting=none'])
        pg=await b.new_page(viewport={'width':2150,'height':538},device_scale_factor=1080/430)
        await pg.goto('http://127.0.0.1:8767/index.html'); await pg.evaluate('document.fonts.ready'); await pg.evaluate('window.wordsReady'); await pg.wait_for_timeout(800)
        await pg.screenshot(path=os.path.join(here,'_strip.png')); await b.close()
asyncio.run(main())
im=Image.open(os.path.join(here,'_strip.png')).convert('RGB')
for i in range(5): im.crop((i*1080,0,(i+1)*1080,1350)).save(f'{out}-{i+1}.png')
print('gotovo:',[f'{out}-{i+1}.png' for i in range(5)])
