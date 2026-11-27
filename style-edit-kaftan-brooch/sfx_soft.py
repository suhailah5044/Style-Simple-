# SFX lembut (soft) untuk gaya cadar: chime, bell, air whoosh, soft tap, sparkle
import numpy as np, wave
from scipy.signal import butter, lfilter
SR=48000; rng=np.random.default_rng(11)
def t(d): return np.arange(int(SR*d))/SR
def save(n,x,g=0.7):
    x=x/(np.max(np.abs(x))+1e-9)*g
    fade=np.minimum(1,np.arange(len(x))[::-1]/(SR*0.03)); x=x*fade
    d=(np.column_stack([x,x])*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
def tone(f,d,dec,harm=((1,1),),att=0.008):
    tt=t(d); x=sum(a*np.sin(2*np.pi*f*m*tt) for m,a in harm)*np.exp(-dec*tt); return x*np.minimum(1,tt/att)
def place(total,parts):
    out=np.zeros(int(SR*total))
    for off,s in parts:
        i=int(SR*off); n=min(len(s),len(out)-i); out[i:i+n]+=s[:n]
    return out
def bp(x,lo,hi): b,a=butter(2,[lo/(SR/2),hi/(SR/2)],'band'); return lfilter(b,a,x)
B=((1,1),(2.0,.18),(3.0,.06))
save("soft_chime", place(1.2,[(0,tone(1319,1.1,5,B)),(0.07,tone(1976,1.0,6,B)*0.6)]))
save("soft_bell",  place(1.6,[(0,tone(880,1.5,3.2,((1,1),(2.76,.2),(5.4,.05)))),(0.12,tone(1320,1.3,4,B)*0.5)]))
save("soft_tap",   place(0.5,[(0,tone(1047,0.45,12,((1,1),(4,.1))))]))
# air whoosh: band-passed noise with smooth swell
n=rng.standard_normal(int(SR*0.8)); env=np.sin(np.pi*np.linspace(0,1,len(n)))**2
save("air_whoosh", bp(n,500,3500)*env, 0.6)
# sparkle: little cascade of high soft notes
notes=[2093,2637,3136,3951]
save("soft_sparkle", place(1.4,[(i*0.06,tone(f,1.0,6,B)*(1-i*0.15)) for i,f in enumerate(notes)]))
# harp_rise: HOOK video ini — petikan harp naik lembut (C-E-G-C-E), lain dari hook video pertama
def pluck(f,d=1.6):
    tt=t(d); x=sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-(2.2+m*1.8)*tt) for m,a in ((1,1),(2,.35),(3,.12),(4,.05)))
    return x*np.minimum(1,tt/0.004)
save("harp_rise", place(2.0,[(i*0.09,pluck(f)*(0.75+i*0.06)) for i,f in enumerate([523.25,659.25,783.99,1046.5,1318.5])]), 0.65)
