# SFX baru (lain dari v1/v2): whoosh, pop, click, ding, soft impact, sparkle, hook hit
import numpy as np,wave
R=48000
def save(n,x):
    x=x/ (np.abs(x).max()+1e-9)*0.9
    w=wave.open(f"sfx/{n}.wav","w");w.setnchannels(1);w.setsampwidth(2);w.setframerate(R)
    w.writeframes((x*32767).astype(np.int16).tobytes());w.close()
t=lambda d:np.arange(int(R*d))/R
rng=np.random.default_rng(7)
def lp(x,a):  # 1-pole lowpass
    y=np.zeros_like(x);s=0
    for i,v in enumerate(x): s+=a*(v-s);y[i]=s
    return y
# whoosh: noise band sweep
d=0.55;T=t(d);n=rng.standard_normal(len(T));env=np.sin(np.pi*T/d)**2
a=0.02+0.25*np.sin(np.pi*T/d);y=np.zeros_like(n);s=0
for i,v in enumerate(n): s+=a[i]*(v-s);y[i]=s
save("air_whoosh",y*env)
# pop: bubbly pitch drop
d=0.16;T=t(d);f=900*np.exp(-T*28)+280;ph=2*np.pi*np.cumsum(f)/R
save("bubble_pop",np.sin(ph)*np.exp(-T*30)*(1-np.exp(-T*900)))
# click: crisp UI tick (2 transients)
d=0.09;T=t(d);c=np.sin(2*np.pi*3200*T)*np.exp(-T*160)+0.6*np.sin(2*np.pi*1800*T)*np.exp(-T*120)
save("soft_click",c+0.3*rng.standard_normal(len(T))*np.exp(-T*600))
# ding: bell (inharmonic partials)
d=1.1;T=t(d);b=sum(a*np.sin(2*np.pi*1320*r*T)*np.exp(-T*k) for a,r,k in [(1,1,4),(.5,2.76,7),(.3,5.4,11),(.2,.5,3)])
save("bell_ding",b*(1-np.exp(-T*2000)))
# soft impact: low thump + air
d=0.7;T=t(d);f=95*np.exp(-T*6)+38;th=np.sin(2*np.pi*np.cumsum(f)/R)*np.exp(-T*7)
save("soft_impact",th+0.15*lp(rng.standard_normal(len(T)),0.08)*np.exp(-T*12))
# sparkle: rising arp of tiny tings
d=0.9;T=t(d);x=np.zeros_like(T)
for i,fr in enumerate([1760,2217,2637,3136,3520]):
    o=int(i*0.07*R);tt=T[:len(T)-o];x[o:]+=np.sin(2*np.pi*fr*tt)*np.exp(-tt*9)*0.6
save("sparkle_rise",x)
# hook hit: impact + bright ting combo
d=1.0;T=t(d);hit=np.sin(2*np.pi*np.cumsum(120*np.exp(-T*9)+45)/R)*np.exp(-T*8)
tg=np.sin(2*np.pi*2093*T)*np.exp(-T*6)*0.35+np.sin(2*np.pi*3136*T)*np.exp(-T*9)*0.2
save("hook_hit",hit+tg)
# cash: two quick high dings
d=0.7;T=t(d);x=np.sin(2*np.pi*2637*T)*np.exp(-T*10);o=int(0.09*R);x[o:]+=np.sin(2*np.pi*3520*T[:-o])*np.exp(-T[:-o]*8)
save("cash_ting",x)
