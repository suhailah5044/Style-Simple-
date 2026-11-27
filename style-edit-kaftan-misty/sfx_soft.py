# Jana SFX lembut (44.1kHz mono) — semua perlahan, attack lembut, tiada bunyi kasar.
import numpy as np, wave
SR=44100
def save(n,x):
    x=x/ (np.abs(x).max()+1e-9)*0.8
    with wave.open(f"sfx/{n}.wav","wb") as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((x*32767).astype(np.int16).tobytes())
def t(d): return np.arange(int(SR*d))/SR
def lp(x,a):  # one-pole lowpass
    y=np.zeros_like(x);p=0
    for i,v in enumerate(x): p+=a*(v-p);y[i]=p
    return y
rng=np.random.default_rng(7)
# 1) mist_whoosh: hembusan angin lembut
T=t(0.9);n=rng.standard_normal(len(T));env=np.sin(np.pi*np.clip(T/0.9,0,1))**2
save("mist_whoosh",lp(lp(n,0.06),0.12)*env)
# 2) soft_chime: loceng kaca lembut
T=t(1.6);x=sum(a*np.sin(2*np.pi*f*T)*np.exp(-T*d) for f,a,d in [(1568,1,3),(2349,.45,4.5),(3136,.25,6),(4699,.1,9)])
save("soft_chime",x*np.minimum(1,T/0.004))
# 3) bubble_pop: pop bulat perlahan
T=t(0.25);f=420+500*np.exp(-T*30);x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-T*22)
save("bubble_pop",x*np.minimum(1,T/0.003))
# 4) sparkle: kilauan halus
T=t(1.2);x=np.zeros_like(T)
for k,f in enumerate([2637,3136,3520,4186,5274]):
    s=int(SR*k*0.06);tt=T[:len(T)-s];x[s:]+=np.sin(2*np.pi*f*tt)*np.exp(-tt*7)*0.6
save("sparkle",x*np.minimum(1,T/0.01))
# 5) airy_swell: hook — riser lembut + chime
T=t(1.4);n=lp(rng.standard_normal(len(T)),0.08);env=(T/1.4)**2*np.exp(-np.maximum(0,T-1.2)*20)
pad=sum(np.sin(2*np.pi*f*T) for f in [523.25,659.25,783.99])*0.15*np.sin(np.pi*T/1.4)
save("airy_swell",n*env*0.7+pad)
