import numpy as np, wave, sys
SR=48000; BPM=120; B=60/BPM; DUR=18.0
N=int(SR*(DUR+4)); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def t_(d): return np.arange(int(SR*d))/SR
def add(sig,t0,pan=0.0,ch=None):
    i=int(t0*SR); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*(1-pan)/1.0 if pan>0 else sig[:n]
    R[i:i+n]+=sig[:n]*(1+pan) if pan<0 else sig[:n]
def lp(x,a): # one-pole lowpass
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
def mtof(m): return 440*2**((m-69)/12)
# drums
def kick():
    t=t_(0.35); f=50+90*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*7)*0.9
def clap():
    t=t_(0.25); n=rng.standard_normal(len(t)); n=n-lp(n,0.15)
    env=np.exp(-t*18)*(1+0.6*np.exp(-((t-0.012)/0.004)**2)); return n*env*0.28
def hat(open_=False):
    t=t_(0.12 if not open_ else 0.3); n=rng.standard_normal(len(t)); n=n-lp(n,0.6)
    return n*np.exp(-t*(55 if not open_ else 14))*0.09
K=kick(); C=clap()
bars=int(np.ceil(DUR/(4*B)))+1
prog=[(57,[57,60,64,67]),(53,[53,57,60,64]),(48,[48,52,55,59]),(55,[55,59,62,66])] # Am7 Fmaj7 Cmaj7 G
side=np.ones(N)
for bar in range(bars):
    t0=bar*4*B
    for b in range(4):
        tb=t0+b*B
        if tb<DUR-0.5:
            add(K,tb); 
            si=int(tb*SR); env=1-0.55*np.exp(-t_(B)*9); side[si:si+len(env)]=np.minimum(side[si:si+len(env)],env[:max(0,min(len(env),N-si))])
        if b in (1,3) and tb<DUR-0.5: add(C,tb)
        for h in range(2):
            th=tb+h*B/2
            if th<DUR-0.3: add(hat(h==1 and b==3),th+0.0,pan=0.2)
# pad chords (detuned saws, lowpassed) + bass + pluck arp
def saw(f,d,det=0.0):
    t=t_(d); out=np.zeros(len(t))
    for dd in (-det,0,det): out+=2*((t*f*(1+dd))%1)-1
    return out/3
pad=np.zeros(N); bass=np.zeros(N); arp=np.zeros(N)
for bar in range(bars):
    t0=bar*4*B; root,ch=prog[bar%4]
    d=4*B
    for m in ch:
        s=saw(mtof(m),d,0.006); env=np.minimum(1,t_(d)/0.05)*np.minimum(1,(d-t_(d))/0.1)
        s=lp(s*env,0.08)*0.10; i=int(t0*SR); n=min(len(s),N-i); pad[i:i+n]+=s[:n]
    for b in range(8):
        tb=t0+b*B/2; s=np.sin(2*np.pi*mtof(root-24)*t_(B/2))*np.exp(-t_(B/2)*3)*0.32
        i=int(tb*SR); n=min(len(s),N-i); bass[i:i+n]+=s[:n]
    notes=ch+[ch[1]+12,ch[2]+12,ch[0]+12,ch[2]]
    for k in range(16):
        tb=t0+k*B/4; m=notes[k%len(notes)]+12; tt=t_(0.22)
        s=(np.sin(2*np.pi*mtof(m)*tt)+0.3*np.sin(4*np.pi*mtof(m)*tt))*np.exp(-tt*16)*0.07
        i=int(tb*SR); n=min(len(s),N-i); arp[i:i+n]+=s[:n]
# echo on arp
d=int(SR*B*0.75); arpE=arp.copy(); arpE[d:]+=arp[:-d]*0.35
mus_end=int(DUR*SR)
tail=np.ones(N); fo=int(1.2*SR); tail[mus_end-fo:mus_end]=np.linspace(1,0,fo); tail[mus_end:]=0
musL=(L+ (pad+bass)*side + arpE*0.9)*tail
musR=(R+ (pad+bass)*side + arp*0.9 + np.roll(arpE,int(SR*0.012))*0.2)*tail
# final hit: ring last chord? keep fade.
# SFX
sfxL=np.zeros(N); sfxR=np.zeros(N)
def whoosh(d=0.32):
    t=t_(d); n=rng.standard_normal(len(t)); out=np.zeros(len(t)); s=0.0
    a=0.02+0.5*(np.sin(np.pi*t/d))**2
    for i in range(len(t)): s+=a[i]*(n[i]-s); out[i]=s
    out=out-lp(out,0.02); return out*np.sin(np.pi*t/d)**1.5*0.55
def pop():
    t=t_(0.07); f=900*np.exp(-t*40)+300; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*60)*0.35
def ding():
    t=t_(1.2); f=1567.98
    return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*6)+0.2*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*12))*np.exp(-t*4)*0.16
def put(s,t0):
    i=int(t0*SR); n=min(len(s),N-i); sfxL[i:i+n]+=s[:n]; sfxR[i:i+n]+=s[:n]
for c in [1.5,3.0,5.5,8.5,11.5,13.0,14.5]: put(whoosh(),c-0.2)
for p in [float(x) for x in sys.argv[2].split(',')]: put(pop(),p)
for dg in [float(x) for x in sys.argv[3].split(',')]: put(ding(),dg)
mus=np.stack([musL,musR]); mus/=np.abs(mus).max(); mus*=0.42
sfx=np.stack([sfxL,sfxR])*0.85
mix=mus+sfx; mix=np.tanh(mix*1.1)/np.tanh(1.1)*0.89
mix=mix[:, :int(SR*DUR)]
out=(mix.T*32767).astype(np.int16)
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
