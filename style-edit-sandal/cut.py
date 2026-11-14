# Source-time segments [start,end] from main.mov (take terbaik, pause & ulang dibuang)
import json,subprocess,sys
SEG=[(37.85,41.05),(11.75,18.96),(96.55,102.55),(105.65,116.75),(140.15,141.95),(155.40,162.30),
     (163.65,167.05),(197.00,200.50),(205.40,205.95),(206.30,211.25),(217.25,222.30),(226.90,228.95)]
SEG=[(a,round(a+round((b-a)*30)/30,4)) for a,b in SEG]  # tepat ikut frame 30fps
def out_t(src):
    o=0
    for a,b in SEG:
        if a<=src<=b: return round(o+src-a,2)
        o+=b-a
    raise ValueError(src)
if __name__=="__main__":
    import os
    src=sys.argv[1]; os.makedirs("seg",exist_ok=True); L=[]
    for i,(a,b) in enumerate(SEG):
        o=f"seg/{i:02d}.mp4"; d=b-a
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",src,"-t",f"{d:.3f}","-af",f"afade=t=in:d=0.02,afade=t=out:st={d-0.03:.2f}:d=0.03",
          "-r","30","-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000","-threads","2",o],check=True)
        L.append(f"file '{o}'")
    open("seg/list.txt","w").write("\n".join(l.replace("seg/","") for l in L))
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","seg/list.txt","-c","copy","assets/footage.mp4"],check=True)
    print("DUR",round(sum(b-a for a,b in SEG),2))
