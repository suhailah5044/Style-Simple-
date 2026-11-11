# SFX & BGM sintesis (stereo, 48kHz). Set baru — berbeza dari standphone v1/v2.
import numpy as np,wave
SR=48000; rng=np.random.default_rng(7)
def T(d): return np.arange(int(SR*d))/SR
def env(t,a,d): return np.minimum(t/a,1)*np.exp(-t/d)
def save(n,L,R=None,g=0.9):
    R=L if R is None else R; x=np.stack([L,R],1); x=x/np.abs(x).max()*g
    w=wave.open(f"sfx/{n}.wav","w");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes((x*32767).astype(np.int16).tobytes());w.close()
def lp(x,c):
    y=np.zeros_like(x);a=np.exp(-2*np.pi*c/SR);z=0
    for i,v in enumerate(x): z=(1-a)*v+a*z;y[i]=z
    return y
def haas(x,ms=9): d=int(SR*ms/1000); return x,np.concatenate([np.zeros(d),x[:-d]])
# 1 prompt_up: UI prompt chime naik (subtitle)
t=T(.45); s=np.sin(2*np.pi*880*t)*env(t,.004,.09)+np.sin(2*np.pi*1318.5*np.maximum(t-.07,0))*env(np.maximum(t-.07,0),.004,.14)*(t>.07)
save("prompt_up",*haas(s+0.25*np.sin(2*np.pi*2637*t)*env(t,.002,.05)))
# 2 prompt_soft: UI prompt glassy (subtitle variasi)
t=T(.4); m=np.sin(2*np.pi*1046.5*t+2.2*np.sin(2*np.pi*2093*t)*np.exp(-t/.05)); save("prompt_soft",*haas(m*env(t,.003,.11),6))
# 3 pop_bubble: pop teks
t=T(.18); f=380+900*np.exp(-t/.018); s=np.sin(2*np.pi*np.cumsum(f)/SR)*env(t,.001,.035); save("pop_bubble",*haas(s,4))
# 4 click_soft: perubahan visual
t=T(.08); s=(rng.standard_normal(len(t))*np.exp(-t/.004))+0.6*np.sin(2*np.pi*2400*t)*np.exp(-t/.01); s=lp(s,6000); save("click_soft",s,0.85*s)
# 5 ding_usp: loceng FM (USP)
t=T(1.3); b=np.sin(2*np.pi*1568*t+3*np.sin(2*np.pi*1568*3.5*t)*np.exp(-t/.25))*env(t,.002,.45)
save("ding_usp",*haas(b+0.3*np.sin(2*np.pi*3136*t)*env(t,.002,.2),11))
# 6 tingting: dua nota chime (hook)
t=T(1.0)
def bell(f,t): return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.76*t)*np.exp(-t/.1))*env(t,.002,.32)
L=bell(2093,t)+np.concatenate([np.zeros(int(.12*SR)),bell(2637,t)[:-int(.12*SR)]])*.8
R=bell(2093,t)*.8+np.concatenate([np.zeros(int(.12*SR)),bell(2637,t)[:-int(.12*SR)]]); save("tingting",L,R)
# 7 whoosh_air: pertukaran footage, pan kiri->kanan
t=T(.6); n=rng.standard_normal(len(t)); e=np.sin(np.pi*np.clip(t/.55,0,1))**2
c=np.convolve(n,np.ones(6)/6,'same')-np.convolve(n,np.ones(40)/40,'same'); w=c*e; p=np.clip(t/.55,0,1)
save("whoosh_air",w*np.cos(p*np.pi/2),w*np.sin(p*np.pi/2))
# 8 impact_soft: kemunculan visual penting
t=T(.9); f=110*np.exp(-t/.25)+42; s=np.sin(2*np.pi*np.cumsum(f)/SR)*env(t,.003,.22)+0.25*lp(rng.standard_normal(len(t)),900)*np.exp(-t/.05)
save("impact_soft",*haas(s,3))
# 9 sparkle_up: highly recommended / CTA
t=T(1.1); s=np.zeros(len(t))
for k,f in enumerate([1760,2217,2637,3322,3520,4434]):
    o=int(k*.07*SR); tt=t[:len(t)-o]; s[o:]+=np.sin(2*np.pi*f*tt)*env(tt,.002,.18)*(1-k*.08)
save("sparkle_up",*haas(s,13))
# 10 cash_tick: harga
t=T(.7); s=np.sin(2*np.pi*2794*t)*env(t,.001,.12)+np.sin(2*np.pi*3729*np.maximum(t-.06,0))*env(np.maximum(t-.06,0),.001,.2)*(t>.06)
save("cash_tick",*haas(s,7))
# BGM: lofi lembut 92bpm (Fmaj7-Em7-Dm7-Cmaj7), stereo
DUR=70; bpm=92; beat=60/bpm; t=T(DUR); L=np.zeros(len(t)); R=np.zeros(len(t))
ch=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]]
def mf(n): return 440*2**((n-69)/12)
bar=beat*4; nb=int(DUR/bar)+1
for i in range(nb):
    for j,n in enumerate(ch[i%4]):
        st=int((i*bar+j*0.03)*SR); d=int(bar*SR); tt=np.arange(min(d,len(t)-st))/SR
        if len(tt)<=0: continue
        v=(np.sin(2*np.pi*mf(n)*tt)+.3*np.sin(2*np.pi*mf(n)*2*tt)*np.exp(-tt/.4))*np.minimum(tt/.02,1)*np.exp(-tt/1.6)*.18
        (L if j%2==0 else R)[st:st+len(tt)]+=v; (R if j%2==0 else L)[st:st+len(tt)]+=v*.6
    bn=ch[i%4][0]-12
    for k in [0,2.5]:
        st=int((i*bar+k*beat)*SR); tt=np.arange(min(int(beat*1.2*SR),len(t)-st))/SR
        if len(tt)>0: v=np.sin(2*np.pi*mf(bn)*tt)*np.minimum(tt/.01,1)*np.exp(-tt/.5)*.35; L[st:st+len(tt)]+=v; R[st:st+len(tt)]+=v
for k in range(int(DUR/beat)):
    st=int(k*beat*SR)
    if k%2==0:
        tt=np.arange(int(.25*SR))/SR; v=np.sin(2*np.pi*(55+70*np.exp(-tt/.03))*tt)*np.exp(-tt/.09)*.5
        if st+len(tt)<len(t): L[st:st+len(tt)]+=v; R[st:st+len(tt)]+=v
    for h in [0,.5]:
        s2=int((k+h)*beat*SR); n=rng.standard_normal(int(.05*SR)); n=n-np.convolve(n,np.ones(8)/8,'same'); v=n*np.exp(-np.arange(len(n))/SR/.012)*.07
        if s2+len(v)<len(t): (L if h else R)[s2:s2+len(v)]+=v; (R if h else L)[s2:s2+len(v)]+=v*.5
fade=np.minimum(1,np.minimum(t/1.5,(DUR-t)/2.5)); L=lp(L,3500)*fade; R=lp(R,3500)*fade
save("bgm_lofi",L,R,0.8)
