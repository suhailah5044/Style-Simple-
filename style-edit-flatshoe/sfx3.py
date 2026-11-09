# SFX set v3 (UI prompt style) — semua dijana, bebas royalti
import numpy as np, wave
SR=48000; rng=np.random.default_rng(11)
def save(n,x,g=0.8):
    x=x/(np.max(np.abs(x))+1e-9)*g
    d=(np.column_stack([x,x])*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
def t(d): return np.arange(int(SR*d))/SR
def tone(f,d,dec=20,harm=((1,1),),att=0.004):
    tt=t(d); x=sum(a*np.sin(2*np.pi*f*m*tt) for m,a in harm)*np.exp(-dec*tt); return x*np.minimum(1,tt/att)
def place(total,parts):
    out=np.zeros(int(SR*total))
    for off,s in parts:
        i=int(SR*off); n=min(len(s),len(out)-i); out[i:i+n]+=s[:n]
    return out
def lp(x,k):
    y=np.zeros_like(x);a=0
    for i in range(len(x)): a+=k*(x[i]-a); y[i]=a
    return y
S=((1,1),(2,.08))
# prompt: soft sine popup (iOS-like), turun-naik
save("prompt", place(0.5,[(0,tone(880,0.18,22,S)),(0.09,tone(1320,0.35,13,S))]))
# bubble: blip pitch naik (macam bubble chat masuk)
tt=t(0.11); f=500+1400*(tt/0.11)**1.5; ph=2*np.pi*np.cumsum(f)/SR
save("bubble", np.sin(ph)*np.sin(np.pi*tt/0.11)**0.7)
# ting ting: loceng terang dua kali
B=((1,1),(2.76,.35),(5.4,.12))
save("tingting", place(0.9,[(0,tone(2093,0.5,9,B)),(0.13,tone(2093,0.7,7,B))]))
# kalimba pluck (dua not)
K=((1,1),(3.9,.18))
save("pluck", place(0.7,[(0,tone(659,0.4,12,K)),(0.08,tone(988,0.55,10,K))]))
# soft click (lembut)
c=lp(rng.standard_normal(int(SR*0.02)),0.25)*np.exp(-t(0.02)*300)
save("click", place(0.15,[(0,c),(0,tone(1800,0.06,70)*0.5)]),0.6)
# sparkle up: arpeggio cepat 5 not
save("sparkle_up", place(1.0,[(i*0.045,tone(f,0.5,9,B)*0.7) for i,f in enumerate([1568,1976,2349,2637,3136])]))
# success: kord major lembut
save("success", place(0.9,[(0,tone(784,0.8,6,S)),(0.02,tone(988,0.8,6,S)),(0.04,tone(1175,0.8,6,S)),(0.04,tone(1568,0.6,8,S)*0.5)]))
# air whoosh (pendek, lembut)
n=rng.standard_normal(int(SR*0.4)); tt=t(0.4)
save("air", (lp(n,0.12)-lp(n,0.02))*np.sin(np.pi*tt/0.4)**2,0.5)
# heart pop (pop + ting kecil) untuk bahagian penutup
p=lp(rng.standard_normal(int(SR*0.02)),0.4)*np.exp(-t(0.02)*200)
save("heartpop", place(0.8,[(0,p),(0.01,tone(1047,0.12,25,S)),(0.07,tone(2637,0.6,8,B)*0.6)]))
