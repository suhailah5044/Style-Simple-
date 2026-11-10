# SFX set v3 (bracelet) — dijana sendiri, bebas lesen
import numpy as np, wave
SR=48000; rng=np.random.default_rng(11)
def save(n,L,R=None,g=0.8):
    R=L if R is None else R; m=max(np.max(np.abs(L)),np.max(np.abs(R)))+1e-9
    d=(np.column_stack([L,R])/m*g*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
def t(d): return np.arange(int(SR*d))/SR
def tone(f,d,dec=20,H=((1,1),),att=0.002):
    tt=t(d); return sum(a*np.sin(2*np.pi*f*m*tt) for m,a in H)*np.exp(-dec*tt)*np.minimum(1,tt/att)
def place(T,parts):
    o=np.zeros(int(SR*T))
    for off,s in parts:
        i=int(SR*off);n=min(len(s),len(o)-i);o[i:i+n]+=s[:n]
    return o
def lp(x,k):
    y=np.zeros_like(x);a=0.
    for i in range(len(x)): a+=k*(x[i]-a);y[i]=a
    return y
def bp(x,k1,k2): return lp(x,k2)-lp(x,k1)
BELL=((1,1),(2.76,.35),(5.4,.12),(8.9,.05))
# intro: headphone shimmer pan L->R + soft bell
d=1.6;tt=t(d);n=rng.standard_normal(len(tt));sh=bp(n,0.05,0.5)*np.sin(np.pi*tt/d)**2*0.5
sp=sum(tone(f,1.2,6,BELL)*0.2 for f in (2093,2637,3136))
pan=np.clip(tt/d,0,1);bell=place(d,[(0.55,tone(1319,1.0,5,BELL)),(0.72,tone(1976,0.9,5,BELL)*.7)])
save("intro_pan",sh*(1-pan)+bell+place(d,[(0.3,sp)])*.3,sh*pan+bell+place(d,[(0.3,sp)])*.3)
# ui prompt: soft click + glide sine
c=bp(rng.standard_normal(int(SR*.008)),.2,.9)*np.exp(-t(.008)*500)
tt=t(.22);g=np.sin(2*np.pi*np.cumsum(880+700*tt/.22)/SR)*np.exp(-tt*16)*.5
save("ui_prompt",place(.4,[(0,c),(.012,g)]))
# ting ting
save("tingting",place(.9,[(0,tone(2349,.5,9,BELL)),(.11,tone(3136,.7,8,BELL))]))
# ding USP
save("ding",place(1.2,[(0,tone(1568,1.1,4.5,BELL))]))
# pop bubble
tt=t(.07);save("pop",np.sin(2*np.pi*np.cumsum(500+1400*tt/.07)/SR)*np.exp(-tt*55))
# click
save("click",place(.12,[(0,c),(.04,c*.6)]))
# whoosh: noise sweep w/ stereo pan
d=.55;tt=t(d);n=rng.standard_normal(len(tt));env=np.sin(np.pi*(tt/d)**.7)**2
lo=lp(n,.04)*env;hi=bp(n,.08,.35)*env*.5;s=lo+hi
save("whoosh",s*(1-tt/d*.6),s*(.4+tt/d*.6))
# soft impact: sub thump + air
tt=t(.6);th=np.sin(2*np.pi*np.cumsum(90-50*tt/.6)/SR)*np.exp(-tt*9);air=lp(rng.standard_normal(len(tt)),.1)*np.exp(-tt*14)*.3
save("soft_impact",th+air)
# frame break: glass-ish crack (clicks) + whoosh tail
cr=place(.5,[(i*.018,bp(rng.standard_normal(400),.3,.95)*np.exp(-t(400/SR)*300)*(1-i*.08)) for i in range(6)])
save("frame_break",cr+place(.5,[(.05,lo[:int(SR*.45)]*.6)]))
# sparkle (worth/cantik)
sp=place(1.0,[(i*.06,tone(f,.5,10,BELL)*.5) for i,f in enumerate((2637,3136,3520,4186,4699))])
save("sparkle",sp)
