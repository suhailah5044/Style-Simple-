import sys,json,wave,numpy as np,subprocess
sys.path.insert(0,'.'); import cuts
def env(f):
    w=wave.open(f+".wav"); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    hop=160; n=len(a)//hop; r=np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1)+1e-12)
    return 20*np.log10(r)
E={f:env(f) for f in ("f1","f2")}
def snap(f,t,kind):
    e=E[f]; i=int(t*100)
    lo,hi=(i-4,i+4) if kind=="s" else (i-3,i+6)
    lo=max(lo,0);hi=min(hi,len(e)-1)
    seg=e[lo:hi]; j=lo+int(np.argmin(seg))
    return j/100
name=sys.argv[1]; segs=getattr(cuts,name)
out=[];parts=[]
for k,(f,s,e,lab) in enumerate(segs):
    s2,e2=snap(f,s,"s"),snap(f,e,"e")
    out.append([f,s2,e2,lab])
fc=[];ins=[]
for k,(f,s,e,lab) in enumerate(out):
    src={"f1":0,"f2":1}[f]; d=e-s; fd=0.025
    fc.append(f"[{src}:v]trim={s}:{e},setpts=PTS-STARTPTS,fps=30[v{k}];[{src}:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d={fd},afade=t=out:st={d-fd:.3f}:d={fd}[a{k}]")
n=len(out)
fc.append("".join(f"[v{k}][a{k}]" for k in range(n))+f"concat=n={n}:v=1:a=1[v][a]")
open(f"cut/{name}.fc","w").write(";".join(fc))
cmd=["ffmpeg","-v","error","-y","-i","dl/f1.mov","-i","dl/f2.mov","-filter_complex_script",f"cut/{name}.fc","-map","[v]","-map","[a]",
     "-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-ar","48000",f"cut/{name}.mp4"]
subprocess.run(cmd,check=True)
# timeline of segments in output
t=0;tl=[]
for f,s,e,lab in out: tl.append([round(t,2),round(t+e-s,2),f,s,e,lab]); t+=e-s
json.dump(tl,open(f"cut/{name}_tl.json","w"),ensure_ascii=False,indent=0)
for x in tl: print(x)
print("DUR",round(t,2))
