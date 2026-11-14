# Source-time segments [start,end] from main.mov (take terbaik, pause & ulang dibuang)
import json,subprocess,sys
SEG=[(37.85,41.05),(96.55,102.55),(105.65,116.75),(152.30,162.30),
     (163.65,167.05),(197.00,200.50),(205.40,205.95),(206.30,211.25),(217.25,222.30),(226.90,228.95)]
SEG=[(a,round(a+round((b-a)*30)/30,4)) for a,b in SEG]  # tepat ikut frame 30fps
def out_t(src):
    o=0
    for a,b in SEG:
        if a<=src<=b: return round(o+src-a,2)
        o+=b-a
    raise ValueError(src)
if __name__=="__main__":
    # Video & audio diproses berasingan supaya tiada drift AAC (lip-sync tepat)
    import os,wave,numpy as np
    src=sys.argv[1]; os.makedirs("seg",exist_ok=True); L=[]; SR=48000
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vn","-ac","2","-ar",str(SR),"seg/src.wav"],check=True)
    ast=float(subprocess.run(["ffprobe","-v","error","-select_streams","a","-show_entries","stream=start_time","-of","csv=p=0",src],capture_output=True,text=True).stdout or 0)
    w=wave.open("seg/src.wav"); A=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(np.float32)
    parts=[]; fd=int(0.012*SR)
    for i,(a,b) in enumerate(SEG):
        o=f"seg/{i:02d}.mp4"; d=b-a; n=round(d*30)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",src,"-frames:v",str(n),"-an","-r","30",
          "-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p","-threads","2",o],check=True)
        L.append(f"file '{i:02d}.mp4'")
        s0=round((a-ast)*SR); seg=A[s0:s0+round(n/30*SR)].copy()
        r=np.linspace(0,1,fd)[:,None]; seg[:fd]*=r; seg[-fd:]*=r[::-1]; parts.append(seg)
    open("seg/list.txt","w").write("\n".join(L))
    out=np.concatenate(parts).clip(-32768,32767).astype(np.int16)
    w=wave.open("seg/aud.wav","w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","seg/list.txt","-i","seg/aud.wav","-map","0:v","-map","1:a",
      "-c:v","copy","-c:a","aac","-b:a","192k","assets/footage.mp4"],check=True)
    print("DUR",round(sum(b-a for a,b in SEG),2))
