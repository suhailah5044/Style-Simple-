import subprocess
S="../src/";b=60/118;L=round(4*b,3)
# file, src start, hdr
SH=[("5205",0.3,1),("main",8.8,0),("5206",6.6,1),("5206",10.4,1),("5211",0.5,1),("main",34.6,0),("5206",2.2,1),("5212",2.3,1),("main",28.7,0),("5211",5.2,1)]
ins=[];f=[]
TM="zscale=t=linear:npl=400,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,"
for i,(fn,ss,h) in enumerate(SH):
    ins+=["-ss",str(ss),"-t",str(L+0.1),"-i",S+fn+".mov"]
    f.append(f"[{i}:v]trim=0:{L},setpts=PTS-STARTPTS,fps=30,{TM if h else ''}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p[v{i}]")
f.append("".join(f"[v{i}]" for i in range(len(SH)))+f"concat=n={len(SH)}:v=1:a=0[o]")
subprocess.run(["ffmpeg","-v","error","-y"]+ins+["-filter_complex",";".join(f),"-map","[o]","-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","base2.mp4"],check=True)
