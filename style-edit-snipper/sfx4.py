# SFX set baru (stereo, sesuai headphone) - lain dari set standphone/begsekolah lama
import numpy as np, wave, os
SR=48000; R=np.random.default_rng(42)
os.makedirs("sfx",exist_ok=True)
def t(d): return np.arange(int(SR*d))/SR
def lp(x,k):
    y=np.empty_like(x);a=0.
    for i in range(len(x)): a+=k*(x[i]-a); y[i]=a
    return y
def hp(x,k): return x-lp(x,k)
def env(d,a=0.004,dec=10): tt=t(d); return np.minimum(1,tt/a)*np.exp(-dec*tt)
def st(x,pan=0.): return np.column_stack([x*np.sqrt((1-pan)/2),x*np.sqrt((1+pan)/2)])
def mix(total,parts):
    o=np.zeros((int(SR*total),2))
    for off,s in parts:
        if s.ndim==1: s=st(s)
        i=int(SR*off); n=min(len(s),len(o)-i); o[i:i+n]+=s[:n]
    return o
def save(n,x,g=0.8):
    if x.ndim==1: x=st(x)
    x=x/(np.abs(x).max()+1e-9)*g
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((x*32767).astype(np.int16).tobytes());w.close()
def sweep(f0,f1,d,shape=1.0): tt=t(d); f=f0+(f1-f0)*(tt/d)**shape; return np.sin(2*np.pi*np.cumsum(f)/SR)
def marimba(f,d=0.5,dec=9): tt=t(d); return (np.sin(2*np.pi*f*tt)+.25*np.sin(2*np.pi*f*4*tt)*np.exp(-30*tt))*env(d,0.001,dec)
def glass(f,d=1.0,dec=4): tt=t(d); return (np.sin(2*np.pi*f*tt)+.35*np.sin(2*np.pi*f*2.32*tt)*np.exp(-6*tt)+.15*np.sin(2*np.pi*f*4.25*tt)*np.exp(-12*tt))*env(d,0.001,dec)
def air(d,k0,k1,p0,p1):
    n=R.standard_normal(int(SR*d)); tt=t(d); k=k0+(k1-k0)*np.sin(np.pi*tt/d)
    y=np.empty_like(n);a=0.
    for i in range(len(n)): a+=k[i]*(n[i]-a); y[i]=a
    y=hp(y,0.03)*np.sin(np.pi*tt/d)**2
    pan=p0+(p1-p0)*tt/d
    return np.column_stack([y*np.sqrt((1-pan)/2),y*np.sqrt((1+pan)/2)])
def thump(f0,f1,d,dec): tt=t(d); f=f1+(f0-f1)*np.exp(-tt*22); return np.sin(2*np.pi*np.cumsum(f)/SR)*env(d,0.002,dec)
def drop(f0=700,f1=1900,d=0.12): return sweep(f0,f1,d,0.6)*env(d,0.001,30)

# ---- HOOK (setiap video lain) ----
# V1 air: titis air + whoosh kiri->kanan + soft bloom
save("hook1",mix(1.6,[(0,air(0.5,0.02,0.3,-0.9,0.9)*.8),(0.38,st(drop(),-.4)),(0.5,st(drop(900,2300,.1)*.7,.4)),
  (0.42,thump(90,45,0.7,6)*.8),(0.46,st(glass(1760,1.1,3.5)*.35,-.2)),(0.5,st(glass(2637,1.1,3.5)*.3,.3))]))
# V2 tahan lasak: reverse swell + punchy impact + metallic ring
d=0.45; sw=hp(R.standard_normal(int(SR*d)),.2)*(t(d)/d)**3*.6
save("hook2",mix(1.6,[(0,sw),(0,sweep(200,900,d,2)*(t(d)/d)**2*.2),(d,thump(110,40,0.9,5)),(d,lp(R.standard_normal(int(SR*.3)),.12)*env(.3,.002,12)*.5),
  (d+.02,st(glass(1318,1.0,3)*.25,.5)),(d+.02,st(glass(1976,1.0,3)*.2,-.5))]))
# V3 anak: pluck chime naik 3 nada + sparkle stereo
save("hook3",mix(1.6,[(0.0,air(0.35,0.03,0.25,0.8,-0.6)*.6),(0.25,st(marimba(784,.6),-.5)),(0.37,st(marimba(988,.6),0)),(0.49,st(marimba(1319,.8,6),.5)),
  (0.5,thump(95,50,0.5,8)*.5)]+[(0.55+i*.04,st(glass(f,.5,9)*.15,p)) for i,(f,p) in enumerate(zip([3136,3951,4699],[-.7,.2,.7]))]))
