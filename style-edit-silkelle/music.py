# Muzik latar ringkas (dijana, bebas royalti) — 118 BPM, pop lembut
import numpy as np,wave
SR=44100;BPM=118;DUR=44.8;b=60/BPM;N=int(SR*DUR);L=np.zeros((N,2))
t=lambda d:np.arange(int(SR*d))/SR
def add(x,at,pan=0.5,v=1.0):
    i=int(at*SR);x=x[:max(0,N-i)];L[i:i+len(x),0]+=x*v*(1-pan)*2*0.5;L[i:i+len(x),1]+=x*v*pan*2*0.5
def kick():
    tt=t(0.35);f=50+90*np.exp(-tt*30);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9)
def hat():
    tt=t(0.06);return np.random.randn(len(tt))*np.exp(-tt*70)*0.25
def clap():
    tt=t(0.2);return np.random.randn(len(tt))*np.exp(-tt*25)*0.35
def note(f,d,dec=3.0):
    tt=t(d);return (np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt))*np.exp(-tt*dec)
CH=[[174.6,220,261.6,329.6],[220,261.6,329.6,392],[146.8,174.6,220,261.6],[130.8,164.8,196,246.9]]
bar=4*b;nb=int(DUR/bar)+1
for k in range(nb):
    c=CH[k%4];t0=k*bar
    for f in c: add(note(f,bar,0.6)*0.10,t0,0.5)
    add(note(c[0]/2,bar,1.2)*0.35,t0)
    for s in range(8):
        f=c[[0,2,1,3,2,1,3,2][s]]*2
        add(note(f,b/2,9)*0.06,t0+s*b/2,0.3+0.4*(s%2))
    if t0>=3.4:
        for q in range(4):
            add(kick()*0.55,t0+q*b)
            add(hat(),t0+q*b+b/2,0.65)
            if q%2: add(clap(),t0+q*b,0.45)
fade=np.ones(N);fl=int(1.5*SR);fade[-fl:]=np.linspace(1,0,fl);fade[:int(0.3*SR)]=np.linspace(0,1,int(0.3*SR))
L*=fade[:,None];L/=np.abs(L).max()*1.12
w=wave.open("assets/music.wav","w");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
w.writeframes((L*32767).astype(np.int16).tobytes());w.close()
