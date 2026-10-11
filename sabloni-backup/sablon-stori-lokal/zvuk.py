# Zvuk za šablon "stori za lokale": muzika 120 BPM + klik na rezovima + grom munje.
# Balans: efekti 5–7 dB ispod muzike, ukupno -14 LUFS. Generisano, bez tuđih semplova.
# Muzika 120 BPM + zvucni efekti za stori sablon (13 s). Sve generisano, bez tudjih semplova.
import numpy as np, wave
SR=44100; DUR=13.0; N=int(SR*DUR); rng=np.random.default_rng(7)
t_all=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); j=min(N,i+len(sig)); s=sig[:j-i]*gain
    L[i:j]+=s*np.sqrt(0.5*(1-pan)); R[i:j]+=s*np.sqrt(0.5*(1+pan))
def env(n,a,d):  # attack/decay u sekundama
    t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def lp(x,a):  # jednostavan niskopropusni filter
    y=np.zeros_like(x); acc=0.0
    for i,v in enumerate(x): acc+=a*(v-acc); y[i]=acc
    return y
def noise(n): return rng.standard_normal(n)
BEAT=0.5; BAR=2.0
# --- bubanj
def kick():
    n=int(.45*SR); t=np.arange(n)/SR; f=48+120*np.exp(-t/0.035)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/0.16)
def clap():
    n=int(.25*SR); x=noise(n); x=x-lp(x,.25); e=sum(np.exp(-np.maximum(0,np.arange(n)/SR-o)/0.012)*(np.arange(n)/SR>=o) for o in (0,.011,.022))
    return x*e*0.6+x*np.exp(-np.arange(n)/SR/0.09)*0.4
def hat(open_=False):
    n=int((.18 if open_ else .05)*SR); x=noise(n); x=x-lp(x,.6); return x*np.exp(-np.arange(n)/SR/(0.06 if open_ else 0.012))
K,CL,HC,HO=kick(),clap(),hat(),hat(True)
# progresija Am - F - C - G (po 1 takt), bas + pad
chords=[(57,60,64),(53,57,60),(48,52,55),(55,59,62)]
roots=[45,41,48,43]
mf=lambda m:440*2**((m-69)/12)
def pad(freqs,dur):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for f in freqs:
        for d in (-0.15,0.15): s+=np.sin(2*np.pi*f*(1+d/100)*t)+0.3*np.sin(2*np.pi*2*f*t)
    s=lp(s,0.08); a=np.minimum(1,t/0.25)*np.minimum(1,(dur-t)/0.3); return s*a/len(freqs)/2
def bass(f,dur):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.sin(2*np.pi*f*t)+0.25*np.sin(2*np.pi*2*f*t)
    return s*np.minimum(1,t/0.01)*np.exp(-t/0.35)
music_L=np.zeros(N); music_R=np.zeros(N)
def madd(sig,start,g,pan=0):
    i=int(start*SR); j=min(N,i+len(sig)); s=sig[:j-i]*g
    music_L[i:j]+=s*np.sqrt(0.5*(1-pan)); music_R[i:j]+=s*np.sqrt(0.5*(1+pan))
nbars=int(np.ceil(DUR/BAR))
for b in range(nbars):
    t0=b*BAR; c=b%4
    madd(pad([mf(m) for m in chords[c]],BAR),t0,0.22)
    for k in range(4):
        tb=t0+k*BEAT
        if tb>=DUR: break
        intro = tb<1.0            # prvi takt: samo pad + hat (meki ulaz)
        if not intro: madd(K,tb,0.9)
        if k in (1,3) and not intro: madd(CL,tb,0.32,0.1)
        madd(HC,tb+0.25,0.16,-0.3)
        madd(HC,tb,0.08,0.3)
        if not intro:
            madd(bass(mf(roots[c]),0.24),tb+0.25,0.42)        # "off-beat" bas
    madd(HO,t0+1.75,0.1,0.4)
# sidechain pumpanje uz kik
pump=np.ones(N)
for b in np.arange(1.0,DUR,BEAT):
    i=int(b*SR); n=int(0.32*SR); j=min(N,i+n); x=np.arange(j-i)/SR
    pump[i:j]=np.minimum(pump[i:j],0.55+0.45*np.minimum(1,x/0.3))
