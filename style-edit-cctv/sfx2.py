import numpy as np, wave
SR=48000; rng=np.random.default_rng(7)
def save(n,x,g=0.8):
    x=x/(np.max(np.abs(x))+1e-9)*g
    d=(np.column_stack([x,x])*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
def t(d): return np.arange(int(SR*d))/SR
def tone(f,d,dec=20,harm=((1,1),),att=0.003):
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
# cork pop: thump + resonant pitch-up "fwop" + fizz
tt=t(0.09); f=350+900*(tt/0.09)**0.6; ph=2*np.pi*np.cumsum(f)/SR
fwop=np.sin(ph)*np.sin(np.pi*tt/0.09)
burst=lp(rng.standard_normal(int(SR*0.03)),0.35)*np.exp(-t(0.03)*120)*2
fz=rng.standard_normal(int(SR*0.9)); fz=(fz-lp(fz,0.3))*np.exp(-t(0.9)*5)*0.12
save("cork", place(1.0,[(0,burst),(0.004,fwop),(0.06,fz)]))
# ui blip (2-note up)
H=((1,1),(3,.12))
save("ui_blip", place(0.35,[(0,tone(1047,0.12,30,H)),(0.065,tone(1568,0.2,22,H))]))
# ui notif (marimba-ish)
M=((1,1),(4,.25),(10,.05))
save("ui_notif", place(0.6,[(0,tone(784,0.35,14,M)),(0.1,tone(1175,0.45,11,M))]))
# ui confirm (3 ascending triangle-ish)
T=((1,1),(3,.11),(5,.04))
save("ui_confirm", place(0.7,[(0,tone(1047,0.25,16,T)),(0.07,tone(1319,0.25,16,T)),(0.14,tone(1568,0.45,10,T))]))
# ui tap
save("ui_tap", tone(2400,0.05,90,((1,1),(2.1,.4)))+np.r_[rng.standard_normal(200)*np.exp(-np.arange(200)/25)*0.4,np.zeros(int(SR*0.05)-200)])
# glass ting ting (higher, shorter than before)
G=((1,1),(2.32,.3),(4.25,.12))
save("glass_ting", place(0.9,[(0,tone(3136,0.6,7,G)),(0.1,tone(3951,0.7,6,G))]))
# coin
c1=np.sign(np.sin(2*np.pi*988*t(0.07)))*0.4; c2=np.sign(np.sin(2*np.pi*1319*t(0.4)))*0.4*np.exp(-t(0.4)*7)
save("coin", lp(place(0.5,[(0,c1),(0.07,c2)]),0.5),0.6)
# sub boom
tt=t(0.7); f=70*np.exp(-tt*3)+38; ph=2*np.pi*np.cumsum(f)/SR
save("sub_boom", np.sin(ph)*np.exp(-tt*4.5)*np.minimum(1,tt/0.008))
# riser + shimmer
n=rng.standard_normal(int(SR*0.5)); tt=t(0.5)
y=n-lp(n,0.2); r=y*(tt/0.5)**2*0.5
sh=[(0.45+i*0.035,tone(f,0.5,9,G)*0.6) for i,f in enumerate([2637,3136,3951,4699])]
save("riser_shimmer", place(1.1,[(0,r)]+sh))
# soft swoosh
n=rng.standard_normal(int(SR*0.35)); tt=t(0.35)
save("swoosh", lp(n,0.08)*np.sin(np.pi*tt/0.35)**3)
