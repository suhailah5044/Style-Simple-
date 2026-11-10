# Potong footage: buang pause/gagap/ulang, susun hook di depan, speed 1.1, kuatkan suara.
import subprocess,json,sys
SRC=sys.argv[1]; SPEED=1.1
SEG=[ # [mula, tamat] masa asal — semua ayat depan kamera, ayat sama diambil sekali sahaja
 [44.12,46.95],   # HOOK: pakai yang ini sebab baju korang takkan ada bau hapak
 [4.05,6.72],     # sabun basuh baju paling wangi
 [9.0,12.38],     # tak tahu dah kali keberapa repeat sabun ni
 [12.38,13.1],    # sebab
 [14.55,20.85],   # walaupun sidai baju dekat luar, keluar dari mesin wangi semerbak
 [37.1,44.05],    # recommended untuk yang sidai lambat, sidai dalam rumah, basuh malam
 [72.62,76.75],   # ini daripada (jenama) serius, wangi sangat-sangat kena cuba
 [79.6,82.42],     # memang wangi melekat dekat baju
 [102.45,104.9],   # saya ambil ni floral perfume
 [105.9,107.75], # bau dia memang sangat-sangat lembut
 [133.8,139.4],   # saya suka kepala dia ada dua jenis, tak perlu angkat berat-berat
 [144.25,147.3],  # penutup ini boleh tadah dan pam sahaja
 [148.8,158.75],  # 5 liter sangat berat, harga murah, hilang bau hapak & kepam
 [160.7,162.9],   # memang sangat-sangat recommend
]
# dibuang (ulang): 47-53 penutup/pam (ada di 133-147), 65-72 jemur lambat/bau hapak (ada di hook & 37-44),
# 140-144 & 147-148 tadah/angkat berat (ulang), 21-25 & 77-79 gagap. Bahagian tanpa muka = tiru sound orang.
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