music_L*=pump; music_R*=pump
# kraj: muzika se utisava poslednjih 0,8 s
fade=np.clip((DUR-t_all)/0.8,0,1)**1.5
music_L*=fade; music_R*=fade
# --- efekti
def whoosh(dur,rise=True):
    n=int(dur*SR); x=noise(n); t=np.arange(n)/SR; out=np.zeros(n); acc=0.0
    for i in range(n):
        k=t[i]/dur; a=(0.02+0.25*(k if rise else 1-k)); acc+=a*(x[i]-acc); out[i]=acc
    e=np.sin(np.pi*np.clip(t/dur,0,1))**1.4
    return (out-lp(out,0.02))*e*3.0
def thud(): n=int(.3*SR); t=np.arange(n)/SR; f=70+90*np.exp(-t/0.03); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/0.09)
def pop(f=880):
    n=int(.18*SR); t=np.arange(n)/SR; ff=f*(1+0.6*np.exp(-t/0.01)); return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t/0.05)
def shimmer():
    n=int(.9*SR); t=np.arange(n)/SR; s=sum(np.sin(2*np.pi*mf(m)*t)*np.exp(-t/(0.25+0.1*i)) for i,m in enumerate((81,84,88,93)))
    return s*np.minimum(1,t/0.005)/4
def zap():
    n=int(.35*SR); t=np.arange(n)/SR; x=noise(n); car=np.sign(np.sin(2*np.pi*(900-700*t/0.35)*t))
    return (car*0.5+ (x-lp(x,.3))*0.8)*np.exp(-t/0.09)
def jab(): # agresivan udar munje: nisko + klik
    n=int(.2*SR); t=np.arange(n)/SR; x=noise(n)
    return np.sin(2*np.pi*np.cumsum(60+140*np.exp(-t/0.02))/SR)*np.exp(-t/0.07)*0.8+(x-lp(x,.5))*np.exp(-t/0.008)*0.5

def swish(dur,lo=0.03,hi=0.12):   # mek vazdusni swish (bez sistanja)
    n=int(dur*SR); x=noise(n); t=np.arange(n)/SR; out=np.zeros(n); acc=0.0
    for i in range(n):
        k=t[i]/dur; acc+=(lo+(hi-lo)*np.sin(np.pi*k))*(x[i]-acc); out[i]=acc
    return out*np.sin(np.pi*np.clip(t/dur,0,1))**2*2.2
def riser(dur):                   # uzlazni sum koji vodi u rez
    n=int(dur*SR); x=noise(n); t=np.arange(n)/SR; out=np.zeros(n); acc=0.0
    for i in range(n):
        acc+=(0.01+0.2*(t[i]/dur)**2)*(x[i]-acc); out[i]=acc
    return out*(t/dur)**2*2.5
def softtap():                    # prigusen udar (umesto oštrog)
    n=int(.18*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*np.cumsum(55+60*np.exp(-t/0.02))/SR)*np.exp(-t/0.06)
def pluck(m,dec=0.35):            # tonski akcenat u A-molu
    n=int(1.0*SR); t=np.arange(n)/SR; f=mf(m)
    s=np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.08)+0.15*np.sin(2*np.pi*3*f*t)*np.exp(-t/0.04)
    return s*np.minimum(1,t/0.004)*np.exp(-t/dec)/1.5
def revswell(dur):   # obrnuti "rep" reverba: raste i preseče se tačno na rezu
    n=int(dur*SR); t=np.arange(n)/SR; x=noise(n); out=np.zeros(n); acc=0.0
    for i in range(n): acc+=0.06*(x[i]-acc); out[i]=acc
    tone=sum(np.sin(2*np.pi*mf(m)*t) for m in (69,76,81))/3
    e=(t/dur)**3
    return (out*1.6+tone*0.5)*e
def subdrop():       # dubok, mek pad ispod muzike
    n=int(.7*SR); t=np.arange(n)/SR; f=38+50*np.exp(-t/0.12)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/0.35)*np.minimum(1,t/0.01)
