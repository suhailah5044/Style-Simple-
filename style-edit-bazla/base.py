import subprocess
S="../src/"
A=[(3.02,6.10),(0.00,2.95),(6.16,9.90),(9.96,11.30),(11.96,13.80),(18.34,20.50),(42.86,46.90)]
# b-roll: file, src start, out start, dur
B=[("5205",0.6,6.9,2.3),("5206",10.4,10.25,2.1),("5211",1.0,13.3,2.2),("5212",2.5,16.3,2.0)]
f=[];n=len(A)
for i,(s,e) in enumerate(A):
    f.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v{i}];[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={e-s-0.04:.2f}:d=0.04[a{i}]")
f.append("".join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[av][aa]")
last="av"
for j,(fn,ss,o,d) in enumerate(B):
    f.append(f"[{j+1}:v]trim={ss}:{ss+d},setpts=PTS-STARTPTS+{o}/TB,fps=30,zscale=t=linear:npl=400,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuva420p,fade=t=in:st={o}:d=0.25:alpha=1,fade=t=out:st={o+d-0.25:.2f}:d=0.25:alpha=1[b{j}]")
    f.append(f"[{last}][b{j}]overlay=eof_action=pass[o{j}]");last=f"o{j}"
cmd=["ffmpeg","-v","error","-y","-i",S+"main.mov"]+sum([["-i",S+b[0]+".mov"] for b in B],[])+["-filter_complex",";".join(f),"-map",f"[{last}]","-map","[aa]","-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-c:a","aac","-b:a","192k","base.mp4"]
subprocess.run(cmd,check=True)
