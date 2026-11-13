import subprocess,json
SEG=[(30.36,32.30),(0.00,4.62),(4.75,9.30),(9.55,12.60),(12.95,13.56),(13.85,16.05),(16.28,20.32),(20.62,24.15),(25.88,28.55),(32.80,34.70),(36.90,39.62),(42.40,46.36),(47.85,49.62),(49.68,51.15),(54.45,58.58),(63.70,65.50)]
f=[];t=0;m=[]
for i,(a,b) in enumerate(SEG):
    d=b-a
    f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={d-0.02:.3f}:d=0.02[a{i}]")
    m.append([round(t,3),a,b]);t+=d
n=len(SEG)
fc=";".join(f)+";"+"".join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[cv][ca];[cv]scale=1080:1920:flags=lanczos,setsar=1[ov]"
subprocess.run(["ffmpeg","-v","error","-y","-i","../dl/src.mov","-filter_complex",fc,"-map","[ov]","-map","[ca]","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-r","30","-c:a","aac","-b:a","192k","footage.mp4"],check=True)
json.dump(m,open("map.json","w"));print(m,t)
