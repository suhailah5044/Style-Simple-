# SFX set tambahan untuk variasi V2-V5 (sintetik, bebas lesen)
import numpy as np, wave
SR=44100; rng=np.random.default_rng(11)
def save(n,x,st=False):
    x=np.asarray(x,np.float64); x=x/(np.abs(x).max()+1e-9)*0.9
    if not st: x=np.stack([x,x],1)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((x*32767).astype(np.int16).tobytes());w.close()
def t(d):return np.arange(int(SR*d))/SR
def ex(x,k):return np.exp(-x*k)
def filt(x,fc,q=0.5):
    F=np.fft.rfft(x);fr=np.fft.rfftfreq(len(x),1/SR);F*=np.exp(-((fr-fc)/(fc*q))**2);return np.fft.irfft(F,len(x))
# swish pantas (slide)
x=t(0.32);n=len(x);s=np.zeros(n);B=512;no=rng.standard_normal(n)
for i in range(0,n,B):
    seg=no[i:i+B];fc=1200+5000*(i/n);s[i:i+B]=filt(np.pad(seg,(0,B-len(seg))),fc)[:len(seg)]
s*=np.sin(np.pi*np.linspace(0,1,n))**1.5;p=np.linspace(-.8,.8,n);save("swish_fast",np.stack([s*(1-p)/2,s*(1+p)/2],1),True)
# rise sweep pendek (zoom through)
x=t(0.45);f=200+1800*(x/0.45)**2;r=np.sin(2*np.pi*np.cumsum(f)/SR)*0.4+filt(rng.standard_normal(len(x)),3000,0.8)
save("rise_sweep",r*(x/0.45)**1.5*np.minimum(1,(0.45-x)*40))
# blip naik (iris)
x=t(0.18);f=np.linspace(600,1800,len(x));save("blip_up",np.sin(2*np.pi*np.cumsum(f)/SR)*ex(x,14))
# paper slide (wipe)
x=t(0.3);save("paper_slide",filt(rng.standard_normal(len(x)),2500,1.2)*np.sin(np.pi*x/0.3)*ex(x,4))
# camera shutter (break)
x=t(0.22);c=np.zeros(len(x))
for o in(0,0.07):
    i=int(o*SR);m=int(0.025*SR);c[i:i+m]+=rng.standard_normal(m)*np.exp(-np.arange(m)/(SR*0.004))
c+=0.3*filt(rng.standard_normal(len(x)),800)*ex(x,25);save("camera_shutter",c)
# thump low (hook/flash)
x=t(0.5);f=70*ex(x,5)+38;save("thump_low",np.sin(2*np.pi*np.cumsum(f)/SR)*ex(x,7))
# glass pluck (teks gaya A)
x=t(0.6);save("glass_pluck",sum(a*np.sin(2*np.pi*fq*x)*ex(x,k) for a,fq,k in[(1,1760,10),(.5,2640,14),(.3,4400,20)]))
# type burst (teks gaya B) - beberapa ketukan kekunci
x=t(0.55);tb=np.zeros(len(x))
for k,o in enumerate(np.arange(0,0.5,0.045)):
    i=int(o*SR);m=int(0.012*SR);tb[i:i+m]+=filt(rng.standard_normal(m),3500+300*(k%3),0.6)*np.exp(-np.arange(m)/(SR*0.003))*(0.7+0.3*(k%2))
save("type_burst",tb)
# chime soft (teks gaya C)
x=t(0.9);save("chime_soft",sum(np.sin(2*np.pi*fq*x)*ex(x,5+i*2) for i,fq in enumerate([1046.5,1318.5,1568]))*np.minimum(1,x*200))
# tick index (teks gaya D)
x=t(0.08);save("tick_index",np.sin(2*np.pi*1500*x)*ex(x,60)+0.3*rng.standard_normal(len(x))*ex(x,200))
# sparkle tail (USP)
x=t(1.0);sp=np.zeros(len(x))
for k in range(9):
    i=int(k*0.05*SR);y=x[:len(x)-i];sp[i:]+=np.sin(2*np.pi*(2000+k*260)*y)*np.exp(-y*12)*(1-k*0.08)
save("sparkle_tail",sp)
print("ok")