def shutter():       # kratak, cist klik (kao okidac) sa malim repom
    n=int(.35*SR); t=np.arange(n)/SR; x=noise(n); hp=x-lp(x,.4)
    c=hp*np.exp(-t/0.004)+0.5*hp*np.exp(-np.maximum(0,t-0.035)/0.006)*(t>=0.035)
    tail=lp(noise(n),0.05)*np.exp(-t/0.12)*0.25
    return c+tail
def lpsweep(x,a0,a1):             # filter na muzici: zatvoren -> otvoren
    y=np.zeros_like(x); acc=0.0; n=len(x)
    for i in range(n):
        a=a0+(a1-a0)*(i/n); acc+=a*(x[i]-acc); y[i]=acc
    return y
# --- odbrojavanje dok se ocene ucitavaju: tik na svakih 4% prstena, usporava kao brojac (cubic-out, 2 s)
def tick(f):
    n=int(.06*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*np.exp(-t/0.012)+0.3*(noise(n)-lp(noise(n),.5))*np.exp(-t/0.003)
def ding():
    n=int(.8*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*mf(88)*t)+0.5*np.sin(2*np.pi*mf(93)*t))*np.exp(-t/0.25)*np.minimum(1,t/0.003)/1.5
import os, re
_html=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'stori-lokal.html'),encoding='utf-8').read()
PCT=float(re.search(r"procenat:\s*([0-9.]+)",_html).group(1))   # procenat se cita iz CONFIG u stori-lokal.html
C0, CD = 4.05, 2.0                      # isto kao u stori-lokal.html (k2+0.1, 2 s)
ks=[k for k in range(4, int(PCT)+1, 4)]
_cnt=np.zeros(int((CD+0.1)*SR)); _cntR=np.zeros_like(_cnt)
for i,k in enumerate(ks):
    y=k/PCT; u=1-(1-y)**(1/3); tk=tick(1500+600*i/len(ks)); o=int(u*CD*SR); _cnt[o:o+len(tk)]+=tk[:len(_cnt)-o]
EVENTS=[]   # (ime, signal, pocetak s, pan, nacin merenja, cilj dB u odnosu na muziku)
EVENTS.append(('odbrojavanje',_cnt,C0,0.0,'vrh',-7.0))
EVENTS.append(('ding',ding(),C0+CD,0.0,'glasnoca',-13.0))
# --- grom munje: pucketanje + dug rep koji se kotrlja (oko 1,6 s)
def thunder():
    n=int(1.7*SR); t=np.arange(n)/SR; x=noise(n)
    crack=(x-lp(x,.35))*np.exp(-t/0.06)
    rumble=lp(lp(noise(n),0.012),0.02)*25*np.exp(-t/0.55)*(1+0.5*np.sin(2*np.pi*3.1*t))*np.minimum(1,t/0.05)
    return crack*0.9+rumble
# vremena iz animacije (T u stori-lokal.html)
# --- munja: električno pražnjenje (odobreno 5.10.2026). Varnice su na taktu, zajedno sa udarcima munje na ekranu.
def praznjenje(start, end):
    n=int((end-start)*SR); t=np.arange(n)/SR
    buzz=np.sign(np.sin(2*np.pi*100*t))*0.25+np.sin(2*np.pi*200*t)*0.2
    cr=noise(n); cr=cr-lp(cr,.5)
    gate=lp((rng.random(n)<0.004).astype(float),0.3)*30
    beats=[0.0]+list(np.arange(9.5,end-0.3,BEAT)-start)          # izlet + svaki takt
    sparks=sum(((t>=b)&(t<b+0.08))*np.exp(-(t-b)/0.02) for b in beats)
    env=np.minimum(1,t/0.01)*(0.55+0.45*np.exp(-t/0.6))*np.clip((end-start-t)/0.5,0,1)
    return (buzz*(0.6+0.4*np.sin(2*np.pi*7*t))*0.8 + cr*np.clip(gate,0,1)*0.8 + cr*sparks*0.7)*env
