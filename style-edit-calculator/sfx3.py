# Jana SFX baru (stereo, sedap guna headphone) + BGM lo-fi lembut. python3 sfx3.py
import numpy as np, wave
SR=44100
def save(n,L,R=None):
    R=L if R is None else R
    m=max(np.abs(L).max(),np.abs(R).max(),1e-9); L=L/m*0.89; R=R/m*0.89
    d=(np.stack([L,R],1)*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes()); w.close()
t=lambda d: np.arange(int(SR*d))/SR
def env(n,a=0.003,dec=8): x=np.arange(n)/SR; return np.minimum(x/a,1)*np.exp(-x*dec)
def lp(x,k=0.15):
    y=np.zeros_like(x); s=0
    for i,v in enumerate(x): s+=k*(v-s); y[i]=s
    return y
def bell(f,d,dec=6,h=(1,2.76,5.4),g=(1,.35,.12)):
    x=t(d); return sum(gg*np.sin(2*np.pi*f*hh*x)*np.exp(-x*dec*hh**.5) for hh,gg in zip(h,g))*env(len(x),0.002,0)
def pad(x,d): o=np.zeros(int(SR*d)); o[:len(x)]=x[:len(o)]; return o
rng=np.random.default_rng(7)
# ui_prompt: dua nada lembut (macam notifikasi UI), kiri->kanan
a=pad(bell(1318,0.5,9),0.7); b=np.zeros_like(a); b[int(.09*SR):]=pad(bell(1975,0.5,8),0.7)[:len(a)-int(.09*SR)]
save("ui_prompt",a*0.9+b*0.4,a*0.4+b*0.9)
# ui_select: tik + nada pendek
x=t(0.35); c=np.sin(2*np.pi*2400*x)*env(len(x),0.001,60)+0.6*np.sin(2*np.pi*1600*x)*env(len(x),0.002,22)
save("ui_select",c)
# key_tick: bunyi butang kalkulator plastik
def tick():
    x=t(0.12); n=rng.standard_normal(len(x))*env(len(x),0.0005,90); return n-lp(n,0.25)+0.5*np.sin(2*np.pi*3100*x)*env(len(x),0.0005,120)
save("key_tick",tick())
# key_triple: tik-tik-tik (pan)
o=np.zeros(int(SR*0.5)); L=o.copy(); R=o.copy()
for i,(st,p) in enumerate([(0,.2),(.11,.5),(.22,.8)]):
    k=tick(); s=int(st*SR); L[s:s+len(k)]+=k*(1-p); R[s:s+len(k)]+=k*p
save("key_triple",L,R)
# ding_glass: ding cerah USP
save("ding_glass",pad(bell(2093,1.2,4.5,(1,2.0,3.0,4.2),(1,.25,.12,.06)),1.3))
# ding_soft: lebih rendah
save("ding_soft",pad(bell(1568,1.0,5),1.1))
# whoosh stereo L->R
x=t(0.55); n=rng.standard_normal(len(x)); e=np.sin(np.pi*np.clip(x/0.55,0,1))**2
f=np.zeros_like(n); s=0
for i,v in enumerate(n): k=0.02+0.25*(i/len(n)); s+=k*(v-s); f[i]=s
pan=x/0.55; save("whoosh_lr",f*e*(1-pan),f*e*pan)
save("whoosh_rl",f*e*pan,f*e*(1-pan))
# soft impact
x=t(0.8); th=np.sin(2*np.pi*(55*x+40*(1-np.exp(-x*20))/20*1))*np.exp(-x*6)
nn=lp(rng.standard_normal(len(x)),0.05)*np.exp(-x*18)*0.6
save("soft_impact",th+nn)
# bubble pop
x=t(0.25); fr=600+1400*np.exp(-x*40); ph=2*np.pi*np.cumsum(fr)/SR
save("bubble_pop",np.sin(ph)*env(len(x),0.001,22))
# sparkle stereo (untuk solar)
L=np.zeros(int(SR*1.4)); R=L.copy()
for i in range(9):
    s=int(i*0.07*SR); b_=bell(2600+i*260,0.6,10)*(0.9-i*0.06); p=0.5+0.45*np.sin(i*1.3)
    L[s:s+len(b_)]+=b_*(1-p); R[s:s+len(b_)]+=b_*p
save("sparkle_lr",L,R)
# hook_shimmer: swirl stereo + rise (sedap guna headphone)
x=t(1.6); n=lp(rng.standard_normal(len(x)),0.08); e=np.clip(x/1.1,0,1)**2*np.exp(-np.clip(x-1.1,0,9)*9)
ch=sum(np.sin(2*np.pi*f_*x*(1+0.05*x))*0.25 for f_ in (880,1320,1760))
sig=(n*0.6+ch)*e; pan=0.5+0.5*np.sin(2*np.pi*1.2*x)
save("hook_shimmer",sig*(1-pan),sig*pan)
# --- BGM lo-fi lembut 84bpm ---
bpm=84; beat=60/bpm; bars=12; dur=bars*4*beat; N=int(dur*SR); L=np.zeros(N); R=np.zeros(N)
chords=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]]
mf=lambda m:440*2**((m-69)/12)
for b_ in range(bars):
    st=int(b_*4*beat*SR); ln=int(4*beat*SR); x=np.arange(ln)/SR
    for j,m in enumerate(chords[b_%4]):
        v=(np.sin(2*np.pi*mf(m)*x)+0.3*np.sin(2*np.pi*mf(m)*2*x)*np.exp(-x*3))*np.minimum(x/0.02,1)*np.exp(-x*0.5)*(1+0.15*np.sin(2*np.pi*4*x))
        p=0.3+0.4*(j/3); L[st:st+ln]+=v*(1-p)*0.18; R[st:st+ln]+=v*p*0.18
    bass=np.sin(2*np.pi*mf(chords[b_%4][0]-12)*x)*np.minimum(x/0.01,1)*np.exp(-x*1.2)*0.35
    L[st:st+ln]+=bass; R[st:st+ln]+=bass
    for q in range(4):
        s=st+int(q*beat*SR)
        if q in (0,2):
            kx=np.arange(int(0.25*SR))/SR; k=np.sin(2*np.pi*(50*kx+60*(1-np.exp(-kx*30))/30))*np.exp(-kx*14)*0.5
            L[s:s+len(k)]+=k; R[s:s+len(k)]+=k
        if q in (1,3):
            sn=lp(rng.standard_normal(int(0.2*SR)),0.35)*np.exp(-np.arange(int(0.2*SR))/SR*22)*0.15
            L[s:s+len(sn)]+=sn; R[s:s+len(sn)]+=sn
        for hh in (0,0.5):
            s2=s+int(hh*beat*SR); hx=rng.standard_normal(int(0.05*SR)); hx=(hx-lp(hx,0.5))*np.exp(-np.arange(len(hx))/SR*80)*0.06
            L[s2:s2+len(hx)]+=hx*0.7; R[s2:s2+len(hx)]+=hx
vin=lp(rng.standard_normal(N),0.1)*0.01; L+=vin; R+=vin
fade=np.minimum(np.arange(N)/SR/1.0,1)*np.minimum((N-np.arange(N))/SR/1.5,1); save("bgm",L*fade,R*fade)
