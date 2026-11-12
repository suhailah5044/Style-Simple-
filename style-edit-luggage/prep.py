# Potong ayat ulang/gagap/pause, b-roll stabil, speed 1.1, kuatkan suara -> assets/footage.mp4 + cuts.json
import numpy as np, wave, json, subprocess, sys
RAW=sys.argv[1]; AUD=sys.argv[2]   # raw.mov, audio.wav (16k mono)
SPEED=1.1
# [audio_src_start, audio_src_end, video_src_start|None, label]
S=[
 [0.00,6.00,None,"HOOK: ini sebenarnya backpack, besar, muat 3-4 hari baju"],
 [9.00,12.75,None,"backpack luggage ni expandable, besarkan kecilkan"],
 [17.40,20.95,None,"dah letak 3 hari baju, sini boleh isi lagi"],
 [21.20,24.10,None,"ada tali, baju takkan terabur"],
 [27.40,31.05,None,"expand 16cm sampai 24cm"],
 [34.10,38.25,None,"baju banyak buka zip, ruang makin besar"],
 [38.30,41.60,None,"depan pun ada zip, isi barang"],
 [43.60,51.60,None,"paling best port USB, tak payah pegang powerbank"],
 [53.60,60.40,None,"waterproof, tak tembus"],
 [69.70,75.60,None,"pakai tak rasa berat, span tebal"],
 [82.95,85.85,None,"belakang ada kompartmen barang bernilai"],
 [89.50,94.40,None,"belakang ada ruang laptop"],
 [97.30,100.05,None,"depan, port kunci"],
 [65.70,67.60,None,"travel sangat memudahkan"],
 [60.50,63.80,None,"backpack besar sangat berbaloi"],
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