# ---- transisi ----
save("whoosh_a",air(0.36,0.04,0.32,-0.8,0.8),0.6)          # pertukaran footage
save("whoosh_b",air(0.42,0.02,0.22,0.8,-0.8),0.6)
# ---- UI prompt (subtitle/overlay) ----
save("ui_prompt1",mix(.45,[(0,st(marimba(1047,.3,14),-.2)),(.07,st(marimba(1568,.35,12),.2))]),0.7)
save("ui_prompt2",mix(.45,[(0,st(sweep(600,1400,.05)*env(.05,.001,30),0)),(.05,st(glass(1397,.4,10)*.6,.25))]),0.7)
save("ui_prompt3",mix(.4,[(0,st(marimba(1175,.25,16),.3)),(.06,st(marimba(880,.3,14),-.3))]),0.65)
# pop lembut (mulut)
tt=t(.07); save("pop2",np.sin(2*np.pi*np.cumsum(300+900*np.exp(-tt*55))/SR)*env(.07,.0005,45),0.7)
# click lembut (keyboard)
c=hp(R.standard_normal(int(SR*.02)),.35)*env(.02,.0004,220)+np.sin(2*np.pi*2100*t(.02))*env(.02,.0003,260)*.4
save("click2",mix(.08,[(0,c)]),0.6)
# ding / ting-ting USP
save("ting2",mix(1.1,[(0,st(glass(2093,.9,5),-.3)),(.13,st(glass(2637,1.0,4.5),.3))]),0.7)
save("ding2",mix(1.2,[(0,st(glass(1661,1.2,3.6),0)),(0,st(marimba(3322,.3,20)*.3,.2))]),0.7)
# soft impact
save("impact2",mix(.9,[(0,thump(85,42,.9,5)),(0,lp(R.standard_normal(int(SR*.35)),.1)*env(.35,.002,10)*.4)]),0.8)
# titis air (water USP)
save("droplet",mix(.5,[(0,st(drop(),-.3)),(.11,st(drop(1000,2600,.09)*.6,.35))]),0.7)
# zip (kompartmen/zipper)
z=np.concatenate([hp(R.standard_normal(int(SR*.006)),.5)*np.exp(-np.linspace(0,6,int(SR*.006)))*(0.4+0.6*np.sin(np.pi*i/22)) for i in range(22)]+[np.zeros(int(SR*.004))]*0)
zz=np.zeros(int(SR*.32));
for i in range(22):
    s=int(SR*(i*0.013)); b=hp(R.standard_normal(int(SR*.008)),.5)*np.exp(-np.linspace(0,7,int(SR*.008)))*(0.4+0.6*np.sin(np.pi*i/22)); zz[s:s+len(b)]+=b
save("zip",np.column_stack([zz*np.linspace(1,.3,len(zz)),zz*np.linspace(.3,1,len(zz))]),0.6)
# shimmer (cantik/design)
save("shimmer",mix(1.0,[(i*.045,st(glass(f,.5,9)*.5,p)) for i,(f,p) in enumerate(zip([2349,2960,3520,4186,4699],[-.6,.3,-.2,.6,0]))]),0.6)
# PiP swish + frame-break crack
save("pip_swish",air(0.24,0.1,0.5,-0.2,0.7),0.55)
crk=hp(R.standard_normal(int(SR*.045)),.6)*env(.045,.0005,95)
save("fbreak",mix(.6,[(0,air(.28,.05,.3,.6,-.6)*.6),(.15,st(crk,-.35)),(.165,st(crk*.6,.35)),(.15,thump(130,60,.3,12)*.45)]),0.7)
# CTA: riser lembut (tiada teks)
d=.8; tt=t(d); save("cta_rise",mix(1.6,[(0,hp(R.standard_normal(int(SR*d)),.12)*(tt/d)**2.4*.4),(0,sweep(400,1600,d,2)*(tt/d)**2*.2),(d,st(glass(2093,.8,4)*.5,-.3)),(d+.07,st(glass(3136,.8,4)*.4,.3))]),0.65)
print(sorted(os.listdir("sfx")))
