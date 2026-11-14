# Source-time segments [start,end] from main.mov (take terbaik, pause & ulang dibuang)
import json,subprocess,sys
SEG=[(66.50,69.30),(69.40,72.05),(11.34,19.15),(85.00,90.15),(97.85,99.10),(106.04,116.40),
     (140.45,141.95),(155.15,161.90),(175.85,179.75),(196.60,199.95),(205.05,205.95),(206.70,210.95),
     (217.50,221.95),(228.20,228.95)]
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
