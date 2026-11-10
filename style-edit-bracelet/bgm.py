# BGM lembut 'luxe lo-fi' 88bpm, dijana sendiri
import numpy as np, wave, sys
SR=44100; D=float(sys.argv[1]) if len(sys.argv)>1 else 64; bpm=88; b=60/bpm
N=int(SR*D); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(3)
def add(buf,i,s):
    n=min(len(s),N-i)
    if n>0: buf[i:i+n]+=s[:n]
def nf(m): return 440*2**((m-69)/12)
chords=[[60,64,67,71],[57,60,64,67],[53,57,60,64],[55,59,62,65]]  # Cmaj7 Am7 Fmaj7 G7
bar=4*b; k=0; tb=0.
while tb<D:
    ch=chords[k%4]; dur=bar; tt=np.arange(int(SR*dur))/SR
    env=np.minimum(1,tt/0.6)*np.minimum(1,(dur-tt)/0.5)
    pad=sum(np.sin(2*np.pi*nf(m)*tt+np.sin(2*np.pi*.3*tt))*(.5 if j else .7) for j,m in enumerate(ch))*env*.08
    i=int(SR*tb); add(L,i,pad*1.0); add(R,i,pad*.85)
    add(L,i,np.sin(2*np.pi*nf(ch[0]-24)*tt)*env*.12); add(R,i,np.sin(2*np.pi*nf(ch[0]-24)*tt)*env*.12)
    for s in range(8):  # pluck arp
        m=ch[[0,2,1,3,2,1,3,2][s]]+12; pt=np.arange(int(SR*.6))/SR
        pl=(np.sin(2*np.pi*nf(m)*pt)+.3*np.sin(4*np.pi*nf(m)*pt))*np.exp(-pt*7)*.06
        j=int(SR*(tb+s*b/2)); (add(L,j,pl) if s%2 else add(R,j,pl)); add(L if s%2 else R,j,pl*.4)
    for q in range(4):  # soft kick + hat
        j=int(SR*(tb+q*b)); kt=np.arange(int(SR*.25))/SR
        if q in (0,2): kk=np.sin(2*np.pi*np.cumsum(110*np.exp(-kt*25)+45)/SR)*np.exp(-kt*14)*.22; add(L,j,kk); add(R,j,kk)
        h=rng.standard_normal(int(SR*.04)); h=np.diff(h,prepend=0)*np.exp(-np.arange(len(h))/SR*120)*.02
        add(L,int(SR*(tb+q*b+b/2)),h); add(R,int(SR*(tb+q*b+b/2)),h)
    tb+=bar; k+=1
f=np.minimum(1,np.arange(N)/SR/1.5)*np.minimum(1,(D-np.arange(N)/SR)/2.5)
L*=f;R*=f; m=max(abs(L).max(),abs(R).max())
d=(np.column_stack([L,R])/m*.85*32767).astype(np.int16)
w=wave.open("sfx/bgm.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(d.tobytes());w.close()
