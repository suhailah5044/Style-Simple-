import numpy as np,wave
sr=44100;bpm=118;b=60/bpm;D=20.5;n=int(sr*D);out=np.zeros(n)
t=lambda d:np.arange(int(sr*d))/sr
def add(x,s):
    i=int(s*sr)
    if i>=n:return
    j=min(n,i+len(x));out[i:j]+=x[:j-i]
kick=np.sin(2*np.pi*(50+90*np.exp(-t(.3)*25))*t(.3))*np.exp(-t(.3)*9)
rng=np.random.default_rng(1);hat=rng.standard_normal(int(sr*.05));hat=np.diff(hat,prepend=0)*np.exp(-t(.05)*90)*.25
clap=rng.standard_normal(int(sr*.15))*np.exp(-t(.15)*30)*.3
f=lambda m:440*2**((m-69)/12)
chords=[[65,69,72],[60,64,67],[62,65,69],[58,62,65]];bass=[41,36,38,34]
def pluck(fr,d=.35):
    x=t(d);return sum(np.sign(np.sin(2*np.pi*fr*k*x))/k*.0 + np.sin(2*np.pi*fr*k*x)/k for k in (1,2,3))*np.exp(-x*7)
beat=0;s=0
while s<D:
    bar=int(beat//4)%4
    add(kick*.8,s)
    add(hat,s+b/2)
    if beat%4 in(1,3):add(clap,s)
    if beat%2==0:
        for m in chords[bar]:add(pluck(f(m))*.09,s+b/2)
    add(np.sin(2*np.pi*f(bass[bar])*t(b*.9))*np.exp(-t(b*.9)*3)*.35,s)
    beat+=1;s+=b
out=out/np.abs(out).max()*.8
fade=np.ones(n);k=int(sr*1.2);fade[-k:]=np.linspace(1,0,k);out*=fade
w=wave.open("music.wav","w");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes())
