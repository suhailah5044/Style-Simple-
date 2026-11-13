import subprocess,sys,json
# [source_in, source_out] — urutan babak
SEG=[(93.0,96.4),(0.6,3.6),(27.0,30.4),(36.0,39.2),(45.0,48.2),(81.0,84.4),(42.0,45.0),
     (66.0,69.4),(51.0,54.0),(120.0,123.2),(108.0,111.2),(126.0,129.0),(129.2,132.0),(133.0,136.6)]
src=sys.argv[1]
f="".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];" for i,(a,b) in enumerate(SEG))
f+="".join(f"[v{i}][a{i}]" for i in range(len(SEG)))+f"concat=n={len(SEG)}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[v]","-map","[a]",
 "-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
 "-c:a","aac","-b:a","192k","assets/footage.mp4"],check=True)
t=0;out=[]
for a,b in SEG: out.append(round(t,2)); t+=b-a
print(json.dumps(out),round(t,2))
