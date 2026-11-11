# Potong ayat ulang/gagap/pause, b-roll stabil, speed 1.1, kuatkan suara -> assets/footage.mp4 + cuts.json
import numpy as np, wave, json, subprocess, sys
RAW=sys.argv[1]; AUD=sys.argv[2]   # raw.mov, audio.wav (16k mono)
SPEED=1.1
# [audio_src_start, audio_src_end, video_src_start|None, label]
S=[
 [0.00,2.66,None,"Beg sekolah daripada Shopee ni"],
 [9.66,12.95,None,"setiap tahun saya masih repeat sebab dia memang tahan lasak"],
 [13.10,14.76,None,"saya suka dia water resistant"],
 [25.22,26.82,None,"kalau kena air pun tak risau"],
 [26.82,28.36,None,"dia jatuh lalu sahaja"],
 [34.52,36.14,None,"tengok dia tak tembus ke dalam"],
 [37.93,41.95,None,"tahan lasak dah dua tahun saya pakai beg ni"],
 [41.95,45.52,None,"hari tu beli plain, kali ni corak"],
 [49.24,50.02,None,"kompartmen dia"],
 [51.04,51.56,None,"begini"],
 [52.08,53.56,None,"ada kompartmen dekat dalam"],
 [55.72,57.70,None,"kalau ambil combo dapat sekali pen"],
 [59.00,64.40,None,"design cantik, jahitan kemas"],
 [82.04,84.14,None,"saya suka sebab anak memang suka"],
 [86.88,88.38,None,"dia kata pakai memang selesa"],
 [88.38,91.54,None,"span tebal tak nipis"],
 [91.54,94.00,None,"bila pakai memang elok"],
 [95.98,100.06,None,"sekolah rendah, menengah, travel"],
 [102.44,103.56,None,"memang sangat2 recommend"],
 [103.56,106.82,73.6,"kualiti elok tau cantik (b-roll stabil)"],
 [110.96,113.96,None,"anak kita memang lasak"],
 [113.96,117.60,None,"bakul kuning, harga murah"],
 [76.06,77.94,None,"sementara warna yang"],
 [78.92,82.16,None,"cantik2 masih ada, cepat grab"],
]
wf=wave.open(AUD); sr=wf.getframerate(); a=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(float)
hop=sr//100; rms=np.sqrt(np.convolve(a**2,np.ones(hop*2)/(hop*2),'same'))[::hop]  # 10ms
def snap(t,lo,hi):
    i0,i1=max(0,int((t+lo)*100)),int((t+hi)*100); return (i0+int(np.argmin(rms[i0:i1])))/100
cuts=[];C={}
def sn(t,lo,hi):
    if t not in C: C[t]=snap(t,-0.06,0.06) if t in shared else snap(t,lo,hi)
    return C[t]
ends={e for s,e,v,l in S}; shared={s for s,e,v,l in S if s in ends}
for s,e,v,l in S:
    s2=sn(s,-0.10,0.04); e2=sn(e,-0.04,0.12)
    cuts.append([s2,e2,(v if v is not None else s2),l])
fv=[];fa=[];n=len(cuts)
for i,(s,e,v,l) in enumerate(cuts):
    d=e-s
    fv.append(f"[0:v]trim=start={v}:duration={d:.3f},setpts=PTS-STARTPTS[v{i}]")
    fa.append(f"[0:a]atrim=start={s}:duration={d:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={d-0.025:.3f}:d=0.025[a{i}]")
cat="".join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[cv][ca]"
post=(f"[cv]setpts=PTS/{SPEED}[vo];"
      f"[ca]atempo={SPEED},highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
      f"loudnorm=I=-13:TP=-1.2:LRA=9[ao]")
fc=";".join(fv+fa)+";"+cat+";"+post
subprocess.run(["ffmpeg","-v","error","-y","-i",RAW,"-filter_complex",fc,"-map","[vo]","-map","[ao]",
 "-c:v","libx264","-preset","medium","-crf","14","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
 "-r","30","-c:a","aac","-b:a","256k","-ar","48000","assets/footage.mp4"],check=True)
# peta masa: src -> output
out=[];t=0
for s,e,v,l in cuts: out.append([s,e,round(t/SPEED,3),l]); t+=e-s
json.dump({"cuts":out,"dur":round(t/SPEED,3)},open("cuts.json","w"),indent=0)
print("DUR",round(t/SPEED,2))
for s,e,o,l in out: print(f"{o:6.2f}  src {s:.2f}-{e:.2f}  {l}")
