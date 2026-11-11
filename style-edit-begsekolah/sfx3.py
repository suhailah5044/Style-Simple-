# SFX baru (stereo, sesuai headphone) - lain dari video sebelum ni
import numpy as np, wave
SR=48000; R=np.random.default_rng(11)
def t(d): return np.arange(int(SR*d))/SR
def lp(x,k):
    y=np.empty_like(x);a=0.
    for i in range(len(x)): a+=k*(x[i]-a); y[i]=a
    return y
def hp(x,k): return x-lp(x,k)
def env(d,a=0.004,dec=10): tt=t(d); return np.minimum(1,tt/a)*np.exp(-dec*tt)
def bell(f,d,dec=6,ratio=2.76,idx=1.2):
    tt=t(d); return np.sin(2*np.pi*f*tt+idx*np.exp(-dec*1.5*tt)*np.sin(2*np.pi*f*ratio*tt))*env(d,0.002,dec)
def st(x,pan=0.):  # pan -1..1
    return np.column_stack([x*np.sqrt((1-pan)/2),x*np.sqrt((1+pan)/2)])
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
def whoosh(d=0.42,k0=0.03,k1=0.25,p0=-0.9,p1=0.9):
    n=R.standard_normal(int(SR*d)); tt=t(d); k=k0+(k1-k0)*np.sin(np.pi*tt/d)
    y=np.empty_like(n);a=0.
    for i in range(len(n)): a+=k[i]*(n[i]-a); y[i]=a
    y=hp(y,0.02)*np.sin(np.pi*tt/d)**2.5
    pan=p0+(p1-p0)*tt/d
    return np.column_stack([y*np.sqrt((1-pan)/2),y*np.sqrt((1+pan)/2)])
def thud(f0=95,f1=42,d=0.6,dec=6):
    tt=t(d); f=f1+(f0-f1)*np.exp(-tt*18); return np.sin(2*np.pi*np.cumsum(f)/SR)*env(d,0.003,dec)
# hook: whoosh L->R + soft thud + bell shimmer (stereo)
sh=[(0.36+i*0.05,st(bell(f,0.9,5)*0.35,p)) for i,(f,p) in enumerate(zip([1975,2637,3322],[-0.6,0,0.6]))]
save("hook",mix(1.4,[(0,whoosh(0.45)),(0.34,thud()*0.9),(0.34,lp(R.standard_normal(int(SR*.25)),.3)*env(.25,.002,16)*.35)]+sh))
save("whoosh",whoosh(0.38,0.05,0.35,0.7,-0.7),0.7)
# pop: bubble (pitch drop)
tt=t(0.09); f=1100*np.exp(-tt*28)+260; save("pop",np.sin(2*np.pi*np.cumsum(f)/SR)*env(0.09,0.001,40),0.75)
# click: mechanical double click
c=lambda: hp(R.standard_normal(int(SR*.012)),.5)*env(.012,.0003,350)+np.sin(2*np.pi*3200*t(.012))*env(.012,.0003,300)*.5
save("click",mix(0.12,[(0,c()),(0.045,c()*0.7)]),0.7)
# ding: bright FM bell, ringing
save("ding",mix(1.2,[(0,st(bell(1568,1.2,4.5),-0.15)),(0.0,st(bell(3136,0.6,9,idx=.6)*.25,0.2))]))
# impact: soft deep hit + air
save("impact",mix(0.9,[(0,thud(80,38,0.9,4.5)),(0,lp(R.standard_normal(int(SR*.4)),.08)*env(.4,.002,9)*.45)]))
# sparkle: random high bells scattered stereo
save("sparkle",mix(1.1,[(i*0.055,st(bell(f,0.6,8,3.01,.8)*0.5,p)) for i,(f,p) in enumerate(zip([2349,3136,2793,3729,4186,3520],[-.7,.5,-.2,.7,-.5,.2]))]),0.7)
# ticks rising (woodblock)
for n,f in [("tick_a",880),("tick_b",1175),("tick_c",1568)]:
    tt=t(.14); save(n,(np.sin(2*np.pi*f*tt)+.4*np.sin(2*np.pi*f*2.4*tt))*env(.14,.001,38),0.7)
# cash: ka-ching (rattle + 2 bells)
rat=sum(np.roll(hp(R.standard_normal(int(SR*.18)),.4)*env(.18,.001,40),int(SR*j*.018)) for j in range(4))*.25
save("cash",mix(1.0,[(0,rat),(0.14,st(bell(2093,.8,6,2.0,.9),-.3)),(0.22,st(bell(2637,.8,5,2.0,.9),.3))]))
# riser for CTA
d=0.7; tt=t(d); n=hp(R.standard_normal(int(SR*d)),.15)*(tt/d)**2.2*.5
f=500+1500*(tt/d)**2; tone=np.sin(2*np.pi*np.cumsum(f)/SR)*(tt/d)**2*.25
save("riser",mix(1.5,[(0,n+tone),(d,st(bell(2637,.8,5)*.6,-.3)),(d+.06,st(bell(3951,.8,5)*.5,.3))]))
# swipe (PiP masuk)
save("swipe",whoosh(0.26,0.08,0.45,-0.3,0.6),0.6)
# snap (frame break): crisp crack + low whoosh
crk=hp(R.standard_normal(int(SR*.05)),.6)*env(.05,.0005,90)
save("snap",mix(0.6,[(0,whoosh(0.3,0.04,0.25,0.5,-0.5)*.6),(0.16,st(crk,-.3)),(0.175,st(crk*.7,.3)),(0.16,thud(120,60,.3,12)*.5)]))
