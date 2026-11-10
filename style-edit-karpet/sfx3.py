# Jana SFX baru (lain dari v1/v2) + muzik latar 116bpm. Semua sintetik, bebas lesen.
import numpy as np, wave
SR=44100; rng=np.random.default_rng(7)
def save(n,x,st=False):
    x=np.asarray(x,np.float64); x=x/ (np.abs(x).max()+1e-9)*0.9
    if not st: x=np.stack([x,x],1)
    d=(x*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
def t(d):return np.arange(int(SR*d))/SR
def env(n,a,r):
    e=np.ones(n);A=int(SR*a);e[:A]=np.linspace(0,1,A);e[A:]=np.exp(-np.arange(n-A)/(SR*r));return e
def lp(x,a):
    y=np.zeros_like(x);s=0
    for i,v in enumerate(x):s+=a*(v-s);y[i]=s
    return y
def bp_noise(d,f0,f1):  # sweeping filtered noise via FFT slices
    n=int(SR*d);x=rng.standard_normal(n);out=np.zeros(n);B=1024
    for i in range(0,n,B):
        seg=x[i:i+B];F=np.fft.rfft(seg,B);fr=np.fft.rfftfreq(B,1/SR);fc=f0+(f1-f0)*i/n
        F*=np.exp(-((fr-fc)/(fc*0.5))**2);out[i:i+B]=np.fft.irfft(F,B)[:len(seg)]
    return out
# whoosh lembut (air)
d=0.55;n=int(SR*d);w=bp_noise(d,500,3500)*np.sin(np.pi*np.linspace(0,1,n))**2
pan=np.linspace(-0.6,0.6,n);save("air_whoosh",np.stack([w*(1-pan)/2,w*(1+pan)/2],1),True)
# bubble pop
x=t(0.12);f=np.linspace(380,1300,len(x));save("bubble_pop",np.sin(2*np.pi*np.cumsum(f)/SR)*env(len(x),0.003,0.035))
# UI click
x=t(0.05);c=rng.standard_normal(len(x))*env(len(x),0.0005,0.004)+0.6*np.sin(2*np.pi*2400*x)*env(len(x),0.0005,0.01);save("ui_click",c)
# bell ding (USP)
x=t(1.2);b=sum(a*np.sin(2*np.pi*1568*m*x)*np.exp(-x*k) for a,m,k in[(1,1,3.5),(.45,2.76,6),(.25,5.4,9),(.15,0.5,4)]);save("bell_ding",b*env(len(x),0.002,9))
# soft impact
x=t(0.6);f=90*np.exp(-x*7)+45;s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*6);s+=0.25*lp(rng.standard_normal(len(x)),0.05)*np.exp(-x*20);save("soft_impact",s)
# frame break: shutter + glass tick
x=t(0.35);sh=np.zeros(len(x))
for k,o in enumerate([0,0.045,0.09]):
    i=int(o*SR);m=int(0.03*SR);sh[i:i+m]+=rng.standard_normal(m)*np.exp(-np.arange(m)/(SR*0.006))*(1-k*0.2)
sh+=0.4*np.sin(2*np.pi*3200*x)*np.exp(-x*30);save("frame_break",sh)
# ting2 (double sparkle)
x=t(0.7);tt=np.zeros(len(x))
for o,fq in[(0,2637),(0.11,3520)]:
    i=int(o*SR);y=x[:len(x)-i];tt[i:]+=np.sin(2*np.pi*fq*y)*np.exp(-y*9)+0.3*np.sin(2*np.pi*fq*2.01*y)*np.exp(-y*14)
save("ting2",tt)
# UI prompt (subtitle): soft marimba 2-note
x=t(0.45);p=np.zeros(len(x))
for o,fq in[(0,880),(0.07,1318.5)]:
    i=int(o*SR);y=x[:len(x)-i];p[i:]+=(np.sin(2*np.pi*fq*y)+0.2*np.sin(2*np.pi*fq*4*y))*np.exp(-y*14)
save("ui_prompt",p)
# ---------- muzik latar 116bpm (house ringan, stereo lebar untuk headphone) ----------
bpm=116;beat=60/bpm;D=30.0;N=int(SR*D);L=np.zeros(N);R=np.zeros(N)
def add(sig,at,gl=1,gr=1):
    i=int(at*SR);j=min(N,i+len(sig));L[i:j]+=sig[:j-i]*gl;R[i:j]+=sig[:j-i]*gr
kx=t(0.35);kick=np.sin(2*np.pi*np.cumsum(50+120*np.exp(-kx*30))/SR)*np.exp(-kx*9)
hx=t(0.06);hat=np.diff(rng.standard_normal(len(hx)+1))*np.exp(-hx*60)
cx=t(0.2);clap=lp(rng.standard_normal(len(cx)),0.6)*np.exp(-cx*22)
chords=[[57,60,64,67],[53,57,60,64],[48,52,55,60],[55,59,62,67]]  # Am7 Fmaj7 C G
mf=lambda m:440*2**((m-69)/12)
nb=int(D/beat)
for b in range(nb):
    T0=b*beat; bar=b//4; ch=chords[bar%4]
    if b>=2: add(kick*0.9,T0)
    add(hat*0.18,T0+beat/2,0.6,1.0); add(hat*0.08,T0+beat*0.75,1.0,0.6)
    if b%2==1 and b>=4: add(clap*0.35,T0,0.9,1.0)
    # bass offbeat
    bx=t(beat*0.45);bs=np.sin(2*np.pi*mf(ch[0]-12)*bx)+0.3*np.sin(2*np.pi*mf(ch[0])*bx);bs*=env(len(bx),0.005,0.12)
    if b>=2: add(bs*0.35,T0+beat/2)
    # pluck chord stabs
    if b%4 in(0,2) or (b%4==3):
        px=t(0.5);st=sum(np.sign(np.sin(2*np.pi*mf(m)*px))*0.15+np.sin(2*np.pi*mf(m)*px) for m in ch)
        st=lp(st,0.25)*env(len(px),0.004,0.09);o=0 if b%4!=3 else beat/2
        add(st*0.12,T0+o,1.0,0.55); add(st*0.12,T0+o+0.012,0.55,1.0)
# pad
pxs=np.arange(N)/SR
for bar in range(int(nb/4)+1):
    ch=chords[bar%4];s0=bar*4*beat;n=int(4*beat*SR);x=np.arange(n)/SR
    pad=sum(np.sin(2*np.pi*mf(m+12)*x+np.sin(2*np.pi*0.3*x)) for m in ch)*np.sin(np.pi*np.linspace(0,1,n))*0.03
    add(pad,s0,1,0.7);add(pad,s0+0.02,0.7,1)
fade=np.ones(N);f=int(1.5*SR);fade[-f:]=np.linspace(1,0,f);fi=int(0.3*SR);fade[:fi]=np.linspace(0,1,fi)
M=np.stack([L,R],1)*fade[:,None];M=np.tanh(M*1.4)
save("music",M,True)
print("ok")
