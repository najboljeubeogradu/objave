# Provera: velike reči se ne preklapaju sa tekstom/grafikom i nijedno slovo nije presečeno ivicom slajda.
import asyncio, threading, http.server, functools, os
from playwright.async_api import async_playwright
site=os.path.join(os.path.dirname(os.path.abspath(__file__)),'_site')
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8769),functools.partial(Q,directory=site))
threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2150,'height':538})
        await pg.goto('http://127.0.0.1:8769/index.html'); await pg.evaluate('document.fonts.ready'); await pg.evaluate('window.wordsReady'); await pg.wait_for_timeout(600)
        r=await pg.evaluate("""(()=>{const W=[...document.querySelectorAll('.big span')].filter(e=>e.textContent.trim()).map(e=>[e.textContent,e.getBoundingClientRect()]);const T=[];
          document.querySelectorAll('.sl').forEach(sl=>{const w=document.createTreeWalker(sl,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(!n.textContent.trim())continue;const rg=document.createRange();rg.selectNodeContents(n);for(const r of rg.getClientRects())T.push([n.textContent.trim().slice(0,18),r])}});
          document.querySelectorAll('.sl #m1,.sl .ic,.sl .m-vtile,.sl .dm-ring,.sl .m-quiz__share').forEach(e=>T.push([e.id||e.className.toString().split(' ')[0],e.getBoundingClientRect()]));
          const out=[];W.forEach(([c,a])=>T.forEach(([n,t])=>{const ox=Math.min(a.right,t.right)-Math.max(a.left,t.left),oy=Math.min(a.bottom-a.height*.05,t.bottom)-Math.max(a.top+a.height*.15,t.top);if(ox>0&&oy>0)out.push(`  "${c}" preko "${n}"`)}));
          W.forEach(([c,a])=>[430,860,1290,1720].forEach(x=>{if(a.left<x-1&&a.right>x+1)out.push(`  slovo "${c}" presečeno ivicom slajda (${x})`)}));
          return out})()""")
        print('\n'.join(r) if r else 'OK: velike reči se ne preklapaju ni sa čim, nijedno slovo nije presečeno')
        await b.close()
asyncio.run(main())
