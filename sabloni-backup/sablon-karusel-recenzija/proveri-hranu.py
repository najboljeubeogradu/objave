# Provera: nijedan ispis ne sme preko jela (i čačkalice). Pokreće se posle render-karusel.py, dok _site postoji.
# Upotreba: python3 proveri-hranu.py
# Potrebno: pip install --break-system-packages "rembg[cpu]"
import os, asyncio, threading, http.server, functools, numpy as np
from PIL import Image
from rembg import remove, new_session
here=os.path.dirname(os.path.abspath(__file__)); site=os.path.join(here,'_site'); ses=new_session('isnet-general-use')
def mask(name):
    im=Image.open(os.path.join(site,'img',name)).convert('RGB'); m=np.asarray(remove(im,session=ses).split()[3])>128
    a=np.asarray(im).astype(int); top=a[:int(a.shape[0]*.3)]                           # cackalica: svetlo drvo iznad jela
    t=(top[:,:,0]>150)&(top[:,:,0]-top[:,:,2]>40)&(top[:,:,1]>110); cols=np.where(t.sum(0)>top.shape[0]*.5)[0]
    if len(cols): m[:top.shape[0], cols.min():cols.max()+1]=True
    return m
mm=mask('hero-mobile.jpg'); md=mask('hero-desktop.jpg')
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8768),functools.partial(http.server.SimpleHTTPRequestHandler,directory=site))
threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2150,'height':538})
        await pg.goto('http://127.0.0.1:8768/index.html'); await pg.evaluate('document.fonts.ready'); await pg.evaluate('window.wordsReady'); await pg.wait_for_timeout(600)
        rects=await pg.evaluate("""(()=>{const out=[];const d=document.getElementById('imgD').getBoundingClientRect();
          // velike reci: svako slovo (bez praznog prostora iznad/ispod)
          document.querySelectorAll('.big span').forEach(e=>{const r=e.getBoundingClientRect();out.push(['rec '+e.textContent,r.left,r.top+r.height*.15,r.right,r.bottom-r.height*.05])});
          // sav tekst u slajdovima: stvarne linije teksta, ne prazne kutije oko njih
          document.querySelectorAll('.sl').forEach(sl=>{const w=document.createTreeWalker(sl,NodeFilter.SHOW_TEXT);let n;
            while(n=w.nextNode()){if(!n.textContent.trim())continue;const rg=document.createRange();rg.selectNodeContents(n);for(const r of rg.getClientRects())out.push([n.textContent.trim().slice(0,24),r.left,r.top,r.right,r.bottom])}});
          // graficki elementi: nalepnica, ikonice, plocice, prsten, dugme
          document.querySelectorAll('.sl #m1,.sl .ic,.sl .m-vtile,.sl .dm-ring,.sl .m-quiz__share').forEach(e=>{const r=e.getBoundingClientRect();out.push([(e.id||e.className.toString().split(' ')[0]),r.left,r.top,r.right,r.bottom])});
          return {rects:out,d:[d.left,d.top,d.width,d.height]}})()""")
        await b.close()
    dx,dy,dw,dh=rects['d']
    def hit(mask,x0,y0,w,h,r):
        H,W=mask.shape; return int(mask[max(0,int((r[1]-y0)/h*H)):max(0,min(H,int((r[3]-y0)/h*H)+1)), max(0,int((r[0]-x0)/w*W)):max(0,min(W,int((r[2]-x0)/w*W)+1))].sum())
    bad=[]
    for n,*r in rects['rects']:
        h=(hit(mm,0,0,430,538,r) if r[0]<430 else 0)+(hit(md,dx,dy,dw,dh,r) if r[2]>dx and r[0]<dx+dw else 0)
        if h: bad.append(f'  "{n}" prelazi preko jela ({h} px)')
    print('\n'.join(bad) if bad else 'OK: nijedan ispis ne prelazi preko jela')
asyncio.run(main())
