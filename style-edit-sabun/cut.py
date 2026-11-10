# Potong footage: buang pause/gagap/ulang, susun hook di depan, speed 1.1, kuatkan suara.
import subprocess,json,sys
SRC=sys.argv[1]; SPEED=1.1
SEG=[ # [mula, tamat] masa asal (saat)
 [44.12,46.95],   # HOOK: pakai yang ini sebab baju korang takkan ada bau hapak
 [4.05,6.72],     # sabun basuh baju paling wangi
 [16.7,20.85],    # bila keluar dari mesin ni wangi semerbak
 [29.6,32.7],     # kalau korang suka basuh baju waktu malam, jemur lambat
 [32.8,34.6],     # jemur dalam ruang tertutup
 [37.1,40.55],    # memang recommended untuk yang selalu sidai lambat
 [74.8,76.75],    # wangi sangat-sangat korang kena cuba
 [79.6,82.5],     # memang wangi melekat dekat baju
 [89.4,93.2],     # bau wangi gila, floral perfume
 [94.9,97.05],    # bau bunga yang lembut je
 [119.9,123.2],   # lily, bunga, buah, susu
 [125.0,131.55],  # kepala memudahkan kerja, tak payah angkat, 5 kilo
 [144.25,147.3],  # penutup boleh tadah dan pam sahaja
 [151.25,158.75], # harga sangat murah, hilangkan bau hapak & kepam
 [160.7,162.9],   # memang sangat-sangat recommend
]
import os,tempfile
tmp=tempfile.mkdtemp(); t=0; edl=[]; lst=open(f"{tmp}/l.txt","w")
for i,(a,b) in enumerate(SEG):
    d=b-a; o=f"{tmp}/s{i}.mkv"
    subprocess.run(["ffmpeg","-v","error","-y","-threads","2","-ss",str(a),"-i",SRC,"-t",f"{d/SPEED:.3f}",
      "-vf",f"setpts=PTS/{SPEED}","-af",f"afade=t=in:d=0.02,atempo={SPEED},afade=t=out:st={d/SPEED-0.04:.3f}:d=0.04",
      "-c:v","libx264","-crf","14","-preset","fast","-pix_fmt","yuv420p","-r","30",
      "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-c:a","pcm_s16le","-ar","48000",o],check=True)
    lst.write(f"file '{o}'\n"); edl.append([a,b,round(t,3)]); t+=d/SPEED
lst.close()
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c:v","copy",
  "-af","highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,loudnorm=I=-13:TP=-1.2:LRA=9",
  "-c:a","aac","-b:a","192k","-ar","48000","assets/footage.mp4"],check=True)
json.dump({"speed":SPEED,"edl":edl,"dur":round(t,3)},open("edl.json","w"),indent=1)
print("DUR",round(t,2))
