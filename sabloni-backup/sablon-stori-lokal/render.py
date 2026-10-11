# Render šablona u MP4 1080x1920, 30 fps, sa zvukom.
# Upotreba (iz foldera šablona): python3 render.py <putanja-do-repoa-sajta> izlaz.mp4
# Folder mora da sadrži: stori-lokal.html, sticker.png (ili ime iz CONFIG.stiker), zvuk.py
import sys, os, shutil, subprocess, asyncio, threading, http.server, functools
repo, out = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__)); site = os.path.join(here, '_site')
os.makedirs(os.path.join(site, 'styles'), exist_ok=True)
for f in ('post-shared.css', 'post-mobile.css', 'post-desktop.css', 'site-header-mobile.css', 'aurora.css'):
    shutil.copy(os.path.join(repo, 'src/styles', f), os.path.join(site, 'styles', f))
shutil.copytree(os.path.join(repo, 'src/assets/fonts/inter'), os.path.join(site, 'assets/fonts/inter'), dirs_exist_ok=True)
shutil.copytree(os.path.join(repo, 'public/fonts/neometric-alt'), os.path.join(site, 'fonts/neometric-alt'), dirs_exist_ok=True)
shutil.copy(os.path.join(repo, 'public/fonts/neometric-alt.css'), os.path.join(site, 'fonts/'))
shutil.copy(os.path.join(here, 'stori-lokal.html'), os.path.join(site, 'index.html'))
for f in os.listdir(here):
    if f.lower().endswith('.png'): shutil.copy(os.path.join(here, f), site)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8766), functools.partial(http.server.SimpleHTTPRequestHandler, directory=site))
threading.Thread(target=srv.serve_forever, daemon=True).start()
frames = os.path.join(here, '_frames'); shutil.rmtree(frames, ignore_errors=True); os.makedirs(frames)
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--font-render-hinting=none'])
        pg = await b.new_page(viewport={'width': 430, 'height': 765}, device_scale_factor=1080/430)
        await pg.goto('http://127.0.0.1:8766/index.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(800)
        n = int(round(await pg.evaluate('TOTAL') * 30))
        for i in range(n):
            await pg.evaluate(f'seek({i/30})'); await pg.screenshot(path=os.path.join(frames, f'f{i:04d}.png'))
        await b.close()
asyncio.run(main())
subprocess.run([sys.executable, os.path.join(here, 'zvuk.py')], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', os.path.join(frames, 'f%04d.png'),
    '-i', os.path.join(here, 'zvuk.wav'), '-vf', 'crop=1080:1920:0:0,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow',
    '-crf', '16', '-profile:v', 'high', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
print('gotovo:', out)
