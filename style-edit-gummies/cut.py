import subprocess,json
# segmen sumber [mula, tamat] — hook dulu, buang pause & ayat ulang
SEG=[[55.62,58.78],[3.35,7.12],[19.72,21.85],[29.05,30.8],[31.72,32.52],[37.08,40.46],[51.55,55.6],[58.82,60.32],[63.0,66.25],[67.35,68.7],[87.0,91.5],[91.72,96.22],[96.6,97.65],[98.22,100.15],[110.72,113.35]]
f=";".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.2f}:d=0.03[a{i}]" for i,(a,b) in enumerate(SEG))
f+=";"+"".join(f"[v{i}][a{i}]" for i in range(len(SEG)))+f"concat=n={len(SEG)}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg","-v","error","-y","-i","src.mov","-filter_complex",f,"-map","[v]","-map","[a]","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-c:a","aac","-b:a","192k","assets/footage.mp4"],check=True)
# peta masa lama -> baru
t=0;M=[]
for a,b in SEG: M.append([a,b,round(t,2)]); t+=b-a
json.dump(M,open("map.json","w")); print("DUR",round(t,2)); [print(m) for m in M]
# B-roll: crop produk sahaja (tiada muka), bisu
for n,(s,x,y,w,h) in {"A":(93.0,0,1000,518,920),"B":(84.0,0,1000,518,920),"D":(66.0,300,1080,470,836)}.items():
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(s),"-t","4","-i","src.mov","-an","-vf",f"crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos","-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",f"assets/broll{n}.mp4"],check=True)
