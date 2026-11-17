# Jana SFX + muzik latar lofi lembut (ikut rujukan: muzik perlahan bawah suara,
# bunyi "tulis/scribble" bila tajuk kuning keluar, pop perkataan kecil,
# whoosh transisi blur, boom dalam untuk penutup gelap).
import numpy as np, wave, os
SR=44100; rng=np.random.default_rng(11)
os.makedirs("sfx",exist_ok=True)
def save(n,x,g=0.8):
    x=x/(np.max(np.abs(x))+1e-9)*g
    d=(np.column_stack([x,x])*32767).astype(np.int16)
    w=wave.open(f"sfx/{n}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
def t(d): return np.arange(int(SR*d))/SR
def lp(x,k):
    y=np.zeros_like(x);a=0.0
    for i in range(len(x)): a+=k*(x[i]-a); y[i]=a
    return y
def hp(x,k): return x-lp(x,k)
def place(total,parts):
    out=np.zeros(int(SR*total))
    for off,s in parts:
        i=int(SR*off); n=min(len(s),len(out)-i)
        if n>0: out[i:i+n]+=s[:n]
    return out

# --- scribble: marker/pen menulis laju (3 sapuan noise tinggi bertekstur)
def stroke(d):
    n=rng.standard_normal(int(SR*d)); tt=t(d)
    x=hp(n,0.35)
    am=0.55+0.45*np.sin(2*np.pi*(38+rng.random()*20)*tt+rng.random()*6)  # tekstur kertas
    env=np.sin(np.pi*tt/d)**0.7
    return x*am*env
save("scribble", place(0.42,[(0,stroke(0.11)),(0.13,stroke(0.09)),(0.24,stroke(0.15))]),0.55)

# --- pop kecil (perkataan putih)
tt=t(0.09); f=900*np.exp(-tt*35)+380
save("pop", np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*45)*np.minimum(1,tt/0.002),0.7)

# --- whoosh transisi blur
d=0.5; n=rng.standard_normal(int(SR*d)); tt=t(d)
k=0.02+0.25*np.sin(np.pi*tt/d)**2
y=np.zeros_like(n);a=0.0
for i in range(len(n)): a+=k[i]*(n[i]-a); y[i]=a
save("whoosh", y*np.sin(np.pi*tt/d)**2,0.7)

# --- boom penutup: sub drop + ekor reverb panjang
d=3.0; tt=t(d); f=55*np.exp(-tt*1.2)+32
sub=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*1.6)*np.minimum(1,tt/0.004)
hit=lp(rng.standard_normal(int(SR*0.08)),0.25)*np.exp(-t(0.08)*60)
tail=lp(rng.standard_normal(int(SR*d)),0.04)*np.exp(-tt*1.4)*0.25
save("boom", place(d,[(0,sub),(0,hit*0.8),(0,tail)]),0.9)

# --- muzik latar lofi lembut (Rhodes + bass + hat perlahan), 78 BPM, loop 4 akord
BPM=78; beat=60/BPM; bar=4*beat; TOTAL=64.0
def ep(freq,d):
    tt=t(d)
    x=np.sin(2*np.pi*freq*tt)+0.25*np.sin(2*np.pi*2*freq*tt)*np.exp(-tt*3)+0.08*np.sin(2*np.pi*3*freq*tt)*np.exp(-tt*6)
    trem=1+0.08*np.sin(2*np.pi*4.5*tt)
    return x*trem*np.exp(-tt*0.9)*np.minimum(1,tt/0.012)
def mid(n): return 440*2**((n-69)/12)
chords=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]]   # Fmaj7 Em7 Dm7 Cmaj7
bass=[41,40,38,36]
parts=[]; b=0.0; i=0
while b<TOTAL:
    c=chords[i%4]
    for k,nn in enumerate(c): parts.append((b+k*0.018,ep(mid(nn),bar*1.05)*0.22))
    parts.append((b+2*beat+0.05,ep(mid(c[2]+12),beat*1.5)*0.08))
    bt=t(bar); parts.append((b,np.sin(2*np.pi*mid(bass[i%4])*bt)*np.exp(-bt*0.7)*np.minimum(1,bt/0.02)*0.35))
    for h in range(8):
        hh=hp(rng.standard_normal(int(SR*0.04)),0.6)*np.exp(-t(0.04)*90)*(0.05 if h%2 else 0.03)
        parts.append((b+h*beat/2,hh))
    b+=bar; i+=1
m=place(TOTAL,parts)
m=lp(m,0.35)                                  # rasa "lofi" lembut
m+=hp(rng.standard_normal(len(m)),0.5)*0.004  # hiss nipis
crack=np.zeros(len(m)); idx=rng.integers(0,len(m),400); crack[idx]=rng.standard_normal(400)*0.15
m+=lp(crack,0.5)
save("music", m, 0.7)
print("ok")
