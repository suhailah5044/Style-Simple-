import numpy as np, wave, sys, json
SR=48000; BPM=100; B=60/BPM; DUR=21.0
N=int(SR*(DUR+3)); rng=np.random.default_rng(11)
L=np.zeros(N); R=np.zeros(N)
def T(d): return np.arange(int(SR*d))/SR
def put(buf,s,t0,g=1.0):
    i=int(t0*SR); n=min(len(s),N-i)
    if n>0: buf[i:i+n]+=s[:n]*g
def st(s,t0,g=1.0,pan=0.0):
    put(L,s,t0,g*(1-max(pan,0))); put(R,s,t0,g*(1+min(pan,0)))
def lp(x,a):
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
def mtof(m): return 440*2**((m-69)/12)
def rhodes(f,d):
    t=T(d); env=np.exp(-t*1.6)*np.minimum(1,t/0.006)
    mod=np.sin(2*np.pi*f*t)*1.4*np.exp(-t*5)
    s=np.sin(2*np.pi*f*t+mod)*env + 0.25*np.sin(2*np.pi*2*f*t)*np.exp(-t*4)
    return s*(1+0.12*np.sin(2*np.pi*4.5*t))
def kick():
    t=T(0.3); f=45+70*np.exp(-t*28); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
def snap():
    t=T(0.18); n=rng.standard_normal(len(t)); n=n-lp(n,0.25); return n*np.exp(-t*30)*0.5
def shaker():
    t=T(0.08); n=rng.standard_normal(len(t)); n=n-lp(n,0.7); return n*np.sin(np.pi*t/0.08)**2*0.12
def bell(f,d=1.4):
    t=T(d); return (np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*f*2.0*t)*np.exp(-t*3)+0.15*np.sin(2*np.pi*f*3.01*t)*np.exp(-t*6))*np.exp(-t*3.2)
prog=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]]  # Fmaj7 Em7 Dm7 Cmaj7
roots=[41,40,38,36]
bars=int(np.ceil(DUR/(4*B)))+1
mel=[[72,76,79],[71,74,76],[69,72,77],[67,71,74]]
for b in range(bars):
    t0=b*4*B; ch=prog[b%4]
    if t0>=DUR: break
    for k,m in enumerate(ch):
        st(rhodes(mtof(m),4*B+0.3),t0+0.012*k,0.10,pan=(k-1.5)*0.15)
    st(rhodes(mtof(ch[1]+12),2*B),t0+2.5*B,0.05,0.3)
    # bass
    for bt,ln in [(0,1.4),(2.5,1.2)]:
        tt=T(ln*B); s=np.sin(2*np.pi*mtof(roots[b%4])*tt)*np.minimum(1,tt/0.01)*np.exp(-tt*1.2)
        st(s,t0+bt*B,0.30)
    for q in range(4):
        tq=t0+q*B
        if tq>=DUR-0.2: continue
        if q in (0,): st(kick(),tq,0.55)
        if q==2: st(kick(),tq+0.5*B,0.45)
        if q in (1,3): st(snap(),tq,0.32,pan=0.1)
        for e in range(2): st(shaker(),tq+e*B/2+0.02,1.0 if e else 0.6,pan=-0.3)
    # sparse melody bells on later bars
    if b>=1:
        for j,m in enumerate(mel[b%4]):
            st(bell(mtof(m+12),1.0),t0+(1.5+j*0.75)*B,0.035,pan=0.35)
# vinyl
vin=rng.standard_normal(N)*0.004; cr=(rng.random(N)>0.99985)*rng.standard_normal(N)*0.08
L+=lp(vin+cr,0.3); R+=lp(vin+cr,0.3)
mus=np.stack([L,R]); mus[:, int(DUR*SR):]=0
fo=int(1.0*SR); e=int(DUR*SR); mus[:,e-fo:e]*=np.linspace(1,0,fo)
mus=np.stack([lp(mus[0],0.35),lp(mus[1],0.35)])
mus/=np.abs(mus).max(); mus*=0.5
# SFX
sfx=np.zeros((2,N))
def sp(s,t0,g=1.0,pan=0.0):
    i=int(t0*SR); n=min(len(s),N-i); sfx[0,i:i+n]+=s[:n]*g*(1-max(pan,0)); sfx[1,i:i+n]+=s[:n]*g*(1+min(pan,0))
def sparkle(t0):
    for j,m in enumerate([84,88,91,96,100]):
        sp(bell(mtof(m),0.9),t0+j*0.055,0.10,pan=(-0.4+0.2*j))
def click(t0):
    t=T(0.05); n=rng.standard_normal(len(t)); n=n-lp(n,0.4)
    s=n*np.exp(-t*140)*0.6+np.sin(2*np.pi*2400*t)*np.exp(-t*90)*0.3
    sp(s,t0,0.55); sp(s*0.6,t0+0.07,0.4)
def tick(t0):
    t=T(0.25); s=np.sin(2*np.pi*2093*t)*np.exp(-t*22)+0.4*np.sin(2*np.pi*4186*t)*np.exp(-t*35)
    sp(s,t0,0.13)
def swell(t0,d=0.6):
    t=T(d); n=rng.standard_normal(len(t)); y=np.zeros(len(t)); s=0.0
    a=0.01+0.25*(t/d)**2
    for i in range(len(t)): s+=a[i]*(n[i]-s); y[i]=s
    sp(y*(t/d)**1.5*0.5,t0-d,0.6)
def pop(t0):
    t=T(0.08); f=700*np.exp(-t*35)+250; sp(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*50),t0,0.30)
ev=json.loads(sys.argv[2])
for t0 in ev.get("sparkle",[]): sparkle(t0)
for t0 in ev.get("click",[]): click(t0)
for t0 in ev.get("tick",[]): tick(t0)
for t0 in ev.get("swell",[]): swell(t0)
for t0 in ev.get("pop",[]): pop(t0)
mix=mus+sfx; mix=np.tanh(mix*1.2)/np.tanh(1.2)*0.9; mix=mix[:,:int(SR*DUR)]
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix.T*32767).astype(np.int16).tobytes()); w.close()
