import subprocess,sys,json
# [source_in, source_out] — urutan babak
SEG=[(93.0,95.8),(1.0,3.1),(27.3,29.4),(36.5,38.6),(45.5,47.6),(86.0,88.1),(42.3,44.4),
     (66.5,68.6),(51.4,53.5),(120.4,122.5),(108.4,110.5),(126.4,128.5),(129.5,131.6),(133.4,135.6)]
def main():
 src=sys.argv[1]
 f="".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];" for i,(a,b) in enumerate(SEG))
 f+="".join(f"[v{i}][a{i}]" for i in range(len(SEG)))+f"concat=n={len(SEG)}:v=1:a=1[v][a]"
 subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[v]","-map","[a]",
  "-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
  "-c:a","aac","-b:a","192k","assets/footage.mp4"],check=True)
 t=0;out=[]
 for a,b in SEG: out.append(round(t,2)); t+=b-a
 print(json.dumps(out),round(t,2))
if __name__=='__main__': main()
