# Hook sahaja 0-3s. Style: tulisan tangan kecil, huruf kecil, putih, tengah ruang kosong atas (ikut contoh TikTok "tahan lasak").
# Tiada muzik — audio asal (suara) sahaja.
# Guna: python3 build.py input.mov output.mp4
import subprocess,sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
FONT=os.path.join(HERE,"assets","Cweyons-Regular.ttf")
# [start, end, text, y, size]   (font tiada nombor / '&')
O=[
 [0.10,3.00,"steady gila holder ni",270,72],
]
fi,fo,rise=0.30,0.25,14
f=[]
for s,e,t,y,sz in O:
    a=f"if(lt(t,{s+fi}),(t-{s})/{fi},if(gt(t,{e-fo}),({e}-t)/{fo},1))"
    yy=f"{y}+{rise}*(1-min(1,(t-{s})/{fi}))"
    f.append(f"drawtext=fontfile='{FONT}':text='{t}':fontsize={sz}:fontcolor=white:"
             f"shadowcolor=black@0.45:shadowx=0:shadowy=3:x=(w-text_w)/2:y='{yy}':alpha='{a}':enable='between(t,{s},{e})'")
open(os.path.join(HERE,"filter.txt"),"w").write(",\n".join(f))
if len(sys.argv)>2:
    subprocess.run(["ffmpeg","-v","error","-y","-i",sys.argv[1],"-filter_script:v",os.path.join(HERE,"filter.txt"),
      "-c:v","libx264","-preset","medium","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
      "-movflags","+faststart",sys.argv[2]],check=True)
