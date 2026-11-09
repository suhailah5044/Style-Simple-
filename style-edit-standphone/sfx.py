import numpy as np, wave
SR=48000
def save(n,x):
    x=x/ (np.max(np.abs(x))+1e-9)*0.8
    d=(np.column_stack([x,x])*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
def t(d): return np.arange(int(SR*d))/SR
def bell(f,d=0.9,dec=6):
    tt=t(d); x=sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-dec*m**0.5*tt) for m,a in [(1,1),(2.76,.35),(5.4,.15),(8.93,.06)])
    att=np.minimum(1,tt/0.002); return x*att
def place(total,parts):
    out=np.zeros(int(SR*total))
    for off,s in parts:
        i=int(SR*off); out[i:i+len(s)]+=s[:len(out)-i]
    return out
rng=np.random.default_rng(1)
# ting single
save("ting", bell(2093,0.9))
# ting ting
save("tingting", place(1.1,[(0,bell(2093,0.9)),(0.12,bell(2637,0.9)*0.9)]))
# pop
tt=t(0.12); f=900*np.exp(-tt*30)+250; ph=2*np.pi*np.cumsum(f)/SR
save("pop", np.sin(ph)*np.exp(-tt*35))
# whoosh
n=rng.standard_normal(int(SR*0.45)); tt=t(0.45)
from numpy.fft import rfft,irfft
# simple sweeping lowpass via moving average of varying width
env=np.sin(np.pi*tt/0.45)**2
y=np.zeros_like(n); a=0
for i in range(len(n)):
    k=0.02+0.25*(i/len(n)); a+= k*(n[i]-a); y[i]=a
save("whoosh", y*env)
# impact (solid)
tt=t(0.6); f=110*np.exp(-tt*8)+45; ph=2*np.pi*np.cumsum(f)/SR
click=rng.standard_normal(len(tt))*np.exp(-tt*120)*0.3
save("impact", np.sin(ph)*np.exp(-tt*6)+click)
# sparkle
parts=[(i*0.045,bell(f,0.6,9)*(1-i*0.08)) for i,f in enumerate([2349,2793,3136,3520,4186])]
save("sparkle", place(0.9,parts))
# cash: ting ting + coins
coins=[(0.18+i*0.04,bell(f,0.4,14)*0.5) for i,f in enumerate([3951,4699,3520,4186])]
save("kaching", place(1.2,[(0,bell(2093,0.9)),(0.1,bell(3136,0.9))]+coins))