DG=float(os.environ.get('DG','1.0'))
EVENTS.append(('klik stiker',shutter(),1.62,-0.2,'vrh',-6.0))
EVENTS.append(('klik rez 1',shutter(),3.95,0.2,'vrh',-6.0))
EVENTS.append(('klik rez 2',shutter(),8.45,-0.2,'vrh',-6.0))
EVENTS.append(('praznjenje',praznjenje(9.15,12.6),9.15,0.0,'glasnoca',-11.0))

import os, subprocess
db=lambda x:20*np.log10(max(1e-9,x))
hp=lambda x,fc: x-lp(x,1-np.exp(-2*np.pi*fc/SR))
# --- profesionalni balans
# 1) EQ: muzika bez infrazvuka (<30 Hz); efekti bez niskog mulja (<140 Hz) da ne mute bas i kik
musL,musR=hp(music_L,30)*0.95,hp(music_R,30)*0.95
def rms(x): return np.sqrt((x**2).mean())
# svaki efekat se automatski poravna prema muzici na svom mestu: kratki po vrhu, dugi po glasnoci (RMS)
for nm,sig,st,pan,mode,target in EVENTS:
    sig=hp(sig,140); i=int(st*SR); j=min(N,i+len(sig)); seg=sig[:j-i]
    mref=np.abs(musL[i:j])+np.abs(musR[i:j])
    if mode=='vrh': g=10**((target+db(mref.max()/2)-db(np.abs(seg).max()))/20)
    else:
        g=10**((target+db(np.sqrt(((musL[i:j]**2+musR[i:j]**2)/2).mean()))-db(rms(seg)))/20)
        g=min(g, 10**((-6.0+db(mref.max()/2)-db(np.abs(seg).max()))/20))   # i vrh najviše 6 dB ispod muzike
    add(seg*g, st, 1.0, pan*0.5)
fxL,fxR=L*np.sqrt(2),R*np.sqrt(2)
# 2) muzika se blago povuče (najviše 2 dB) dok traje efekat, pa se vrati (napad 5 ms, otpuštanje 150 ms)
env=np.abs(fxL)+np.abs(fxR); fol=np.zeros(N); acc=0.0
aa,ar=1-np.exp(-1/(0.005*SR)),1-np.exp(-1/(0.15*SR))
for i,v in enumerate(env): acc+=(aa if v>acc else ar)*(v-acc); fol[i]=acc
ref=np.percentile(fol[fol>1e-4],95) if (fol>1e-4).any() else 1
duck=1-0.206*np.clip(fol/ref,0,1)
musL*=duck; musR*=duck
mus=np.stack([musL,musR],1); fx=np.stack([fxL,fxR],1)
# kontrola: vrh i glasnoća (RMS 300 ms) svakog efekta u odnosu na muziku
for nm,(a,b) in {'klik stiker':(1.6,1.9),'klik rez 1':(3.93,4.2),'odbrojavanje':(4.05,6.0),'ding':(6.05,6.6),'klik rez 2':(8.43,8.7),'praznjenje':(9.15,12.4)}.items():
    i,j=int(a*SR),int(b*SR)
    print(f"{nm:13s} vrh {db(np.abs(fx[i:j]).max())-db(np.abs(mus[i:j]).max()):6.1f} dB | glasnoća {db(rms(fx[i:j]))-db(rms(mus[i:j])):6.1f} dB")
# 3) zbir, blago "lepljenje" (meki limiter) i pretapanje na kraju
m=mus+fx; m=np.tanh(m*1.15)/np.tanh(1.15)
fo=np.clip((DUR-t_all)/0.6,0,1)[:,None]; m*=fo; m*=0.89/np.max(np.abs(m))
here=os.path.dirname(os.path.abspath(__file__)); raw=os.path.join(here,'_zvuk-raw.wav'); out=os.path.join(here,'zvuk.wav')
with wave.open(raw,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m*32767).astype('<i2').tobytes())
# 4) glasnoća za Instagram: -14 LUFS, true peak -1 dBTP
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',raw,'-af','loudnorm=I=-14:TP=-1:LRA=11','-ar','44100',out],check=True)
os.remove(raw); print('zvuk.wav gotov')
