# SFX lembut untuk gaya "menu": swish halus (tukar tajuk) + kilau kecil (harga)
import numpy as np, wave
SR=44100; rng=np.random.default_rng(5)
def save(n,x,g=0.7):
    x=x/(np.max(np.abs(x))+1e-9)*g
    d=(np.column_stack([x,x])*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
def t(d): return np.arange(int(SR*d))/SR
# swish: noise ditapis, sapuan naik lembut
d=0.38; n=rng.standard_normal(int(SR*d)); tt=t(d)
k=0.015+0.12*np.sin(np.pi*tt/d)**2; y=np.zeros_like(n); a=0.0
for i in range(len(n)): a+=k[i]*(n[i]-a); y[i]=a
save("swish", y*np.sin(np.pi*tt/d)**2.5, 0.6)
# kilau: 3 nada tinggi lembut
def tone(f,d,dec): tt=t(d); return (np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2.7*f*tt))*np.exp(-dec*tt)*np.minimum(1,tt/0.004)
out=np.zeros(int(SR*0.9))
for i,f in enumerate([2093,2637,3136]):
    s=tone(f,0.7,7); j=int(SR*i*0.06); out[j:j+len(s)]+=s[:len(out)-j]
save("glint", out, 0.5)
print("ok")
