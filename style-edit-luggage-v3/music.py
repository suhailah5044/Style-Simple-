# Muzik latar original (dijana): 118bpm, kick lembut + hat + chord pluck. Mix perlahan bawah suara.
import numpy as np, wave
sr=44100; bpm=118; beat=60/bpm; dur=62; n=int(sr*dur); L=np.zeros(n); R=np.zeros(n)
t=lambda d: np.arange(int(sr*d))/sr
def add(buf,x,at):
    i=int(at*sr); j=min(n,i+len(x)); buf[i:j]+=x[:j-i]
k=t(.35); kick=np.sin(2*np.pi*(48+90*np.exp(-k*28))*k)*np.exp(-k*9)*.9
h=t(.06); hat=np.random.default_rng(1).standard_normal(len(h))*np.exp(-h*70)*.18
hat=np.diff(np.concatenate([[0],hat]))
f=lambda m:440*2**((m-69)/12)
prog=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
def pluck(freqs,d):
    x=t(d); s=sum(np.sign(np.sin(2*np.pi*fr*x))*.5+np.sin(2*np.pi*fr*x) for fr in freqs)
    return s*np.exp(-x*5)*.07
def bass(fr,d):
    x=t(d); return np.sin(2*np.pi*fr*x)*np.exp(-x*3)*.35
b=0
while b*beat<dur:
    T=b*beat; bar=(b//4)%4; ch=prog[bar]
    for buf in (L,R): add(buf,kick,T)
    add(L,hat*1.0,T+beat/2); add(R,hat*0.8,T+beat/2)
    if b%2==0: add(L,pluck([f(m) for m in ch],beat*1.5),T+beat/2); add(R,pluck([f(m+12) for m in ch],beat*1.5)*.6,T+beat/2)
    add(L,bass(f(ch[0]-12),beat*.9),T); add(R,bass(f(ch[0]-12),beat*.9),T)
    b+=1
fade=np.minimum(1,np.minimum(np.arange(n)/(sr*.8),(n-np.arange(n))/(sr*2)))
st=np.stack([L,R],1)*fade[:,None]; st/=np.abs(st).max()/0.8
w=wave.open("sfx/music.wav","w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((st*32767).astype(np.int16).tobytes()); w.close(); print("music ok")
