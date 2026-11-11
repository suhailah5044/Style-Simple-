import subprocess,sys
from edit import *
MAIN,BROLL,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
# video pieces on cut timeline
pieces=[]
for a,b in SEGS:
    t=a; reps=sorted([c for c in CUT if a<=c[0][0]<b],key=lambda c:c[0][0])
    for (s,e),(src,vin) in reps:
        if s>t: pieces.append(("main",t,s))
        pieces.append((src,vin,vin+(e-s))); t=e
    if t<b: pieces.append(("main",t,b))
VF="scale=in_range=pc:out_range=tv,format=yuv420p"
fc=[];vl=[]
for i,(src,a,b) in enumerate(pieces):
    inp=0 if src=="main" else 1
    fc.append(f"[{inp}:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps=30[v{i}]");vl.append(f"[v{i}]")
al=[]
for i,(a,b) in enumerate(SEGS):
    fc.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03[a{i}]");al.append(f"[a{i}]")
fc.append(f"{''.join(vl)}concat=n={len(vl)}:v=1:a=0,setpts=PTS/{SPEED},{VF}[vo]")
fc.append(f"{''.join(al)}concat=n={len(al)}:v=0:a=1,atempo={SPEED},highpass=f=80,"
          "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
          "loudnorm=I=-13:TP=-1.2:LRA=7,aresample=48000[ao]")
cmd=["ffmpeg","-v","error","-y","-i",MAIN,"-i",BROLL,"-filter_complex",";".join(fc),"-map","[vo]","-map","[ao]",
     "-c:v","libx264","-preset","medium","-crf","15","-r","30","-g","30","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-color_range","tv",
     "-c:a","aac","-b:a","256k","-movflags","+faststart",OUT]
print(len(pieces),"pieces, dur",DUR); subprocess.run(cmd,check=True)
