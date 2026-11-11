# Potong footage: buang pause + gagap, snap titik potong ke tenaga audio paling rendah,
# fade audio 12ms setiap sambungan, zoom selang-seli 1.00/1.07 untuk sorok jump cut.
# Guna: python3 cut.py <config.json> <out.mp4>
import sys,json,subprocess,wave,numpy as np
cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
SRC=cfg["sources"]            # {"f1":"path.mov",...}
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-vn","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
def silences(p):
    r=subprocess.run(["ffmpeg","-i",p,"-af","silencedetect=noise=-32dB:d=0.18","-f","null","-"],capture_output=True,text=True).stderr
    s=[float(l.split("silence_start: ")[1]) for l in r.splitlines() if "silence_start" in l]
    e=[float(l.split("silence_end: ")[1].split()[0]) for l in r.splitlines() if "silence_end" in l]
    return list(zip(s,e+[1e9]))
A={k:load(v) for k,v in SRC.items()}; SIL={k:silences(v) for k,v in SRC.items()}
def rms(k,t): i=int(t*16000); x=A[k][max(0,i-80):i+80]; return float(np.sqrt(np.mean(x*x))) if len(x) else 0
def snap(k,t,w=0.1):
    c=np.arange(t-w,t+w,0.005); return float(c[np.argmin([rms(k,x) for x in c])])
PAD=0.07
segs=[]
for k,a,b in cfg["keep"]:
    a=snap(k,a); b=snap(k,b)
    cur=a
    for s,e in SIL[k]:
        if e<=cur or s>=b: continue
        if s-cur>0.05: segs.append([k,cur,min(b,s+PAD)])
        cur=max(cur,e-PAD)
    if b-cur>0.12: segs.append([k,cur,b])
# merge tiny segments (<0.25s) into nothing to avoid flicker
segs=[s for s in segs if s[2]-s[1]>=0.25]
idx={k:i for i,k in enumerate(SRC)}
fc=[];o=0;mp=[]
for n,(k,a,b) in enumerate(segs):
    i=idx[k]; z=1.07 if n%2 else 1.0
    v=f"[{i}:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS"
    if z>1: v+=f",scale=iw*{z}:ih*{z}:flags=lanczos,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.42"
    fc.append(v+f",fps=30,format=yuv420p[v{n}]")
    d=b-a
    fc.append(f"[{i}:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d-0.015:.3f}:d=0.015[a{n}]")
    mp.append([k,round(a,3),round(b,3),round(o,3)]); o+=d
fc.append("".join(f"[v{n}][a{n}]" for n in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=1[v][a]")
cmd=["ffmpeg","-v","error","-y"]
for k in SRC: cmd+=["-i",SRC[k]]
cmd+=["-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000",out]
subprocess.run(cmd,check=True)
json.dump({"map":mp,"dur":round(o,3)},open(out+".map.json","w"))
print(f"{len(segs)} segmen, durasi {o:.2f}s")
