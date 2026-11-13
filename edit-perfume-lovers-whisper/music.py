# Jana muzik latar upbeat ringan (120 BPM, 44.1kHz) -> sfx/bgm.wav . Bebas royalti (dijana sendiri).
import numpy as np,wave
SR=44100;BPM=120;b=60/BPM;DUR=40.0;N=int(SR*DUR);out=np.zeros(N)
def env(n,a=0.005,d=0.3):
    t=np.arange(n)/SR;return np.minimum(1,t/a)*np.exp(-t/d)
def add(t0,sig):
    i=int(t0*SR);j=min(N,i+len(sig));out[i:j]+=sig[:j-i]
def tone(f,dur,amp,d=0.25,w=0):
    n=int(dur*SR);t=np.arange(n)/SR
    s=np.sin(2*np.pi*f*t)+0.35*np.sin(4*np.pi*f*t)+w*np.sign(np.sin(2*np.pi*f*t))
    return amp*s*env(n,0.004,d)
chords=[[60,64,67,71],[57,60,64,67],[53,57,60,64],[55,59,62,67]]  # Cmaj7 Am7 Fmaj7 G
mf=lambda m:440*2**((m-69)/12)
beat=0;t=0
rng=np.random.default_rng(1)
while t<DUR:
    bar=int(beat//4);ch=chords[bar%4]
    # kick 4-on-floor
    n=int(0.25*SR);tt=np.arange(n)/SR;add(t,0.9*np.sin(2*np.pi*(50+90*np.exp(-tt*35))*tt)*np.exp(-tt*9))
    # offbeat hat
    n=int(0.06*SR);add(t+b/2,0.12*rng.standard_normal(n)*np.exp(-np.arange(n)/SR*70))
    # clap on 2 & 4
    if beat%4 in(1,3):
        n=int(0.15*SR);add(t,0.22*rng.standard_normal(n)*np.exp(-np.arange(n)/SR*28))
    # bass
    add(t+b/2,tone(mf(ch[0]-24),b*0.45,0.35,0.12))
    # pluck arp 8ths
    for k in range(2):
        add(t+k*b/2,tone(mf(ch[(beat*2+k)%4]+12),0.3,0.13,0.12))
    beat+=1;t=beat*b
out=np.tanh(out*1.1);out/=np.max(np.abs(out));out*=0.8
fade=int(1.5*SR);out[-fade:]*=np.linspace(1,0,fade)
w=wave.open("sfx/bgm.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
